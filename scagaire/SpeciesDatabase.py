"""
SpeciesDatabase - Write species-gene associations to database file

This module handles writing species-to-gene mappings to the database file,
including metadata like occurrence counts and timestamps.
"""

import os
import sys
from datetime import datetime

class SpeciesDatabase:
    """
    Write species-gene associations to database file.
    
    Handles formatting and writing gene occurrence data to the
    species-to-genes database file.
    
    Attributes:
        output_file (str): Path to output database file
        species (str): Bacterial species name
        database (str): AMR database name
        fixed_time (str): Fixed timestamp (for testing)
        delimiter (str): Field delimiter (tab)
    """
    
    def __init__(self, output_file, species, database, fixed_time = None):
        """
        Initialize database writer.
        
        Args:
            output_file (str): Path to output file
            species (str): Species name
            database (str): AMR database name
            fixed_time (str): Fixed timestamp string (optional, for testing)
        """
        self.species    = species
        self.output_file = output_file
        self.database = database
        self.fixed_time = fixed_time
        self.delimiter  = "\t"

    def output_genes_to_freq_file(self, gene_to_freq):
        """
        Write gene occurrence frequencies to database file.
        
        Format: species\tgene\tcount\tsource\tdatabase\tmethod\tdate
        Example: Campylobacter jejuni\tblaOXA-785\t6\tabricate\tncbi\tauto\t20191008
        
        Args:
            gene_to_freq (dict): Map of gene names to occurrence counts
        """
        with open(self.output_file, "a+") as out_fh:
            for gene, freq in gene_to_freq.items():
                # Build output line with metadata
                gene_results = [self.species, gene, str(freq), 'abricate' + "\t"+ self.database + "\t" +'auto']
                
                # Add timestamp (current date or fixed for testing)
                if self.fixed_time is None:
                    gene_results.append(datetime.today().strftime('%Y%m%d'))
                else:
                    gene_results.append(self.fixed_time)
                
                # Write tab-delimited line
                out_fh.write( self.delimiter.join([str(g) for g in gene_results]) + "\n")
                