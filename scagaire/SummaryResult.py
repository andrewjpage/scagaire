"""
SummaryResult - Data class for aggregated gene statistics

Represents summary statistics for a single gene, including the gene name
and the number of times it appears in the filtered results.
"""

class SummaryResult:
    """
    Summary statistics for a single AMR gene.
    
    Attributes:
        gene_name (str): Name of the AMR gene
        occurances (int): Number of times gene appears in results
    """
    
    def __init__(self, gene_name, occurances):
        """
        Initialize summary result.
        
        Args:
            gene_name (str): Name of the AMR gene
            occurances (int): Number of occurrences
        """
        self.gene_name = gene_name
        self.occurances = occurances
        
    def __str__(self):
        """
        Format as tab-delimited string.
        
        Returns:
            str: "gene_name\toccurances"
        """
        return "\t".join([self.gene_name, str(self.occurances )])
        