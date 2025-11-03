# Scagaire Documentation

Welcome to the comprehensive documentation for Scagaire, a tool for filtering antimicrobial resistance (AMR) gene predictions by bacterial species.

## Table of Contents

1. [User Guide](user-guide.md) - How to use Scagaire
2. [Work Instructions](work-instructions.md) - Step-by-step workflows
3. [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
4. [Architecture Overview](architecture.md) - System design and components
5. [API Documentation](api.md) - Module and class references
6. [Testing Guide](testing.md) - Running and writing tests
7. [Installation Guide](installation.md) - Detailed installation instructions

## Quick Start

Scagaire allows you to filter AMR gene predictions from metagenomic samples by bacterial species, focusing on medically relevant pathogens.

### Basic Usage

```bash
# List available species
scagaire_species

# Filter AMR results by species
scagaire "Klebsiella pneumoniae" amr_results.tsv
```

### Key Features

- **Species-specific filtering**: Focus on AMR genes found in target pathogens
- **Multiple input formats**: Supports Abricate, StarAMR, and RGI outputs
- **Bundled database**: Includes 40 most common bacterial pathogens
- **Custom databases**: Build your own species-specific databases

## Getting Help

- **Documentation**: Browse the documents in this directory
- **Issues**: Report bugs on [GitHub Issues](https://github.com/quadram-institute-bioscience/scagaire/issues)
- **Questions**: See the [User Guide](user-guide.md) or README.md in the root directory

## Documentation Structure

Each document serves a specific purpose:

- **User Guide**: Comprehensive usage information for end users
- **Work Instructions**: Practical step-by-step workflows for common tasks
- **Contributing Guide**: Guidelines for developers and contributors
- **Architecture Overview**: Technical design and implementation details
- **API Documentation**: Code-level documentation for developers
- **Testing Guide**: Information about running and writing tests
- **Installation Guide**: Detailed installation procedures

## License

Scagaire is licensed under GPLv3. See the LICENSE file in the root directory for details.

## Citation

If you use Scagaire in your research, please cite:

```
Scagaire
Andrew J Page, Thanh Le Viet, Justin O'Grady
https://github.com/quadram-institute-bioscience/scagaire
```
