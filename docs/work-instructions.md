# Scagaire Work Instructions

This document provides step-by-step workflows for common Scagaire tasks. Follow these procedures for consistent, reliable results.

## Table of Contents

1. [Standard Workflow: Filtering Metagenomic AMR Results](#standard-workflow)
2. [Building a Custom Species Database](#building-custom-database)
3. [Comparing AMR Profiles Between Species](#comparing-species)
4. [Batch Processing Multiple Samples](#batch-processing)
5. [Quality Control Checks](#quality-control)
6. [Interpreting Results](#interpreting-results)

---

## Standard Workflow: Filtering Metagenomic AMR Results

**Purpose**: Filter AMR predictions from a metagenomic sample to focus on a specific pathogen.

**Prerequisites**:
- Assembled metagenomic contigs in FASTA format
- Scagaire installed and accessible
- AMR prediction tool (Abricate recommended)

### Procedure

#### Step 1: Predict AMR Genes

**Action**: Run Abricate on your assembly.

```bash
abricate --db ncbi my_assembly.fasta > amr_predictions.tsv
```

**Expected output**: Tab-delimited file with AMR gene predictions.

**Quality check**: Verify file is not empty and contains expected columns.

```bash
head -2 amr_predictions.tsv
wc -l amr_predictions.tsv
```

#### Step 2: Identify Target Species

**Action**: Determine which species you want to focus on.

**Option A**: Check what's available in the database:
```bash
scagaire_species
```

**Option B**: If you know your species, verify it's in the database:
```bash
scagaire_species | grep "Klebsiella"
```

**Note**: Species name must match exactly (case-sensitive).

#### Step 3: Filter AMR Results

**Action**: Filter predictions by target species.

```bash
scagaire "Klebsiella pneumoniae" amr_predictions.tsv > filtered_results.tsv
```

**Quality check**: Verify filtered results:
```bash
# Check result count
wc -l filtered_results.tsv

# View first few results
head filtered_results.tsv
```

#### Step 4: Review and Interpret

**Action**: Analyze filtered results.

**What to check**:
- Number of genes identified
- Gene names and resistance classes
- Coverage and identity percentages
- Presence of known resistance markers

**Example interpretation**:
```
5 AMR genes found in K. pneumoniae:
- blaKPC-2: Carbapenem resistance
- aac(6')-Ib: Aminoglycoside resistance
- oqxAB: Fluoroquinolone resistance
```

---

## Building a Custom Species Database

**Purpose**: Create a species-specific AMR database for species not included in the bundled data.

**Prerequisites**:
- `ncbi-genome-download` installed
- `abricate` installed
- `mash` installed
- Internet connection

### Procedure

#### Step 1: Prepare Working Directory

```bash
mkdir -p custom_databases
cd custom_databases
```

#### Step 2: Download and Process Species Data

**Action**: Run scagaire_download for your species.

```bash
scagaire_download "Mycobacterium tuberculosis" \
  -t 4 \
  -o mtb_database.tsv \
  --assembly_level complete
```

**Parameters explained**:
- `-t 4`: Use 4 CPU threads
- `-o mtb_database.tsv`: Output file name
- `--assembly_level complete`: Only use complete genomes

**Time estimate**: 15 minutes to several hours depending on:
- Number of assemblies available
- Assembly quality
- Network speed
- CPU threads used

#### Step 3: Verify Database Creation

**Quality checks**:

```bash
# Check database file exists and has content
ls -lh mtb_database.tsv
wc -l mtb_database.tsv

# View database structure
head -5 mtb_database.tsv

# Count unique genes
cut -f2 mtb_database.tsv | sort -u | wc -l
```

**Expected format**:
```
Species\tGene\tCount\tSource\tDatabase\tMethod\tDate
```

#### Step 4: Use Custom Database

```bash
scagaire "Mycobacterium tuberculosis" amr_results.tsv -d mtb_database.tsv
```

---

## Comparing AMR Profiles Between Species

**Purpose**: Identify shared AMR genes between two species.

**Prerequisites**:
- Species names known and in database
- Understanding of AMR epidemiology

### Procedure

#### Step 1: Identify Species to Compare

```bash
# Check species are in database
scagaire_species | grep -E "Salmonella|Escherichia"
```

#### Step 2: Run Comparison

```bash
scagaire_compare \
  --species1 "Salmonella enterica" \
  --species2 "Escherichia coli" \
  --database_filter ncbi
```

#### Step 3: Analyze Shared Genes

**Output format**:
```
Gene\tSpecies1\tCount1\tSpecies2\tCount2
```

**Interpretation**:
- High counts in both: Widely distributed resistance
- High in one, low in other: Species-specific patterns
- Similar counts: Possible horizontal transfer

---

## Batch Processing Multiple Samples

**Purpose**: Process multiple metagenomic samples efficiently.

### Procedure

#### Step 1: Prepare Sample List

Create `samples.txt`:
```
sample1	Klebsiella pneumoniae
sample2	Escherichia coli
sample3	Salmonella enterica
```

#### Step 2: Create Processing Script

Create `process_batch.sh`:

```bash
#!/bin/bash

while IFS=$'\t' read -r sample species; do
    echo "Processing ${sample}..."
    
    # Run Abricate
    abricate "${sample}.fasta" > "${sample}_amr.tsv"
    
    # Filter by species
    scagaire "${species}" "${sample}_amr.tsv" > "${sample}_filtered.tsv"
    
    echo "Completed ${sample}"
done < samples.txt
```

#### Step 3: Execute Batch Processing

```bash
chmod +x process_batch.sh
./process_batch.sh
```

#### Step 4: Aggregate Results

```bash
# Combine all filtered results
cat *_filtered.tsv > all_filtered_results.tsv

# Count genes per sample
for f in *_filtered.tsv; do
    echo "$f: $(grep -v '^#' $f | wc -l) genes"
done
```

---

## Quality Control Checks

**Purpose**: Ensure data quality throughout the workflow.

### Input Quality Checks

#### Assembly Quality

```bash
# Check assembly statistics
grep -c "^>" assembly.fasta  # Number of contigs
awk '/^>/ {next} {total += length($0)} END {print total}' assembly.fasta  # Total size
```

**Acceptable ranges**:
- Bacterial genome: 1-10 Mb
- Contig count: Fewer is better (<100 for good assembly)

#### AMR Prediction Quality

```bash
# Check prediction quality in Abricate results
awk -F'\t' '$9 >= 95 && $10 >= 95' amr_predictions.tsv | wc -l
```

**Quality thresholds**:
- Coverage ≥95%
- Identity ≥95%

### Output Quality Checks

#### Result Validation

```bash
# Verify all filtered genes are in original results
cut -f6 filtered_results.tsv | sort -u > filtered_genes.txt
cut -f6 amr_predictions.tsv | sort -u > all_genes.txt
comm -12 filtered_genes.txt all_genes.txt
```

#### Database Validation

```bash
# Check database statistics
scagaire_species --overview
```

**Expected metrics**:
- Species count: >30
- Database entries: >1000
- No empty values

---

## Interpreting Results

### Understanding Gene Counts

**High gene count (>20 genes)**:
- May indicate multidrug-resistant strain
- Check for clustered resistance patterns
- Verify assembly quality

**Low gene count (1-5 genes)**:
- May represent baseline resistance
- Check gene identity/coverage thresholds
- Consider species-specific patterns

**No genes found**:
- Species may not harbor AMR genes
- Check species name spelling
- Verify input format compatibility

### Assessing Clinical Significance

**Critical resistance markers**:
- Carbapenemases (blaKPC, blaNDM, blaOXA-48-like)
- Vancomycin resistance (vanA, vanB)
- Colistin resistance (mcr genes)
- Extended-spectrum β-lactamases (CTX-M, SHV, TEM)

**Action items for critical markers**:
1. Verify prediction quality (>95% identity/coverage)
2. Check gene context (plasmid vs. chromosome)
3. Consider reporting to public health authorities
4. Review infection control procedures

### Common Interpretation Pitfalls

**Avoid**:
- Assuming all predicted genes are functional
- Ignoring coverage/identity thresholds
- Over-interpreting rare genes
- Neglecting species taxonomy verification

**Best practices**:
- Use conservative thresholds
- Validate with additional tools
- Consider epidemiological context
- Consult resistance databases (CARD, ResFinder)

---

## Troubleshooting Common Issues

### No Results After Filtering

**Causes**:
1. Species name mismatch
2. No genes for this species in database
3. Input format not recognized

**Solutions**:
```bash
# Check exact species name
scagaire_species | grep -i "klebsiella"

# Force format detection
scagaire "Klebsiella pneumoniae" amr_results.tsv -t abricate

# Check with verbose mode
scagaire "Klebsiella pneumoniae" amr_results.tsv -v
```

### Database Download Failures

**Causes**:
1. Network timeout
2. NCBI rate limiting
3. No assemblies available

**Solutions**:
```bash
# Use retry logic
for i in {1..3}; do
    scagaire_download "Species name" && break
    sleep 60
done

# Check assembly availability at NCBI first
```

### Performance Issues

**Optimization strategies**:
- Use more threads: `-t 8`
- Process smaller batches
- Use SSD storage
- Filter assemblies by quality first

---

## Documentation Standards

When documenting your analysis:

**Include**:
- Scagaire version: `scagaire --version`
- Database version/date
- Input parameters used
- Quality thresholds applied
- Number of samples processed
- Date of analysis

**Example documentation**:
```
Analysis Date: 2024-01-15
Tool: Scagaire v1.0.0
Database: Bundled (species_to_genes.tsv, 2023-10-31)
Species: Klebsiella pneumoniae
Min Coverage: 95%
Min Identity: 95%
Samples: 50
Filtered Genes: 247 total, 15 unique
```
