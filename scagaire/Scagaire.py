"""
Scagaire - Filter AMR results by bacterial species

This module provides the main Scagaire class that filters antimicrobial resistance (AMR) 
gene predictions by bacterial species. It takes AMR results from tools like Abricate, 
StarAMR, or RGI and filters them to show only genes found in specified pathogenic species.
"""

import os
import sys
import pkg_resources
from scagaire.FilterResults import FilterResults
from scagaire.Config import Config
from scagaire.parser.SpeciesToGenes import SpeciesToGenes
from scagaire.Summary import Summary

class Scagaire:
    """
    Main class for filtering AMR results by bacterial species.
    
    This class coordinates the filtering process by:
    1. Loading the species-to-genes database
    2. Parsing and validating input species names
    3. Filtering AMR results based on species
    4. Generating output files with filtered results
    
    Attributes:
        verbose (bool): Enable verbose output
        input_file (str): Path to input AMR results file
        database_file (str): Path to species-to-genes database
        database_name (str): Name of the AMR database used
        minimum_occurances (int): Minimum gene occurrences threshold
        output_file (str): Path to output file (or None for STDOUT)
        results_type (str): Format of input results (abricate/rgi/staramr)
        summary_file (str): Path to summary output file
        overwrite_files (bool): Whether to overwrite existing output files
        species (list): List of species names to filter by
        config_file (str): Path to configuration JSON file
    """
    
    def __init__(self, options):
        """
        Initialize the Scagaire filtering system.
        
        Args:
            options: Object containing command-line options with attributes:
                - verbose: Enable verbose output
                - input_file: Path to AMR results file
                - database_file: Path to species database (None for bundled)
                - database_name: Name of AMR database
                - minimum_occurances: Minimum gene occurrence threshold
                - output_file: Output file path (None for STDOUT)
                - results_type: Input format type
                - summary_file: Summary output file path
                - overwrite_files: Whether to overwrite existing files
                - species: Species name(s) to filter by
        """
        self.verbose = options.verbose
        self.input_file = options.input_file
        self.database_file = options.database_file
        self.database_name = options.database_name
        self.minimum_occurances = options.minimum_occurances
        self.output_file = options.output_file
        self.results_type = options.results_type
        self.summary_file = options.summary_file
        self.overwrite_files = options.overwrite_files
        
        # Use bundled database if none specified
        if self.database_file is None:
            self.database_file = str(pkg_resources.resource_filename( __name__, 'data/species_to_genes.tsv'))
            
        # Load configuration file with taxon categories
        self.config_file = os.path.join(str(pkg_resources.resource_filename( __name__, 'data/')), 'config.json')
        
        # Parse species string into list, expanding categories
        self.species = self.parse_species(options.species)
        
        # Handle existing output files according to overwrite flag
        if self.overwrite_files:
            # Remove existing files if overwrite is enabled
            if self.output_file is not None and os.path.exists(self.output_file):
                os.remove(self.output_file)
            if self.summary_file is not None and os.path.exists(self.summary_file):
                os.remove(self.summary_file)
        else:
            # Exit with error if files exist and overwrite is disabled
            if self.output_file is not None and os.path.exists(self.output_file):
                sys.exit("Output file already exists, please choose another filename.")
            if self.summary_file is not None and os.path.exists(self.summary_file):
                sys.exit("Summary file already exists, please choose another filename.")
    
    def parse_species(self, species_str):
        """
        Parse species string and expand taxon categories.
        
        Accepts multiple formats:
        - Single species: "Salmonella enterica"
        - Multiple species: "Salmonella enterica,Streptococcus pneumoniae"
        - Category names: "skin" (expands to all skin-associated species)
        
        Args:
            species_str (str): Comma-separated species names or categories
            
        Returns:
            list: List of species names with categories expanded
        """
        config = Config(self.config_file, self.verbose)
        split_species_str = species_str.split(",")
        output_species = []
        
        for s in split_species_str:
            # Check if this is a taxon category (e.g., "skin", "respiratory")
            if s in config.taxon_categories():
                # Expand category to all species it contains
                for c in config.taxon_categories()[s]:
                    output_species.append(c)
            else:
                # Use species name directly
                output_species.append(s)
        
        return output_species
    
    def output_summary(self, results, species):
        """
        Write summary statistics to the summary file.
        
        Aggregates filtered results by gene name and counts occurrences,
        then writes one line per gene showing species, gene name, and count.
        
        Args:
            results (list): List of filtered AMR result objects
            species (str): Species name for this set of results
        """
        # Aggregate results by gene name
        s = Summary(results, self.verbose)
        output_gene_occurances = [str(g) for g in s.aggregate_results().values()]
        
        # Append summary to output file
        with open(self.summary_file, "a+") as output_fh:
            if len(results) > 0:
                # Write one line per gene with species, gene, and count
                for r in output_gene_occurances:
                    output_fh.write(species + "\t" + r + "\n")
            else:
                # Write "no_results" if no genes found for this species
                output_fh.write(species + "\t" + "no_results\t0" + "\n")

    def run(self):
        """
        Execute the main filtering workflow.
        
        Process flow:
        1. Initialize FilterResults with database and parameters
        2. For each species in the list:
           a. Verify species exists in database
           b. Filter AMR results by species
           c. Output summary statistics
           d. Write filtered results to output file or STDOUT
        
        Results are written in the same format as the input, with only
        genes found in the specified species retained.
        """
        # Initialize the filtering engine
        filter_results =  FilterResults(self.input_file, self.database_file, self.minimum_occurances, self.results_type, self.database_name, self.verbose)
        
        # Load species database for validation
        sg = SpeciesToGenes(self.database_file, self.verbose)
        
        # Process each species separately
        for spec in self.species:
            # Validate that species exists in database
            if spec not in sg.all_species():
                print("Error: Species not found in database so nothing to do")
                return

            # Filter results for this species
            results = filter_results.filter_by_species(spec)
            
            # Generate summary statistics
            self.output_summary(results, spec)
            
            # Format output: convert results to strings
            output_content = "\n".join([str(r) for r in results])
            
            # Generate header line
            header = ""
            if len(results) > 0:
                header = "\t".join(results[0].header)
            else:
                header = "No results"
            
            # Write to file or STDOUT
            if self.output_file != None:
                with open(self.output_file, "a+") as output_fh:
                    # Add species separator if processing multiple species
                    if len(self.species) > 1:
                        output_fh.write("Results for species:\t" + str(spec) + "\n=======================\n")
                    output_fh.write(header+ "\n")
                    output_fh.write(output_content + "\n")
            else:
                # Print to screen if no output file specified
                print("Results for species:\t" + str(spec) + "\n=======================")
                print(header)
                print(output_content)
        