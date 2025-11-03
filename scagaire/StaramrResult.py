"""
StaramrResult - Data class for StarAMR results

Represents a single AMR gene prediction from StarAMR tool.
StarAMR uses ResFinder database to scan microbial genomes for AMR genes.
"""

class StaramrResult:
    """
    Single AMR gene prediction from StarAMR.
    
    Attributes:
        file (str): Input filename
        sequence (str): Sequence/contig name
        start (str): Start position
        end (str): End position
        gene (str): Gene name
        coverage (str): Coverage value
        perc_coverage (str): Percentage coverage
        perc_identity (str): Percentage identity
        accession (str): Database accession
        resistance (str): Resistance annotation
        header (list): Column headers
        delimiter (str): Output delimiter (tab)
    """
    
    def __init__(self, header = []):
        """
        Initialize StarAMR result object.
        
        Args:
            header (list): Column header names
        """
        self.file          = None
        self.sequence      = None
        self.start         = None
        self.end           = None
        self.gene          = None
        self.coverage      = None
        self.perc_coverage = None
        self.perc_identity = None
        self.accession     = None
        self.resistance    = None
        
        self.header = header
        self.delimiter = "\t"

    def __str__(self):
        """
        Format as tab-delimited string matching StarAMR format.
        
        Returns:
            str: Tab-delimited result line
        """
        return (self.delimiter).join([self.file, self.gene, self.resistance, self.perc_identity, self.perc_coverage, self.coverage, self.sequence, self.start, self.end, self.accession ])
