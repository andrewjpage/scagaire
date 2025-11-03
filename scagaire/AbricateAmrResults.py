"""
AbricateAmrResults - Run Abricate and parse results

This module executes Abricate to predict AMR genes in genome assemblies
and parses the output results.
"""

import os
import subprocess
from scagaire.parser.Abricate098 import Abricate098
from tempfile import mkstemp

class AbricateAmrResults:
    """
    Execute Abricate and parse AMR gene predictions.
    
    Runs Abricate tool with specified parameters to predict AMR genes
    in a genome assembly, then parses the results.
    
    Attributes:
        input_file (str): Path to genome assembly file
        database_name (str): Abricate database to use (e.g., 'ncbi', 'card')
        min_coverage (int): Minimum percentage coverage threshold
        min_identity (int): Minimum percentage identity threshold
        threads (int): Number of CPU threads to use
        verbose (bool): Enable verbose output
    """
    
    def __init__(self, input_file, database_name, min_coverage, min_identity, threads, verbose):
        """
        Initialize Abricate runner.
        
        Args:
            input_file (str): Path to genome assembly
            database_name (str): Abricate database name
            min_coverage (int): Minimum coverage percentage (0-100)
            min_identity (int): Minimum identity percentage (0-100)
            threads (int): Number of threads
            verbose (bool): Enable verbose output
        """
        self.input_file = input_file
        self.database_name = database_name
        self.min_coverage = min_coverage
        self.min_identity = min_identity
        self.threads = threads
        
        self.verbose = verbose
        
    def get_amr_results(self):
        """
        Run Abricate and return parsed results.
        
        Executes Abricate with configured parameters, writes output to
        temporary file, parses results, and cleans up temp file.
        
        Returns:
            list: List of AMR result objects
        """
        # Create temporary file for Abricate output
        fd, abricate_output = mkstemp()
        
        # Build and execute Abricate command
        cmd = " ".join(['abricate', '--db', self.database_name, '--minid', str(self.min_identity), '--mincov', str(self.min_coverage),'--threads', str(self.threads), self.input_file , '>', abricate_output])
        if self.verbose:
            print("Run Abricate to find AMR genes\t"+ cmd)
        subprocess.check_output(cmd, shell=True)
        
        # Parse results
        ab_parser = Abricate098(abricate_output, self.verbose)
        
        # Clean up temporary file
        os.close(fd)
        os.remove(abricate_output)
        
        if self.verbose:
            print(str(ab_parser))
        
        return ab_parser.results
        