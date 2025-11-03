"""
ScagaireSpecies - List available species in database

This module provides functionality to list and display information about
bacterial species available in the Scagaire database.
"""

import os
import pkg_resources
from scagaire.parser.SpeciesToGenes  import SpeciesToGenes
from scagaire.Config import Config

class ScagaireSpecies:
    """
    List and display available species in database.
    
    Provides three display modes:
    - Simple: List of species names
    - Detailed: Species with database availability matrix
    - Overview: Summary statistics
    
    Attributes:
        verbose (bool): Enable verbose output
        database_filename (str): Database filename
        detailed (bool): Show detailed matrix view
        overview (bool): Show summary statistics
        database (str): Full path to database file
        config_file (str): Path to configuration file
    """
    
    def __init__(self, verbose, detailed, overview, database_filename = 'species_to_genes.tsv'):
        """
        Initialize species listing tool.
        
        Args:
            verbose (bool): Enable verbose output
            detailed (bool): Show detailed database matrix
            overview (bool): Show summary statistics
            database_filename (str): Database filename (default: bundled)
        """
        self.verbose = verbose
        self.database_filename = database_filename
        self.detailed = detailed
        self.overview = overview
        
        # Use bundled database
        self.database = os.path.join(str(pkg_resources.resource_filename( __name__, 'data/')), self.database_filename)
    
        self.config_file = os.path.join(str(pkg_resources.resource_filename( __name__, 'data/')), 'config.json')
    
    def print_all(self):
        """
        Print species list in selected format.
        
        Chooses output format based on flags:
        - overview: Summary statistics
        - detailed: Species x Database matrix
        - default: Simple species list
        """
        if self.overview:
            self.print_overview()
        elif self.detailed:
            self.print_detailed()
        else:
            self.print_simple()
        
        
    def print_overview(self):
        """
        Print database overview statistics.
        
        Shows:
        - Number of species
        - Number of databases
        - Number of unique genes
        - Sum of all gene occurrences
        """
        sg = SpeciesToGenes(self.database, self.verbose)
        databases = sorted(sg.all_databases())
        print("No. of species:\t" + str(sg.num_of_all_species()))
        print("No. of databases:\t" + str(sg.num_of_all_databases()))
        print("No. of genes:\t" + str(sg.num_of_all_genes()))
        print("Sum of occurances:\t" + str(sg.sum_of_occurances()))
    
    def print_detailed(self):
        """
        Print detailed species x database matrix.
        
        Shows which databases contain data for each species.
        Format: Species\tDB1\tDB2\t...
        Uses "----" for missing database entries.
        """
        sg = SpeciesToGenes(self.database, self.verbose)
        databases = sorted(sg.all_databases())
        
        # Print header
        print("\t".join(['Species'] + databases))

        # Print each species row
        for species in sorted(sg.all_species()):
            species_dbs = sg.species_databases(species)
            cells = [species]
            for d in databases:
                if d in species_dbs:
                    cells.append(d)
                else:
                    cells.append('----')
            print("\t".join(cells))
            
        
    def print_simple(self):
        """
        Print simple list of species names.
        
        Lists all available species names, followed by
        taxon categories (e.g., "skin", "respiratory").
        """
        sg = SpeciesToGenes(self.database, self.verbose)
        print("\n".join(sorted(sg.all_species())))

        # Also print taxon categories
        c = Config(self.config_file, self.verbose)
        print("\n".join(c.taxon_categories_printable_list()))
