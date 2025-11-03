# Scagaire Architecture Overview

This document describes the technical architecture and design of Scagaire.

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [Data Flow](#data-flow)
4. [Module Structure](#module-structure)
5. [Database Format](#database-format)
6. [Design Patterns](#design-patterns)
7. [Extension Points](#extension-points)

## System Overview

Scagaire is a command-line tool designed to filter AMR (Antimicrobial Resistance) gene predictions by bacterial species. The system consists of:

- **Input parsers** for multiple AMR prediction tools
- **Filtering engine** using species-to-genes database
- **Database builder** for creating custom databases
- **Output formatters** matching input formats

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     User Input                          │
│  (AMR Results + Species Name + Parameters)              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                 Format Detection                         │
│  (IdentifyResults)                                       │
│  ├─ Try Abricate 0.9.8+                                 │
│  ├─ Try Abricate 0.9.7                                  │
│  ├─ Try StarAMR                                         │
│  └─ Try RGI                                             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              Parse Input Results                         │
│  (Format-Specific Parsers)                               │
│  └─ Create Result Objects                               │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│           Load Species Database                          │
│  (SpeciesToGenes)                                        │
│  └─ Parse species-to-genes.tsv                          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              Filter Results                              │
│  (FilterResults)                                         │
│  ├─ Match genes to species                              │
│  └─ Apply occurrence threshold                          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│               Format Output                              │
│  (Same format as input)                                  │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Main Controller (Scagaire)

**Purpose**: Orchestrates the filtering workflow.

**Responsibilities**:
- Parse command-line options
- Initialize filtering components
- Process each species in the list
- Generate output files

**Key Methods**:
- `__init__()`: Initialize with options
- `parse_species()`: Expand species categories
- `run()`: Execute filtering workflow
- `output_summary()`: Generate summary statistics

### 2. Format Identifier (IdentifyResults)

**Purpose**: Auto-detect AMR results format.

**Strategy**: Try each parser sequentially until one validates successfully.

**Supported Formats**:
- Abricate 0.9.8+ (primary)
- Abricate 0.9.7 (legacy)
- StarAMR
- RGI (CARD)

### 3. Result Parsers

**Base Class**: `AmrParser`

**Implementations**:
- `Abricate097`: Legacy Abricate format
- `Abricate098`: Current Abricate format
- `Staramr`: StarAMR/ResFinder format
- `Rgi`: RGI/CARD format

**Common Pattern**:
```python
class FormatParser(AmrParser):
    def __init__(self, input_file, verbose):
        self.default_header = [...]
        self.column_to_variable_mapping = {...}
        self.results = self.populate_results()
    
    def populate_results(self):
        # Read file
        # Parse rows
        # Create result objects
        # Return list
```

### 4. Database Manager (SpeciesToGenes)

**Purpose**: Load and query species-to-genes database.

**Database Schema**:
```
species | gene | occurrences | source | database | method | date
```

**Query Methods**:
- `all_species()`: List all species
- `all_databases()`: List all databases
- `filter_by_species()`: Get genes for species
- `species_databases()`: Get databases for species

### 5. Filtering Engine (FilterResults)

**Purpose**: Filter AMR results by species.

**Algorithm**:
```python
1. Parse all input results
2. Load species-specific genes from database
3. Create lookup dictionary {gene: occurrences}
4. Filter: keep only genes in lookup with count ≥ threshold
5. Return filtered results
```

**Performance**: O(n + m) where n=input results, m=database entries

### 6. Database Builder (ScagaireDownload)

**Purpose**: Build custom species databases.

**Workflow**:
```
1. Download assemblies from NCBI
2. Validate species with MASH
3. Run Abricate on each assembly
4. Aggregate gene occurrences
5. Write to database file
```

**Components**:
- `MashSpecies`: Species verification
- `AbricateAmrResults`: AMR prediction
- `SpeciesDatabase`: Database output

## Data Flow

### Filtering Workflow

```
Input File → Format Detection → Parsing → Result Objects
                                              ↓
                                         Gene Names
                                              ↓
Species Name → Config → Species List → Database Query
                                              ↓
                                      Species-Gene Map
                                              ↓
Result Objects + Species-Gene Map → Filtering → Filtered Results → Output
```

### Database Building Workflow

```
Species Name → NCBI Download → Assembly Files
                                     ↓
                              MASH Validation
                                     ↓
                              Validated Files
                                     ↓
                              Abricate (parallel)
                                     ↓
                              AMR Predictions
                                     ↓
                              Aggregation
                                     ↓
                              Database File
```

## Module Structure

```
scagaire/
├── __init__.py
├── Scagaire.py              # Main controller
├── FilterResults.py         # Filtering logic
├── IdentifyResults.py       # Format detection
├── Config.py                # Configuration parser
├── ScagaireDownload.py      # Database builder
├── ScagaireCompare.py       # Species comparison
├── ScagaireSpecies.py       # Species listing
├── Summary.py               # Result aggregation
├── SummaryResult.py         # Summary data class
├── SpeciesGenes.py          # Species-gene data class
├── SpeciesDatabase.py       # Database writer
├── MashSpecies.py           # Species validation
├── AbricateAmrResults.py    # Abricate runner
├── AbricateResult097.py     # Data class
├── AbricateResult098.py     # Data class
├── RgiResult.py             # Data class
├── StaramrResult.py         # Data class
├── parser/
│   ├── __init__.py
│   ├── AmrParser.py         # Base parser
│   ├── Abricate097.py       # Format parser
│   ├── Abricate098.py       # Format parser
│   ├── Rgi.py               # Format parser
│   ├── Staramr.py           # Format parser
│   └── SpeciesToGenes.py    # Database parser
├── data/
│   ├── config.json          # Taxon categories
│   ├── species_to_genes.tsv # Main database
│   └── refseq_reference_*.msh # MASH database
└── tests/
    ├── *_test.py            # Unit tests
    └── data/                # Test fixtures
```

## Database Format

### Species-to-Genes Database

**File**: `species_to_genes.tsv`

**Format**: Tab-delimited with header

**Columns**:
1. `species`: Bacterial species name (e.g., "Escherichia coli")
2. `gene`: AMR gene name (e.g., "blaKPC-2")
3. `occurrences`: Number of assemblies containing gene
4. `source`: Data source ("abricate")
5. `database`: AMR database used ("ncbi", "card", etc.)
6. `method`: Collection method ("auto", "manual")
7. `date`: Date created (YYYYMMDD)

**Example**:
```
Klebsiella pneumoniae	blaKPC-2	156	abricate	ncbi	auto	20231031
Escherichia coli	blaCTX-M-15	423	abricate	ncbi	auto	20231031
```

**Indexing**: Loaded into memory, filtered by species+database in O(n) time.

### Configuration File

**File**: `config.json`

**Format**: JSON

**Structure**:
```json
{
  "taxon_categories": {
    "skin": [
      "Staphylococcus aureus",
      "Streptococcus pyogenes"
    ],
    "respiratory": [
      "Streptococcus pneumoniae",
      "Haemophilus influenzae"
    ]
  }
}
```

## Design Patterns

### 1. Strategy Pattern (Parsers)

Different parsing strategies for different formats, all implementing common interface.

```python
class AmrParser:  # Strategy interface
    def is_valid(self): pass
    def populate_results(self): pass

class Abricate098(AmrParser):  # Concrete strategy
    def is_valid(self): ...
    def populate_results(self): ...
```

### 2. Template Method Pattern

Base parser defines structure, subclasses implement specifics.

```python
class AmrParser:
    def populate_results(self):  # Template method
        file_contents = self.read_file_multi_delimiters()
        header = self.get_header(file_contents)
        # Subclass-specific processing
        return results
```

### 3. Factory Pattern (Result Objects)

Parsers create appropriate result objects based on format.

```python
def populate_results(self):
    for row in file_contents:
        result = AbricateResult098()  # Factory method
        # Populate result
        results.append(result)
    return results
```

### 4. Facade Pattern (Main Controller)

`Scagaire` class provides simplified interface to complex subsystems.

```python
class Scagaire:
    def run(self):
        # Hides complexity of:
        # - Format detection
        # - Parsing
        # - Database queries
        # - Filtering
        # - Output generation
```

## Extension Points

### Adding New AMR Tool Support

**Steps**:
1. Create result data class in `scagaire/`
2. Create parser in `scagaire/parser/`
3. Add to format detection in `IdentifyResults`
4. Add tests in `scagaire/tests/`

**Example**:
```python
# 1. Result class
class NewToolResult:
    def __init__(self, header=[]):
        self.gene = None
        # ... other fields

# 2. Parser
class NewTool(AmrParser):
    def __init__(self, input_file, verbose):
        self.default_header = [...]
        # ... parser logic

# 3. Detection
class IdentifyResults:
    def get_results(self):
        # ... existing parsers
        nt = NewTool(self.input_file, self.verbose)
        if nt.is_valid() or self.results_type == 'newtool':
            return nt.results
```

### Adding New Database Sources

**Options**:
1. Extend `ScagaireDownload` to support new sources
2. Create converter script for external databases
3. Manually curate database entries

**Requirements**:
- Must produce compatible TSV format
- Species names must be consistent
- Occurrence counts must be accurate

### Adding New Analysis Features

**Integration points**:
- New command: Create new script in `scripts/`
- New analysis: Add method to existing class
- New filter: Extend `FilterResults`

## Performance Considerations

### Memory Usage

- Database loaded entirely into memory: ~10-50 MB
- Result objects created for all predictions
- Minimal memory growth during processing

**Optimization**: Stream processing for very large files could be implemented.

### Processing Speed

- Format detection: <0.1s
- Parsing: ~0.01s per 100 results
- Filtering: O(n+m) where n=results, m=database
- Total: <1s for typical metagenomic sample

**Bottlenecks**: Database building (downloads + Abricate runs)

### Scalability

- Single sample: <1s
- Batch processing: Linear scaling
- Database building: Limited by NCBI/Abricate performance

## Security Considerations

### Input Validation

- File paths validated before access
- Species names sanitized for database queries
- Numeric parameters range-checked

### Dependency Security

- Minimal external dependencies
- Standard library preferred
- Dependencies pinned in requirements

### Database Integrity

- Database format validated on load
- Malformed entries skipped with warning
- No arbitrary code execution

## Future Architecture Improvements

### Potential Enhancements

1. **Streaming Parser**: Handle very large files (>1GB)
2. **Database Indexing**: Speed up species queries
3. **Parallel Processing**: Multi-threaded batch processing
4. **API Server**: REST API for web integration
5. **Plugin System**: Dynamic parser registration
6. **Caching**: Cache parsed databases

### Backward Compatibility

- Maintain support for existing database format
- Version detection for format changes
- Migration scripts for major updates
