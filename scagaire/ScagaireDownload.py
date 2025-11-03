"""
ScagaireDownload - Automated species database builder

This module automates the process of building a species-specific AMR gene database by:
1. Downloading genome assemblies from NCBI for a given species
2. Validating species classification using MASH
3. Running Abricate to predict AMR genes in each assembly
4. Aggregating results into a species-to-genes database

This enables users to create databases for species not included in the bundled data.
"""

import re
import os
import subprocess
import shutil
import pkg_resources
from tempfile import mkdtemp

from scagaire.MashSpecies import MashSpecies
from scagaire.AbricateAmrResults import AbricateAmrResults
from scagaire.SpeciesDatabase import  SpeciesDatabase

class ScagaireDownload:
    """
    Automated builder for species-specific AMR gene databases.
    
    Downloads genome assemblies for a species from NCBI, validates their
    taxonomic classification, predicts AMR genes, and creates a database
    mapping genes to species with occurrence counts.
    
    Attributes:
        species (str): Target species name
        output_file (str): Path to output database file
        output_directory (str): Working directory for downloads
        threads (int): Number of CPU threads
        refseq_category (str): RefSeq quality category
        assembly_level (str): Assembly completeness level
        mash_database (str): Path to MASH reference database
        min_coverage (int): Minimum gene coverage percentage
        min_identity (int): Minimum gene identity percentage
        downloads_directory (str): Pre-downloaded genomes directory
        abricate_database (list): List of Abricate databases to use
        verbose (bool): Enable verbose output
        debug (bool): Keep intermediate files
        minimum_distance (float): MASH distance threshold
        directories_to_cleanup (list): Temp directories to remove
    """
    
    def __init__(self, options):
        """
        Initialize the database builder.
        
        Args:
            options: Object with attributes:
                - species: Target species name
                - output_file: Output database file path
                - output_directory: Working directory
                - threads: Number of threads
                - refseq_category: RefSeq quality filter
                - assembly_level: Assembly level filter
                - mash_database: MASH reference database
                - min_coverage: Minimum gene coverage
                - min_identity: Minimum gene identity
                - downloads_directory: Pre-downloaded genomes path
                - abricate_database: Comma-separated database list
                - verbose: Enable verbose output
                - debug: Keep intermediate files
                - minimum_distance: MASH distance threshold
        """
        self.species = options.species
        self.output_file = options.output_file
        self.output_directory = options.output_directory
        self.threads = options.threads
        self.refseq_category = options.refseq_category
        self.assembly_level = options.assembly_level
        self.mash_database = options.mash_database
        self.min_coverage = options.min_coverage
        self.min_identity = options.min_identity
        self.downloads_directory = options.downloads_directory
        self.abricate_database = self.parse_abricate_database(options.abricate_database)
        self.verbose = options.verbose
        self.debug = options.debug
        self.minimum_distance = options.minimum_distance
        
        # Create output directory named after species if not specified
        if self.output_directory is None:
            self.output_directory = re.sub("[^a-zA-Z0-9]+", "_", self.species)

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        
        # Use bundled MASH database if not specified
        if self.mash_database is None:
            self.mash_database = str(pkg_resources.resource_filename( __name__, 'data/refseq_reference_20191031.msh'))
        
        self.directories_to_cleanup = []
        
    def parse_abricate_database(self, abricate_str):
        """
        Parse comma-separated Abricate database list.
        
        Args:
            abricate_str (str): Comma-separated database names
            
        Returns:
            list: List of database names
        """
        return abricate_str.split(",")

    def run(self):
        """
        Execute the database building workflow.
        
        Process:
        1. Download assemblies from NCBI (or use pre-downloaded)
        2. Find all genome FASTA files
        3. Validate species using MASH
        4. For each Abricate database:
           a. Run Abricate on all validated assemblies
           b. Aggregate gene occurrence counts
           c. Write to output database file
        """
        # Download or use existing assemblies
        download_directory = self.downloads_directory
        if self.downloads_directory is None:
            download_directory = self.download_species()
        
        # Find all genome assembly files
        input_files = self.find_input_files(download_directory)
        
        # Filter out mis-labeled assemblies using MASH
        filtered_input_files = self.remove_species_mismatch(input_files, self.species)
        
        # Process each Abricate database
        for ab_database in self.abricate_database:
            # Run Abricate on all assemblies
            files_to_amr_results = self.amr_for_input_files(filtered_input_files, ab_database)
            
            # Aggregate gene counts across all assemblies
            gene_to_freq = self.aggregate_amr_results(files_to_amr_results)
            
            # Write to database file
            SpeciesDatabase(self.output_file, self.species, ab_database ).output_genes_to_freq_file(gene_to_freq)
        
    def aggregate_amr_results(self, files_to_amr_results):
        """
        Aggregate AMR results across multiple assemblies.
        
        Counts how many assemblies contain each gene. A gene appearing
        multiple times in one assembly is counted only once.
        
        Args:
            files_to_amr_results (dict): Map of file paths to AMR result lists
            
        Returns:
            dict: Map of gene names to occurrence counts
        """
        gene_to_freq = {}
        
        for amr_results in files_to_amr_results.values():
            for amr_result in amr_results:
                if amr_result.gene in gene_to_freq:
                    # Gene already seen, increment count
                    gene_to_freq[amr_result.gene] += 1
                else:
                    # First occurrence of this gene
                    gene_to_freq[amr_result.gene] = 1
        
        return gene_to_freq

    def download_species(self):
        """
        Download genome assemblies from NCBI for the target species.
        
        Uses ncbi-genome-download to fetch all assemblies matching
        the specified criteria.
        
        Returns:
            str: Path to download directory
        """
        # Create temporary download directory
        download_directory = str(mkdtemp(dir=self.output_directory))
        self.directories_to_cleanup.append(download_directory)

        # Build ncbi-genome-download command
        cmd = " ".join(
            [
                "ncbi-genome-download",
                "-o",
                download_directory,
                "--genera",
                '"' + self.species + '"',
                "--parallel",
                str(self.threads),
                "--assembly-level",
                self.assembly_level,
                "-R",
                self.refseq_category,
                "-F",
                "fasta",
                "bacteria",
            ]
        )
        if self.verbose:
            print("Download genomes from NCBI:\t"+ cmd)
        subprocess.check_output(cmd, shell=True)
        
        return download_directory
        
    def find_input_files(self, download_directory):
        """
        Find all genome assembly FASTA files in download directory.
        
        Recursively searches for files ending with "genomic.fna.gz".
        
        Args:
            download_directory (str): Root directory to search
            
        Returns:
            list: Paths to all genome assembly files
        """
        input_files = []
        for root, dirs, files in os.walk(download_directory):
            for file in files:
                if file.endswith("genomic.fna.gz"):
                    input_files.append(os.path.join(root, file))
        return input_files
        
    def remove_species_mismatch(self, input_files, species):
        """
        Filter assemblies by verifying species classification with MASH.
        
        Compares each assembly against reference database to ensure it
        actually belongs to the target species. Removes mis-labeled assemblies.
        
        Args:
            input_files (list): List of genome assembly paths
            species (str): Expected species name
            
        Returns:
            list: Filtered list of assemblies matching target species
        """
        filtered_input_files = []
        
        for f in input_files:
            # Identify species using MASH
            mash_species = MashSpecies(f, self.mash_database, self.verbose, minimum_distance = self.minimum_distance).get_species()
            
            if mash_species == species:
                # Species matches expected
                if self.verbose:
                    print('Species match for file ' + str(f) + " got " + mash_species)
                filtered_input_files.append(f)
            else:
                # Species mismatch or no match found
                if self.verbose:
                    if mash_species is not None:
                        print('Species mismatch for file ' + str(f) + ", expected " + species + " but got " + mash_species)
                    else:
                        print('Couldnt find any species for file ' + str(f) + ", expected " + species)
                
        return filtered_input_files
        
    def amr_for_input_files(self, input_files, database):
        """
        Run Abricate on all input assemblies.
        
        Args:
            input_files (list): List of genome assembly paths
            database (str): Abricate database name
            
        Returns:
            dict: Map of file paths to lists of AMR results
        """
        files_to_amr_results = {}
        
        for f in input_files:
            # Run Abricate and parse results
            amr = AbricateAmrResults(f, database, self.min_coverage, self.min_identity, self.threads, self.verbose ).get_amr_results()
            files_to_amr_results[f] = amr
        
        return files_to_amr_results
        
    def __del__(self):
        """
        Cleanup temporary directories unless debug mode is enabled.
        """
        if not self.debug:
            for d in self.directories_to_cleanup:
                if os.path.exists(d):
                    shutil.rmtree(d)
                    
                    
