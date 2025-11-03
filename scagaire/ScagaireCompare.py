"""
ScagaireCompare - Compare AMR gene profiles between species

This module compares the AMR gene profiles of two bacterial species,
identifying genes shared between them and their occurrence frequencies.
"""

import os
import pkg_resources
from scagaire.parser.SpeciesToGenes  import SpeciesToGenes
from scagaire.Config import Config

class ScagaireCompare:
    """
    Compare AMR gene profiles between two species.
    
    Identifies genes that appear in both species and reports their
    occurrence frequencies in each.
    
    Attributes:
        verbose (bool): Enable verbose output
        debug (bool): Enable debug mode
        species1 (str): First species name
        species2 (str): Second species name
        database_filter (str): Database name filter
        database (str): Path to species-to-genes database
        config_file (str): Path to configuration file
    """
    
    def __init__(self, options):
        """
        Initialize the comparison tool.
        
        Args:
            options: Object with attributes:
                - verbose: Enable verbose output
                - debug: Enable debug mode
                - species1: First species name
                - species2: Second species name
                - database_filter: Database filter
                - database_file: Database path (None for bundled)
        """
        self.verbose  = options.verbose
        self.debug    = options.debug
        self.verbose = options.verbose
        
        self.species1 = options.species1
        self.species2 = options.species2
        self.database_filter = options.database_filter
        
        # Use bundled database if none specified
        self.database = options.database_file
        
        if options.database_file is None:
            self.database = str(pkg_resources.resource_filename( __name__, 'data/species_to_genes.tsv'))
    
        self.config_file = os.path.join(str(pkg_resources.resource_filename( __name__, 'data/')), 'config.json')
    

    def compare(self):
        """
        Compare AMR profiles and print shared genes.
        
        Finds genes present in both species and outputs:
        gene_name\tspecies1\tcount1\tspecies2\tcount2
        
        Only includes genes found in both species.
        """
        # Load gene lists for both species
        sg = SpeciesToGenes(self.database, self.verbose)
        species1_species_to_genes = sg.filter_by_species(self.species1, self.database_filter)
        species2_species_to_genes = sg.filter_by_species(self.species2, self.database_filter)
        
        # Extract gene names
        species1_gene_names = [s.gene for s in species1_species_to_genes]
        species2_gene_names = [s.gene for s in species2_species_to_genes]
        
        # Filter to shared genes only
        filtered_species1_species_to_genes = [s for s in species1_species_to_genes if s.gene in species2_gene_names]
        filtered_species2_species_to_genes = [s for s in species2_species_to_genes if s.gene in species1_gene_names]
        
        # Print comparison for each shared gene
        for s in filtered_species1_species_to_genes:
            matching_species = [s2 for s2 in filtered_species2_species_to_genes if s.gene == s2.gene]
            
            print("\t".join([s.gene, s.species, str(s.occurances), matching_species[0].species, str(matching_species[0].occurances)]))
            
