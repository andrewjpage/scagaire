# API Documentation

This document provides detailed API reference for Scagaire modules and classes.

## Table of Contents

1. [Core Modules](#core-modules)
2. [Parser Modules](#parser-modules)
3. [Data Classes](#data-classes)
4. [Utility Modules](#utility-modules)

## Core Modules

### scagaire.Scagaire

Main controller class for filtering AMR results.

```python
from scagaire.Scagaire import Scagaire

class Scagaire:
    """Filter AMR results by bacterial species."""
```

#### Constructor

```python
def __init__(self, options):
    """
    Initialize Scagaire filtering system.
    
    Args:
        options: Object with attributes:
            - verbose (bool): Enable verbose output
            - input_file (str): Path to AMR results file
            - database_file (str): Path to species database (None for bundled)
            - database_name (str): Name of AMR database
            - minimum_occurances (int): Minimum gene occurrence threshold
            - output_file (str): Output file path (None for STDOUT)
            - results_type (str): Input format type
            - summary_file (str): Summary output file path
            - overwrite_files (bool): Whether to overwrite existing files
            - species (str): Species name(s) to filter by
    """
```

#### Methods

```python
def parse_species(self, species_str):
    """
    Parse and expand species string.
    
    Args:
        species_str (str): Comma-separated species names or categories
        
    Returns:
        list: Expanded list of species names
    """

def output_summary(self, results, species):
    """
    Write summary statistics to file.
    
    Args:
        results (list): Filtered AMR result objects
        species (str): Species name
    """

def run(self):
    """Execute main filtering workflow."""
```

#### Example Usage

```python
class Options:
    def __init__(self):
        self.verbose = False
        self.input_file = 'amr_results.tsv'
        self.database_file = None
        self.database_name = 'ncbi'
        self.minimum_occurances = 0
        self.output_file = 'filtered.tsv'
        self.results_type = None
        self.summary_file = None
        self.overwrite_files = False
        self.species = 'Escherichia coli'

options = Options()
scagaire = Scagaire(options)
scagaire.run()
```

### scagaire.FilterResults

Filtering engine for AMR results.

```python
from scagaire.FilterResults import FilterResults

class FilterResults:
    """Filter AMR results by species."""
    
    def __init__(self, results_filename, database_filename, 
                 minimum_occurances, results_type, database_name, verbose):
        """
        Initialize filtering engine.
        
        Args:
            results_filename (str): Path to AMR results
            database_filename (str): Path to species database
            minimum_occurances (int): Minimum occurrence threshold
            results_type (str): Format hint (None for auto)
            database_name (str): Database name filter
            verbose (bool): Enable verbose output
        """
    
    def filter_by_species(self, species):
        """
        Filter results for specific species.
        
        Args:
            species (str): Species name
            
        Returns:
            list: Filtered AMR result objects
        """
```

### scagaire.IdentifyResults

Format detection for AMR results.

```python
from scagaire.IdentifyResults import IdentifyResults

class IdentifyResults:
    """Auto-detect and parse AMR result formats."""
    
    def __init__(self, input_file, results_type, verbose):
        """
        Initialize format detector.
        
        Args:
            input_file (str): Path to results file
            results_type (str): Format hint (None for auto)
            verbose (bool): Enable verbose output
        """
    
    def get_results(self):
        """
        Detect format and return parsed results.
        
        Returns:
            list: Parsed AMR result objects
        """
```

## Parser Modules

### scagaire.parser.AmrParser

Base class for AMR result parsers.

```python
from scagaire.parser.AmrParser import AmrParser

class AmrParser:
    """Base parser for AMR results."""
    
    def __init__(self, input_file, verbose):
        """
        Initialize parser.
        
        Args:
            input_file (str): Path to results file
            verbose (bool): Enable verbose output
        """
    
    def is_valid(self):
        """
        Check if file matches expected format.
        
        Returns:
            bool: True if format matches
        """
    
    def read_file_multi_delimiters(self):
        """
        Read file with auto-detected delimiter.
        
        Returns:
            list: List of rows
        """
```

### scagaire.parser.Abricate098

Parser for Abricate 0.9.8+ format.

```python
from scagaire.parser.Abricate098 import Abricate098

class Abricate098(AmrParser):
    """Parser for Abricate 0.9.8+ output."""
    
    def __init__(self, input_file, verbose):
        """
        Initialize Abricate 0.9.8+ parser.
        
        Args:
            input_file (str): Path to Abricate results
            verbose (bool): Enable verbose output
        
        Attributes:
            results (list): List of AbricateResult098 objects
            header (list): Column headers
        """
```

### scagaire.parser.SpeciesToGenes

Parser and manager for species-to-genes database.

```python
from scagaire.parser.SpeciesToGenes import SpeciesToGenes

class SpeciesToGenes:
    """Query interface for species database."""
    
    def __init__(self, input_file, verbose):
        """
        Initialize database parser.
        
        Args:
            input_file (str): Path to database TSV
            verbose (bool): Enable verbose output
        """
    
    def all_species(self):
        """
        Get list of all species.
        
        Returns:
            list: Sorted species names
        """
    
    def all_databases(self):
        """
        Get list of all databases.
        
        Returns:
            list: Sorted database names
        """
    
    def filter_by_species(self, query, database_name):
        """
        Filter entries by species and database.
        
        Args:
            query (str): Species name
            database_name (str): Database filter
            
        Returns:
            list: SpeciesGenes objects
        """
    
    def num_of_all_species(self):
        """
        Count unique species.
        
        Returns:
            int: Number of species
        """
```

## Data Classes

### scagaire.AbricateResult098

Data class for Abricate 0.9.8+ results.

```python
from scagaire.AbricateResult098 import AbricateResult098

class AbricateResult098:
    """Single AMR gene prediction from Abricate 0.9.8+."""
    
    def __init__(self, header=[]):
        """
        Initialize result object.
        
        Args:
            header (list): Column headers
        
        Attributes:
            file (str): Input filename
            sequence (str): Contig name
            start (str): Start position
            end (str): End position
            strand (str): Strand (+/-)
            gene (str): Gene name
            coverage (str): Coverage value
            perc_coverage (str): % coverage
            perc_identity (str): % identity
            database (str): AMR database
            accession (str): Accession number
            product (str): Product description
            resistance (str): Resistance annotation
        """
    
    def __str__(self):
        """
        Format as tab-delimited string.
        
        Returns:
            str: Tab-delimited result line
        """
```

### scagaire.SpeciesGenes

Data class for species-gene associations.

```python
from scagaire.SpeciesGenes import SpeciesGenes

class SpeciesGenes:
    """Association between species and AMR gene."""
    
    def __init__(self, species, gene, occurances, database_name):
        """
        Initialize species-gene association.
        
        Args:
            species (str): Species name
            gene (str): Gene name
            occurances (int): Occurrence count
            database_name (str): Database name
        
        Attributes:
            species (str): Bacterial species
            gene (str): AMR gene
            occurances (int): Occurrence count
            database_name (str): AMR database
        """
    
    def __str__(self):
        """
        Format as tab-delimited string.
        
        Returns:
            str: "species\tgene\tcount\tdatabase"
        """
```

## Utility Modules

### scagaire.Config

Configuration file parser.

```python
from scagaire.Config import Config

class Config:
    """Parse configuration JSON file."""
    
    def __init__(self, input_file, verbose):
        """
        Initialize config parser.
        
        Args:
            input_file (str): Path to config.json
            verbose (bool): Enable verbose output
        """
    
    def taxon_categories(self):
        """
        Get taxon category mappings.
        
        Returns:
            dict: Category name to species list
        """
    
    def taxon_categories_printable_list(self):
        """
        Generate printable category list.
        
        Returns:
            list: Formatted category strings
        """
```

### scagaire.Summary

Result aggregation.

```python
from scagaire.Summary import Summary

class Summary:
    """Aggregate results by gene name."""
    
    def __init__(self, results, verbose):
        """
        Initialize aggregator.
        
        Args:
            results (list): AMR result objects
            verbose (bool): Enable verbose output
        """
    
    def aggregate_results(self):
        """
        Aggregate by gene name.
        
        Returns:
            dict: Gene name to SummaryResult
        """
```

### scagaire.MashSpecies

Species verification using MASH.

```python
from scagaire.MashSpecies import MashSpecies

class MashSpecies:
    """Verify species using MASH distance."""
    
    def __init__(self, input_file, database, verbose, minimum_distance=0.1):
        """
        Initialize MASH validator.
        
        Args:
            input_file (str): Path to assembly
            database (str): Path to MASH database
            verbose (bool): Enable verbose output
            minimum_distance (float): Max distance threshold
        """
    
    def get_species(self):
        """
        Identify species of assembly.
        
        Returns:
            str: Species name or None
        """
```

### scagaire.ScagaireDownload

Database builder.

```python
from scagaire.ScagaireDownload import ScagaireDownload

class ScagaireDownload:
    """Build species-specific databases."""
    
    def __init__(self, options):
        """
        Initialize database builder.
        
        Args:
            options: Object with attributes for download parameters
        """
    
    def run(self):
        """Execute database building workflow."""
    
    def download_species(self):
        """
        Download assemblies from NCBI.
        
        Returns:
            str: Download directory path
        """
    
    def find_input_files(self, download_directory):
        """
        Find assembly files.
        
        Args:
            download_directory (str): Root directory
            
        Returns:
            list: Paths to assembly files
        """
```

## Complete Example

Here's a complete example using the API:

```python
#!/usr/bin/env python3
from scagaire.FilterResults import FilterResults
from scagaire.parser.SpeciesToGenes import SpeciesToGenes

# Initialize filtering engine
filter_results = FilterResults(
    results_filename='amr_results.tsv',
    database_filename='species_to_genes.tsv',
    minimum_occurances=5,
    results_type=None,  # Auto-detect
    database_name='ncbi',
    verbose=True
)

# Filter by species
species = 'Escherichia coli'
results = filter_results.filter_by_species(species)

# Print results
print(f"Found {len(results)} genes for {species}")
for result in results:
    print(f"{result.gene}\t{result.perc_identity}\t{result.perc_coverage}")

# Query database
db = SpeciesToGenes('species_to_genes.tsv', verbose=False)
print(f"Total species in database: {db.num_of_all_species()}")
print(f"Species: {', '.join(db.all_species()[:5])}...")
```

## Error Handling

Most classes raise standard Python exceptions:

```python
try:
    results = filter_results.filter_by_species(species)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid value: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
