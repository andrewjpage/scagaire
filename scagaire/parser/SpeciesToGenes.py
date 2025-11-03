"""
SpeciesToGenes - Parser and manager for species-to-genes database

Parses and provides query interface for the species-to-genes database file.
This database maps bacterial species to AMR genes with occurrence counts,
enabling species-specific filtering of AMR predictions.
"""

import csv
import re
import os
from tempfile import mkstemp
from scagaire.SpeciesGenes import SpeciesGenes

class SpeciesToGenes:
    """
    Parser and query interface for species-to-genes database.
    
    Loads the TSV database mapping species names to AMR genes with
    occurrence counts, and provides methods to query and filter the data.
    
    Database format: species\tgene\tcount\tsource\tdatabase\tmethod\tdate
    
    Attributes:
        input_file (str): Path to database file
        verbose (bool): Enable verbose output
        minimum_num_columns (int): Minimum columns required (3)
        species_to_genes (list): List of SpeciesGenes objects
    """
    
    def __init__(self, input_file, verbose):
        """
        Initialize database parser.
        
        Args:
            input_file (str): Path to database TSV file
            verbose (bool): Enable verbose output
        """
        self.input_file = input_file
        self.verbose = verbose
        self.minimum_num_columns = 3

        # Parse database file
        self.species_to_genes = self.populate()
        
    def read_file_multi_delimiters(self):
        """
        Read database file with auto-detected delimiter.
        
        Returns:
            list: List of data rows (header excluded)
        """
        file_contents = []
        with open(self.input_file, newline='') as csvfile:
            # Auto-detect delimiter
            dialect = csv.Sniffer().sniff(csvfile.readline(), [',','\t'])
            csvfile.seek(0)
            bnreader = csv.reader(csvfile, dialect)
            
            # Skip header
            header  = next(bnreader)
            
            # Read data rows
            for row in bnreader:
                file_contents.append(row)

        return file_contents
                
    def populate(self):
        """
        Parse database file into SpeciesGenes objects.
        
        Returns:
            list: List of SpeciesGenes objects
        """
        file_contents = self.read_file_multi_delimiters()
        results = []
        
        for row in file_contents:
            # Skip incomplete rows
            if len(row)< self.minimum_num_columns:
                continue
            
            # Create SpeciesGenes object
            # Format: species, gene, count, database_name (column 4)
            results.append(SpeciesGenes(str(row[0]), str(row[1]), int(row[2]), str(row[4])))
        
        return results
    
    def all_species(self):
        """
        Get list of all species in database.
        
        Returns:
            list: Sorted unique species names
        """
        return sorted(list(set([s.species for s in self.species_to_genes])))
        
    def all_databases(self):
        """
        Get list of all database names in database.
        
        Returns:
            list: Sorted unique database names
        """
        return sorted(list(set([s.database_name for s in self.species_to_genes])))
        
    def all_genes(self):
        """
        Get list of all genes in database.
        
        Returns:
            list: Sorted unique gene names
        """
        return sorted(list(set([s.gene for s in self.species_to_genes])))    
        
    def num_of_all_species(self):
        """
        Count unique species.
        
        Returns:
            int: Number of unique species
        """
        return len(self.all_species())
        
    def num_of_all_databases(self):
        """
        Count unique databases.
        
        Returns:
            int: Number of unique databases
        """
        return len(self.all_databases())
        
    def num_of_all_genes(self):
        """
        Count unique genes.
        
        Returns:
            int: Number of unique genes
        """
        return len(self.all_genes())
    
    def sum_of_occurances(self):
        """
        Sum all gene occurrence counts.
        
        Returns:
            int: Total of all occurrence counts
        """
        return sum([s.occurances for s in self.species_to_genes])
        
    def species_databases(self, query):
        """
        Get databases containing data for a species.
        
        Args:
            query (str): Species name
            
        Returns:
            list: Sorted list of database names
        """
        specific_species = [s for s in self.species_to_genes if s.species == query]
        databases = sorted(list(set([s.database_name for s in specific_species])))
        return databases
        
    def filter_by_species(self, query, database_name):
        """
        Filter entries by species and database.
        
        Args:
            query (str): Species name
            database_name (str): Database name filter
            
        Returns:
            list: SpeciesGenes objects matching criteria
        """
        return [s for s in self.species_to_genes if s.species == query and s.database_name == database_name]
            
            