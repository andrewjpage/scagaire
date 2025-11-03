"""
SpeciesGenes - Data class for species-gene associations

Represents the association between a bacterial species and an AMR gene,
including how many times that gene has been observed in that species.
"""

class SpeciesGenes:
    """
    Association between species and AMR gene.
    
    Attributes:
        species (str): Bacterial species name
        gene (str): AMR gene name
        occurances (int): Number of times observed in species
        database_name (str): AMR database name (e.g., 'ncbi', 'card')
        delimiter (str): Output delimiter (tab)
    """
    
    def __init__(self, species, gene, occurances, database_name):
        """
        Initialize species-gene association.
        
        Args:
            species (str): Bacterial species name
            gene (str): AMR gene name
            occurances (int): Occurrence count
            database_name (str): AMR database name
        """
        self.species    = species
        self.gene       = gene
        self.occurances = occurances
        self.database_name = database_name
        self.delimiter  = "\t"

    def __str__(self):
        """
        Format as tab-delimited string.
        
        Returns:
            str: "species\tgene\toccurances\tdatabase"
        """
        return (self.delimiter).join([self.species, self.gene, str(self.occurances), self.database_name ])
                