# Installation Guide

This guide provides detailed instructions for installing Scagaire on various platforms and configurations.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Conda Installation](#conda-installation)
4. [Pip Installation](#pip-installation)
5. [Docker Installation](#docker-installation)
6. [Galaxy Installation](#galaxy-installation)
7. [Development Installation](#development-installation)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

## System Requirements

### Operating Systems

- **Linux**: Ubuntu 16.04+, CentOS 7+, Debian 9+
- **macOS**: 10.12 (Sierra) or later
- **Windows**: Not officially supported (use Docker or WSL2)

### Software Dependencies

**Required**:
- Python 3.6 or later
- pip (Python package installer)

**Optional** (for building databases):
- mash (species verification)
- abricate (AMR gene prediction)
- ncbi-genome-download (downloading genomes)

### Hardware Requirements

**Minimum**:
- 512 MB RAM
- 100 MB disk space (for software)
- 1 GB disk space (including database)

**Recommended**:
- 2 GB RAM
- 5 GB disk space
- Multi-core CPU (for database building)

## Installation Methods

Choose the method that best suits your needs:

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| Conda | Most users | Easy, manages dependencies | Requires conda |
| Pip | Python developers | Direct install | May need system deps |
| Docker | Containerized environments | Isolated, reproducible | Requires Docker |
| Galaxy | Galaxy users | Integrated workflow | Limited to Galaxy |
| Development | Contributors | Latest code, editable | Manual dependencies |

## Conda Installation

Conda is the recommended installation method for most users.

### Step 1: Install Conda

If you don't have conda installed:

**Linux/macOS**:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
```

**Verify conda installation**:
```bash
conda --version
```

### Step 2: Install Scagaire

```bash
pip install git+git://github.com/quadram-institute-bioscience/scagaire.git
```

### Step 3: Install Optional Dependencies

For building databases:
```bash
conda install -c conda-forge -c bioconda mash abricate ncbi-genome-download
```

### Step 4: Verify Installation

```bash
scagaire --version
scagaire_species
```

## Pip Installation

### Prerequisites

Ensure Python 3.6+ and pip are installed:

```bash
python3 --version
pip3 --version
```

### Installation

```bash
pip3 install git+git://github.com/quadram-institute-bioscience/scagaire.git
```

### User Installation (No Root)

```bash
pip3 install --user git+git://github.com/quadram-institute-bioscience/scagaire.git

# Add to PATH (add to ~/.bashrc for persistence)
export PATH=$PATH:$HOME/.local/bin
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv scagaire-env

# Activate
source scagaire-env/bin/activate  # Linux/macOS
# scagaire-env\Scripts\activate   # Windows

# Install
pip install git+git://github.com/quadram-institute-bioscience/scagaire.git

# Deactivate when done
deactivate
```

## Docker Installation

Docker provides an isolated, reproducible environment.

### Step 1: Install Docker

**Linux (Ubuntu)**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in
```

**macOS**: Download Docker Desktop from https://www.docker.com/products/docker-desktop

**Verify**:
```bash
docker --version
```

### Step 2: Pull Scagaire Image

```bash
docker pull quadraminstitute/scagaire
```

### Step 3: Run Scagaire

```bash
# List available species
docker run --rm quadraminstitute/scagaire scagaire_species

# Filter results (mount your data directory)
docker run --rm -v /path/to/data:/data quadraminstitute/scagaire \
    scagaire "Escherichia coli" /data/amr_results.tsv > /path/to/filtered.tsv
```

### Docker Usage Tips

**Create alias for convenience**:
```bash
# Add to ~/.bashrc
alias scagaire='docker run --rm -v $(pwd):/data quadraminstitute/scagaire scagaire'

# Usage
scagaire "E. coli" amr_results.tsv
```

**Run interactively**:
```bash
docker run --rm -it -v /path/to/data:/data quadraminstitute/scagaire bash
# Now you're inside the container
scagaire --help
```

## Galaxy Installation

Scagaire is available in the Galaxy ToolShed.

### Installation

1. Log in to your Galaxy instance as admin
2. Go to **Admin** → **Install and Uninstall**
3. Search for "scagaire" in the ToolShed
4. Click **Install**
5. Select tool panel section
6. Confirm installation

### Usage in Galaxy

1. Upload your AMR results file
2. Find Scagaire in the tool panel
3. Select input file and species
4. Run tool
5. View filtered results

## Development Installation

For contributors and developers.

### Step 1: Clone Repository

```bash
git clone https://github.com/quadram-institute-bioscience/scagaire.git
cd scagaire
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install in Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .
```

### Step 4: Install Development Tools

```bash
pip install pytest pytest-cov coverage pylint black flake8
```

### Step 5: Run Tests

```bash
python3 -m unittest discover -s scagaire/tests/ -v
```

## Verification

### Check Installation

```bash
# Check version
scagaire --version

# Should print version number, e.g., "1.0.0"
```

### List Available Commands

```bash
# Main filtering command
scagaire --help

# Species listing
scagaire_species --help

# Database builder
scagaire_download --help
```

### Test with Example Data

```bash
# List species
scagaire_species

# Should print list of available species
```

### Run Test Suite

```bash
cd /path/to/scagaire
python3 -m unittest discover -s scagaire/tests/

# All tests should pass (except possibly one requiring mash)
```

## Troubleshooting

### Common Issues

#### "Command not found: scagaire"

**Cause**: Installation directory not in PATH.

**Solution**:
```bash
# Find installation location
pip show scagaire

# Add to PATH (Linux/macOS)
export PATH=$PATH:$HOME/.local/bin

# Make permanent
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

#### "No module named 'scagaire'"

**Cause**: Package not installed or wrong Python version.

**Solution**:
```bash
# Verify Python version
python3 --version

# Reinstall
pip3 install --force-reinstall git+git://github.com/quadram-institute-bioscience/scagaire.git
```

#### Permission Denied

**Cause**: Insufficient permissions.

**Solution**:
```bash
# Install for current user only
pip3 install --user git+git://github.com/quadram-institute-bioscience/scagaire.git

# Or use virtual environment
python3 -m venv env
source env/bin/activate
pip install git+git://github.com/quadram-institute-bioscience/scagaire.git
```

#### Docker: Cannot Connect

**Cause**: Docker daemon not running.

**Solution**:
```bash
# Start Docker
sudo systemctl start docker  # Linux
# Or start Docker Desktop (macOS/Windows)

# Verify
docker ps
```

#### Tests Fail: "mash: command not found"

**Cause**: Optional dependency not installed.

**Solution**: This is expected if mash isn't installed. Only one test requires it.

```bash
# Install mash (optional)
conda install -c bioconda mash
```

### Platform-Specific Issues

#### macOS: SSL Certificate Error

**Cause**: Python SSL certificates not installed.

**Solution**:
```bash
# Run Python's certificate installer
/Applications/Python\ 3.*/Install\ Certificates.command

# Or install certifi
pip install --upgrade certifi
```

#### Linux: "externally-managed-environment" Error

**Cause**: System Python is managed by package manager.

**Solution**:
```bash
# Use virtual environment
python3 -m venv env
source env/bin/activate
pip install git+git://github.com/quadram-institute-bioscience/scagaire.git

# Or use --break-system-packages (not recommended)
pip install --break-system-packages git+git://github.com/quadram-institute-bioscience/scagaire.git
```

#### Windows (WSL2): Path Issues

**Cause**: Windows/Linux path confusion.

**Solution**:
```bash
# Use Linux paths within WSL2
cd /home/username/data  # Not /mnt/c/Users/...

# Or convert paths
wslpath 'C:\Users\username\data'
```

## Updating

### Conda/Pip Installation

```bash
pip install --upgrade git+git://github.com/quadram-institute-bioscience/scagaire.git
```

### Docker Installation

```bash
docker pull quadraminstitute/scagaire
```

### Development Installation

```bash
cd /path/to/scagaire
git pull
pip install -e .
```

## Uninstallation

### Conda/Pip

```bash
pip uninstall scagaire
```

### Docker

```bash
docker rmi quadraminstitute/scagaire
```

### Development

```bash
cd /path/to/scagaire
pip uninstall scagaire
cd ..
rm -rf scagaire
```

## Additional Resources

- **Repository**: https://github.com/quadram-institute-bioscience/scagaire
- **Issues**: https://github.com/quadram-institute-bioscience/scagaire/issues
- **Documentation**: See docs/ directory
- **Conda Package**: https://anaconda.org/bioconda/scagaire

## Getting Help

If you encounter issues not covered here:

1. Check the [User Guide](user-guide.md)
2. Search [existing issues](https://github.com/quadram-institute-bioscience/scagaire/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Installation method
   - Complete error message
   - Steps to reproduce
