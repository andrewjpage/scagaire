"""
AbricateResult097 - Data class for Abricate 0.9.7 results

Represents a single AMR gene prediction from Abricate version 0.9.7.
This is a legacy format; version 0.9.8+ uses a different column structure.
"""

class AbricateResult097:
    """
    Single AMR gene prediction from Abricate 0.9.7.
    
    Attributes:
        file (str): Input filename
        sequence (str): Sequence/contig name
        start (str): Start position
        end (str): End position
        gene (str): Gene name
        coverage (str): Coverage value
        coverage_map (str): Coverage map
        gaps (str): Gaps in alignment
        perc_coverage (str): Percentage coverage
        perc_identity (str): Percentage identity
        database (str): AMR database used
        accession (str): Database accession
        product (str): Gene product description
        header (list): Column headers
        delimiter (str): Output delimiter (tab)
    """
    
    def __init__(self, header = []):
        """
        Initialize Abricate 0.9.7 result object.
        
        Args:
            header (list): Column header names
        """
        self.file          = None
        self.sequence      = None
        self.start         = None
        self.end           = None
        self.gene          = None
        self.coverage      = None
        self.coverage_map  = None
        self.gaps          = None
        self.perc_coverage = None
        self.perc_identity = None
        self.database      = None
        self.accession     = None
        self.product       = None
        
        self.header = header
        self.delimiter = "\t"

    def __str__(self):
        """
        Format as tab-delimited string matching Abricate format.
        
        Returns:
            str: Tab-delimited result line
        """
        return (self.delimiter).join([self.file, self.sequence, self.start, self.end, self.gene, self.coverage, self.coverage_map, self.gaps, self.perc_coverage, self.perc_identity, self.database, self.accession, self.product
        ])
