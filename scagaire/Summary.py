"""
Summary - Aggregate AMR results by gene name

This module aggregates AMR results by gene name, counting how many times
each gene appears in the results. Used for generating summary statistics.
"""

from scagaire.SummaryResult import SummaryResult

class Summary:
    """
    Aggregate AMR results by gene name.
    
    Counts occurrences of each gene in the results and creates
    summary statistics.
    
    Attributes:
        results (list): List of AMR result objects
        verbose (bool): Enable verbose output
    """
    
    def __init__(self, results, verbose):
        """
        Initialize summary aggregator.
        
        Args:
            results (list): List of AMR result objects
            verbose (bool): Enable verbose output
        """
        self.results = results
        self.verbose = verbose

    def aggregate_results(self):
        """
        Aggregate results by gene name, counting occurrences.
        
        Creates a dictionary mapping gene names to SummaryResult objects
        that track the total number of times each gene appears.
        
        Returns:
            dict: Map of gene name to SummaryResult object
        """
        genename_to_summary = {}
        
        for r in self.results:
            if r.gene in genename_to_summary:
                # Gene already seen, increment count
                genename_to_summary[r.gene].occurances += 1
            else:
                # First occurrence of this gene
                genename_to_summary[r.gene] = SummaryResult(r.gene, 1)
        
        return genename_to_summary 
