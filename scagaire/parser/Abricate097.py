"""
Abricate097 - Parser for Abricate version 0.9.7 output

Parses AMR gene predictions from Abricate version 0.9.7 format.
This is a legacy format; current versions use Abricate098 format.
"""

import csv
import re
import os
from tempfile import mkstemp
from scagaire.AbricateResult097 import AbricateResult097
from scagaire.parser.AmrParser import AmrParser

class Abricate097(AmrParser):
    """
    Parser for Abricate 0.9.7 format.
    
    Expected columns:
    #FILE, SEQUENCE, START, END, GENE, COVERAGE, COVERAGE_MAP, GAPS,
    %COVERAGE, %IDENTITY, DATABASE, ACCESSION, PRODUCT
    
    Attributes:
        input_file (str): Path to Abricate output file
        verbose (bool): Enable verbose output
        minimum_num_columns (int): Expected column count (13)
        default_header (list): Expected header columns
        header (list): Actual header from file
        column_to_variable_mapping (dict): Column name to attribute mapping
        results (list): Parsed AbricateResult097 objects
    """
    
    def __init__(self, input_file, verbose):
        """
        Initialize Abricate 0.9.7 parser.
        
        Args:
            input_file (str): Path to Abricate output file
            verbose (bool): Enable verbose output
        """
        self.input_file = input_file
        self.verbose = verbose

        self.minimum_num_columns = 13
        self.default_header = [ '#FILE', 'SEQUENCE', 'START', 'END', 'GENE', 'COVERAGE', 'COVERAGE_MAP', 'GAPS', '%COVERAGE', '%IDENTITY', 'DATABASE', 'ACCESSION', 'PRODUCT']
        self.header = self.default_header
        
        # Map column names to result object attributes
        self.column_to_variable_mapping = {
            '#FILE': 'file', 
            'SEQUENCE': 'sequence', 
            'START': 'start', 
            'END': 'end', 
            'GENE': 'gene', 
            'COVERAGE': 'coverage', 
            'COVERAGE_MAP': 'coverage_map', 
            'GAPS': 'gaps', 
            '%COVERAGE': 'perc_coverage', 
            '%IDENTITY': 'perc_identity', 
            'DATABASE': 'database', 
            'ACCESSION': 'accession', 
            'PRODUCT': 'product'
        }
        
        # Parse file and populate results
        self.results = self.populate_results()
        
    def populate_results(self):
        """
        Parse file and create result objects.
        
        Reads file, validates header, and creates AbricateResult097
        objects for each result line.
        
        Returns:
            list: List of AbricateResult097 objects
        """
        file_contents = self.read_file_multi_delimiters()
        self.header = self.get_header(file_contents)
        
        abricate_results = []
        
        for row in file_contents:
            # Skip incomplete rows
            if len(row)< self.minimum_num_columns:
                continue
            
            # Create result object
            ab_result = AbricateResult097(header = self.default_header)
            
            # Map columns to object attributes
            for index, value in enumerate(row):
                if self.header[index] in self.column_to_variable_mapping:
                    variable_name = self.column_to_variable_mapping[self.header[index]]
                    setattr(ab_result, variable_name, value)
                else:
                    # Unknown column, skip
                    continue
            
            abricate_results.append(ab_result)
        
        return abricate_results
        
    def __str__(self):
        """
        Format all results as multi-line string.
        
        Returns:
            str: All results, one per line
        """
        return "\n".join([str(r) for r in self.results])
            

                