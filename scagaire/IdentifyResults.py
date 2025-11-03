"""
IdentifyResults - Auto-detect and parse AMR result formats

This module automatically identifies the format of AMR results files and returns
parsed results. It supports multiple AMR prediction tools including Abricate
(versions 0.9.7 and 0.9.8+), StarAMR, and RGI (CARD).
"""

from scagaire.parser.Abricate098 import Abricate098
from scagaire.parser.Abricate097 import Abricate097
from scagaire.parser.Staramr import Staramr
from scagaire.parser.Rgi import Rgi

class IdentifyResults:
    """
    Auto-detect AMR results format and parse accordingly.
    
    Tries each parser in order until finding a valid match:
    1. Abricate 0.9.8+ format (current)
    2. Abricate 0.9.7 format (legacy)
    3. StarAMR format
    4. RGI (CARD) format
    
    Attributes:
        input_file (str): Path to AMR results file
        results_type (str): Format hint (None for auto-detect)
        verbose (bool): Enable verbose output
    """
    
    def __init__(self, input_file, results_type, verbose):
        """
        Initialize the format detector.
        
        Args:
            input_file (str): Path to AMR results file
            results_type (str): Format hint ('abricate', 'staramr', 'rgi', or None)
            verbose (bool): Enable verbose output
        """
        self.input_file = input_file
        self.results_type = results_type
        self.verbose = verbose

    def get_results(self):
        """
        Auto-detect format and return parsed AMR results.
        
        Tries each parser sequentially:
        1. Abricate 0.9.8+ (checks header validity)
        2. Abricate 0.9.7 (checks header validity or if type explicitly set)
        3. StarAMR (checks header validity or if type explicitly set)
        4. RGI (checks header validity or if type explicitly set)
        
        Returns:
            list: List of AMR result objects, or empty list if no valid format found
        """
        # Try Abricate 0.9.8+ format first (most common)
        a = Abricate098(self.input_file, self.verbose)
        if a.is_valid():
            return a.results
        
        # Try Abricate 0.9.7 format (legacy)
        a7 = Abricate097(self.input_file, self.verbose)
        if a7.is_valid() or self.results_type == 'abricate':
            return a7.results
        
        # Try StarAMR format
        s = Staramr(self.input_file, self.verbose)
        if s.is_valid() or self.results_type == 'staramr':
            return s.results
        
        # Try RGI (CARD) format
        r = Rgi(self.input_file, self.verbose)
        if r.is_valid() or self.results_type == 'rgi':
            return r.results

        # No valid format found
        return []
                  