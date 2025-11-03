"""
MashSpecies - Species identification using MASH

This module uses MASH (MinHash alignment) to verify the species classification
of genome assemblies by comparing them against a reference database.
"""

import os
import subprocess

class MashSpecies:
    """
    Verify species classification using MASH distance.
    
    Compares genome assemblies against a reference database using MASH
    to identify the closest matching species. Used to filter out
    mis-labeled assemblies.
    
    Attributes:
        input_file (str): Path to genome assembly file
        database (str): Path to MASH reference database (.msh)
        minimum_distance (float): Maximum distance threshold (0-1)
        verbose (bool): Enable verbose output
    """
    
    def __init__(self, input_file, database, verbose, minimum_distance = 0.1):
        """
        Initialize MASH species identifier.
        
        Args:
            input_file (str): Path to genome assembly
            database (str): Path to MASH reference database
            verbose (bool): Enable verbose output
            minimum_distance (float): Maximum distance for match (default 0.1)
        """
        self.input_file = input_file
        self.database = database
        self.minimum_distance = minimum_distance
        self.verbose = verbose
        
    def get_species(self):
        """
        Identify species of genome assembly.
        
        Runs MASH dist to compare assembly against reference database,
        sorts by distance, and returns closest matching species.
        
        Returns:
            str: Species name ("Genus species") or None if no match
        """
        # Run MASH dist, filter by distance, sort, take top match
        cmd = " ".join(['mash', 'dist','-d', str(self.minimum_distance), self.database, self.input_file, '|', 'sort','-k', '3', '|', 'head', '-n', '1'])
        if self.verbose:
            print("Run Mash against RefSeq reference genomes\t"+ cmd)
        mash_output = subprocess.check_output(cmd, shell=True)
        
        if len(mash_output) > 0:
            # Parse species from sketch path: ".../Genus/species/..."
            sketch_match = mash_output.decode().split('/')
            species = sketch_match[0] + " " + sketch_match[1]
            return species
        
        return None
        