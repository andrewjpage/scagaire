"""
AmrParser - Base class for AMR result parsers

This module provides the base class for parsing various AMR (antimicrobial resistance)
result file formats. Subclasses implement specific parsers for different tools
(Abricate, StarAMR, RGI, etc.).
"""

import csv
import re
import os
from tempfile import mkstemp

class AmrParser:
    """
    Base class for parsing AMR result files.
    
    Provides common functionality for reading delimited files and validating
    headers. Subclasses implement format-specific parsing logic.
    
    Attributes:
        input_file (str): Path to AMR results file
        verbose (bool): Enable verbose output
        minimum_num_columns (int): Minimum expected columns
        default_header (list): Expected header columns for this format
        column_to_variable_mapping (dict): Map column names to object attributes
    """
    
    def __init__(self, input_file, verbose):
        """
        Initialize the parser.
        
        Args:
            input_file (str): Path to AMR results file
            verbose (bool): Enable verbose output
        """
        self.input_file = input_file
        self.verbose = verbose
        self.minimum_num_columns = 1
        self.default_header = [ ]
        self.column_to_variable_mapping = {}

    def is_valid(self):
        """
        Check if file matches expected format by validating header.
        
        Returns:
            bool: True if header matches default_header, False otherwise
        """
        for i,h in enumerate(self.header):
            if h != self.default_header[i]:
                return False
        
        return True
        
    def get_header(self, file_contents):
        """
        Extract and remove header line from file contents.
        
        Args:
            file_contents (list): List of file rows
            
        Returns:
            list: Header row (first row, now removed from file_contents)
        """
        return file_contents.pop(0)
        
    def read_file_multi_delimiters(self):
        """
        Read CSV/TSV file with auto-detected delimiter.
        
        Uses Python's csv.Sniffer to automatically detect whether file
        uses comma or tab delimiters.
        
        Returns:
            list: List of rows, where each row is a list of column values
        """
        file_contents = []
        with open(self.input_file, newline='') as csvfile:
            # Auto-detect delimiter (comma or tab)
            dialect = csv.Sniffer().sniff(csvfile.readline(), [',','\t'])
            csvfile.seek(0)
            bnreader = csv.reader(csvfile, dialect)
            
            # Read all rows
            for row in bnreader:
                file_contents.append(row)

        return file_contents
                