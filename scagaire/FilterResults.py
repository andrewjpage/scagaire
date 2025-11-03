"""
FilterResults - Filter AMR results by bacterial species

This module filters antimicrobial resistance gene predictions based on a database
of genes known to occur in specific bacterial species. It takes raw AMR results
and retains only genes that have been observed in the target species.
"""

import csv
import re
import os
from tempfile import mkstemp
from scagaire.IdentifyResults import IdentifyResults
from scagaire.parser.SpeciesToGenes import SpeciesToGenes

class FilterResults:
    """
    Filter AMR gene predictions by bacterial species.
    
    This class coordinates the filtering process by:
    1. Parsing input AMR results from various tools
    2. Loading species-specific gene databases
    3. Filtering results to retain only genes found in target species
    4. Applying minimum occurrence thresholds
    
    Attributes:
        results_filename (str): Path to input AMR results file
        database_filename (str): Path to species-to-genes database
        minimum_occurances (int): Minimum times a gene must occur to be included
        database_name (str): Name of the AMR database (e.g., 'ncbi', 'card')
        results_type (str): Format of input results (auto-detected if None)
        verbose (bool): Enable verbose output
    """
    
    def __init__(self, results_filename, database_filename, minimum_occurances, results_type,  database_name, verbose):
        """
        Initialize the filtering system.
        
        Args:
            results_filename (str): Path to input AMR results file
            database_filename (str): Path to species-to-genes database
            minimum_occurances (int): Minimum gene occurrence threshold
            results_type (str): Input format type (None for auto-detect)
            database_name (str): Name of AMR database used
            verbose (bool): Enable verbose output
        """
        self.results_filename = results_filename
        self.database_filename = database_filename
        self.minimum_occurances = minimum_occurances
        self.database_name = database_name
        self.results_type = results_type
        self.verbose = verbose

    def filter_by_species(self, species):
        """
        Filter AMR results to retain only genes found in specified species.
        
        Process:
        1. Parse all AMR results from input file
        2. Load species-specific gene list from database
        3. Create lookup dictionary of valid genes with occurrence counts
        4. Filter results to retain only genes in the species
        5. Apply minimum occurrence threshold
        
        Args:
            species (str): Species name to filter by (e.g., "Escherichia coli")
            
        Returns:
            list: Filtered list of AMR result objects containing only genes
                  found in the specified species with sufficient occurrences
        """
        # Parse all AMR results from input file (format auto-detected)
        all_results = IdentifyResults(self.results_filename, self.results_type, self.verbose).get_results()
        
        # Load list of genes known to occur in this species
        species_genes = SpeciesToGenes(self.database_filename, self.verbose).filter_by_species(species, self.database_name)
    
        # Create a dictionary for fast gene lookup, filtering by minimum occurrences
        # Key: gene name, Value: number of occurrences in species
        species_genes_to_occurances = { g.gene: g.occurances for g in species_genes if g.occurances >= self.minimum_occurances }
        
        # Filter results to keep only genes in the species-specific dictionary
        filtered_results = [r for r in all_results if r.gene in species_genes_to_occurances]
        
        return filtered_results
        