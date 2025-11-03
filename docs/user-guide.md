# Scagaire User Guide

This guide provides comprehensive information on using Scagaire to filter AMR gene predictions by bacterial species.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Command Reference](#command-reference)
5. [Input Formats](#input-formats)
6. [Output Formats](#output-formats)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

## Introduction

Scagaire (Irish for "filter") allows you to filter antimicrobial resistance (AMR) gene predictions from metagenomic samples based on bacterial species. This helps focus analysis on medically relevant pathogens rather than commensal bacteria.

### Why Use Scagaire?

- **Reduce false positives**: Filter out AMR genes from non-pathogenic bacteria
- **Species-specific analysis**: Focus on your pathogen of interest
- **Multiple databases**: Works with Abricate, StarAMR, and RGI outputs
- **Pre-built database**: Includes 40 most common bacterial pathogens

## Installation

### Conda Installation

```bash
pip install git+git://github.com/quadram-institute-bioscience/scagaire.git
```

### Docker Installation

```bash
docker pull quadraminstitute/scagaire
```

For detailed installation instructions, see [installation.md](installation.md).

## Basic Usage

### Step 1: Generate AMR Predictions

First, use your favorite AMR prediction tool on your assembly:

```bash
# Using Abricate
abricate my_assembly.fa > amr_results.tsv

# Using StarAMR
staramr search -o staramr_output my_assembly.fa

# Using RGI
rgi main -i my_assembly.fa -o rgi_output
```

### Step 2: List Available Species

Check which species are available in the database:

```bash
scagaire_species
```

### Step 3: Filter by Species

Filter your AMR results by a specific species:

```bash
scagaire "Klebsiella pneumoniae" amr_results.tsv
```

## Command Reference

### scagaire

Main filtering command for AMR results.

**Syntax:**
```bash
scagaire [options] species input_file
```

**Arguments:**
- `species`: Species name (must match database exactly, use quotes)
- `input_file`: AMR results file from Abricate, StarAMR, or RGI

**Options:**
- `-h, --help`: Show help message
- `-d DATABASE, --database DATABASE`: Path to custom database
- `-t {abricate,rgi,staramr}, --results_type`: Force input format
- `-o OUTPUT, --output_file OUTPUT`: Output file (default: STDOUT)
- `-m COUNT, --minimum_occurances COUNT`: Minimum gene occurrences (default: 0)
- `-v, --verbose`: Verbose output
- `--debug`: Debug mode (keep intermediate files)
- `--version`: Show version

**Examples:**

```bash
# Basic filtering
scagaire "Salmonella enterica" abricate_results.tsv

# Save to file
scagaire "Escherichia coli" amr_results.tsv -o filtered_results.tsv

# Filter with minimum occurrence threshold
scagaire "Staphylococcus aureus" amr_results.tsv -m 5

# Multiple species (comma-separated)
scagaire "Salmonella enterica,Escherichia coli" amr_results.tsv

# Use category shortcut
scagaire "skin" amr_results.tsv  # Filters by all skin-associated pathogens
```

### scagaire_species

List all available species in the database.

**Syntax:**
```bash
scagaire_species [options]
```

**Options:**
- `-h, --help`: Show help message
- `-v, --verbose`: Verbose output
- `--version`: Show version
- `-d, --detailed`: Show detailed database matrix
- `-o, --overview`: Show summary statistics

**Examples:**

```bash
# Simple list
scagaire_species

# Detailed matrix view
scagaire_species --detailed

# Summary statistics
scagaire_species --overview
```

### scagaire_download

Build custom species databases from NCBI.

**Syntax:**
```bash
scagaire_download [options] species
```

**Arguments:**
- `species`: Species name to download and process

**Options:**
- `-l {all,complete,chromosome,scaffold,contig}`: Assembly level (default: all)
- `-t THREADS`: Number of threads (default: 1)
- `-o OUTPUT`: Output database file (default: species_to_genes.tsv)
- `-m MASH_DB`: Custom MASH database
- `--min_coverage`: Minimum coverage percentage (default: 95)
- `--min_identity`: Minimum identity percentage (default: 95)
- `--abricate_database`: Abricate database to use (default: ncbi)

**Example:**

```bash
scagaire_download "Campylobacter jejuni" -t 4 -o campylobacter_db.tsv
```

## Input Formats

Scagaire automatically detects and parses three input formats:

### Abricate Format

Tab-delimited output from Abricate (versions 0.9.7 and 0.9.8+).

**Required columns:**
- #FILE, SEQUENCE, START, END, GENE, %COVERAGE, %IDENTITY

### StarAMR Format

Tab-delimited resfinder.tsv output from StarAMR.

**Required columns:**
- Isolate ID, Gene, Predicted Phenotype, %Identity, %Overlap

### RGI Format

Tab-delimited output from RGI (CARD database).

**Required columns:**
- ORF_ID, Contig, Start, Stop, Best_Hit_ARO

## Output Formats

Scagaire outputs results in the same format as the input, with only species-specific genes retained.

### Standard Output

By default, results are printed to STDOUT in the original format:

```bash
scagaire "Klebsiella pneumoniae" amr_results.tsv
```

### File Output

Save to a file using `-o`:

```bash
scagaire "Klebsiella pneumoniae" amr_results.tsv -o filtered.tsv
```

### Summary Output

Use the summary file option in scripts for aggregated statistics.

## Advanced Usage

### Using Custom Databases

Build and use your own species database:

```bash
# Build database
scagaire_download "Mycobacterium tuberculosis" -o mtb_db.tsv

# Use custom database
scagaire "Mycobacterium tuberculosis" amr_results.tsv -d mtb_db.tsv
```

### Filtering by Occurrence

Exclude rarely observed genes:

```bash
# Only keep genes observed in at least 5 assemblies
scagaire "Escherichia coli" amr_results.tsv -m 5
```

### Multiple Species

Filter by multiple species at once:

```bash
scagaire "Escherichia coli,Klebsiella pneumoniae,Salmonella enterica" amr_results.tsv
```

### Using Taxon Categories

Use predefined categories for groups of related pathogens:

```bash
# Skin pathogens
scagaire "skin" amr_results.tsv

# Respiratory pathogens
scagaire "respiratory" amr_results.tsv
```

### Docker Usage

When using Docker, mount your data directory:

```bash
docker run --rm -it -v /path/to/data:/data quadraminstitute/scagaire \
  scagaire "Klebsiella pneumoniae" /data/amr_results.tsv
```

## Troubleshooting

### "Species not found in database"

The species name must exactly match a name in the database. Use `scagaire_species` to see available names.

### Format Not Detected

If auto-detection fails, specify format explicitly:

```bash
scagaire "Escherichia coli" amr_results.tsv -t abricate
```

### Empty Results

This may indicate:
- No genes in your results match the species
- Genes are below the minimum occurrence threshold
- Species name doesn't match database

### Permission Denied

Ensure you have write permissions for the output directory.

## Best Practices

1. **Use quotes** around species names: `"Escherichia coli"`
2. **Check available species** before filtering
3. **Start with default settings** before adjusting thresholds
4. **Use verbose mode** (`-v`) when troubleshooting
5. **Keep original results** for comparison

## Performance Tips

- Use the `-m` option to exclude rare genes and reduce noise
- Process large datasets in parallel by species
- Use SSD storage for faster database access

## Support

For additional help:
- Check the [README.md](../README.md) in the root directory
- Report issues on [GitHub](https://github.com/quadram-institute-bioscience/scagaire/issues)
- Review [work-instructions.md](work-instructions.md) for common workflows
