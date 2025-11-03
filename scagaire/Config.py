"""
Config - Configuration file parser

This module loads and parses the configuration JSON file that defines
taxon categories. Categories allow users to specify groups of species
(e.g., "skin", "respiratory") instead of individual species names.
"""

import json

class Config:
    """
    Configuration file parser for taxon categories.
    
    Loads JSON configuration file containing predefined groups of species
    organized by categories (e.g., skin pathogens, respiratory pathogens).
    
    Attributes:
        input_file (str): Path to configuration JSON file
        verbose (bool): Enable verbose output
        configuration (dict): Parsed configuration data
    """
    
    def __init__(self, input_file,  verbose):
        """
        Initialize configuration parser.
        
        Args:
            input_file (str): Path to config JSON file
            verbose (bool): Enable verbose output
        """
        self.input_file = input_file
        self.verbose = verbose
        self.configuration = self.read_contents()

    def read_contents(self):
        """
        Read and parse JSON configuration file.
        
        Returns:
            dict: Parsed configuration data
        """
        data = {}
        with open(self.input_file) as json_file:
            data = json.load(json_file)
        return data

    def taxon_categories(self):
        """
        Get taxon category mappings.
        
        Returns:
            dict: Category names to list of species mappings
        """
        return self.configuration['taxon_categories']
        
    def taxon_categories_printable_list(self):
        """
        Generate human-readable list of taxon categories.
        
        Formats categories with abbreviated genus names for display.
        Example: "Salmonella enterica" -> "S. enterica"
        
        Returns:
            list: Formatted strings showing category and species list
        """
        output = []
        for category, species in self.taxon_categories().items():
            
            # Shorten genus names (Genus species -> G. species)
            shortened_genus_species = []
            for s in sorted(species):
                genus_species = s.split(" ")
                if len(genus_species)>1:
                    # Abbreviate genus: "Escherichia coli" -> "E. coli"
                    shortened_genus_species.append(genus_species[0][0] + ". " + genus_species[1])
                else:
                    # Keep single-word names as-is
                    shortened_genus_species.append(s)
            
            # Format as: "category\t(species1, species2, ...)"
            species_list = ", ".join(shortened_genus_species)
            output.append(category + "\t(" + species_list + ")")
        return output
            
                