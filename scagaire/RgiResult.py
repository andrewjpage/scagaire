"""
RgiResult - Data class for RGI (CARD) results

Represents a single AMR gene prediction from RGI (Resistance Gene Identifier)
which uses the CARD (Comprehensive Antibiotic Resistance Database).
"""

class RgiResult:
    """
    Single AMR gene prediction from RGI (CARD database).
    
    Attributes:
        orf_id (str): ORF identifier
        contig (str): Contig name
        start (str): Start position
        end (str): End position
        orientation (str): Gene orientation
        cut_off (str): Cut-off type
        pass_bitscore (str): Pass bitscore threshold
        best_hit_bitscore (str): Best hit bitscore
        gene (str): Gene name (Best_Hit_ARO)
        best_identities (str): Best identities percentage
        aro (str): ARO accession number
        model_type (str): Model type
        snps_in_best_hit_aro (str): SNPs in best hit
        other_snps (str): Other SNPs
        drug_class (str): Drug class
        resistance_mechanism (str): Resistance mechanism
        amr_gene_family (str): AMR gene family
        predicted_dna (str): Predicted DNA sequence
        predicted_protein (str): Predicted protein sequence
        card_protein_sequence (str): CARD protein sequence
        percentage_length_of_reference_sequence (str): Percentage length
        id (str): ID field
        model_id (str): Model ID
        nudged (str): Nudged field
        note (str): Additional notes
        header (list): Column headers
        delimiter (str): Output delimiter (tab)
    """
    
    def __init__(self, header = []):
        """
        Initialize RGI result object.
        
        Args:
            header (list): Column header names
        """
        self.orf_id = None
        self.contig = None
        self.start = None
        self.end = None
        self.orientation = None
        self.cut_off = None
        self.pass_bitscore = None
        self.best_hit_bitscore = None
        self.gene = None
        self.best_identities = None
        self.aro = None
        self.model_type = None
        self.snps_in_best_hit_aro = None
        self.other_snps = None
        self.drug_class = None
        self.resistance_mechanism = None
        self.amr_gene_family = None
        self.predicted_dna = None
        self.predicted_protein = None
        self.card_protein_sequence = None
        self.percentage_length_of_reference_sequence = None
        self.id = None
        self.model_id = None
        self.nudged = None
        self.note = None
        
        self.header = header
        self.delimiter = "\t"

    def __str__(self):
        """
        Format as tab-delimited string matching RGI format.
        
        Returns:
            str: Tab-delimited result line
        """
        return (self.delimiter).join([self.orf_id, self.contig, self.start, self.end, self.orientation, self.cut_off, self.pass_bitscore, self.best_hit_bitscore, self.gene, self.best_identities, self.aro, self.model_type, self.snps_in_best_hit_aro, self.other_snps, self.drug_class, self.resistance_mechanism, self.amr_gene_family, self.predicted_dna, self.predicted_protein, self.card_protein_sequence, self.percentage_length_of_reference_sequence, self.id, self.model_id, self.nudged, self.note 
        ])
        
        
          

