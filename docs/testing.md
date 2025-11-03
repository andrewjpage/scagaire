# Testing Guide

This guide covers running tests, understanding test coverage, and writing new tests for Scagaire.

## Table of Contents

1. [Running Tests](#running-tests)
2. [Test Structure](#test-structure)
3. [Test Coverage](#test-coverage)
4. [Writing Tests](#writing-tests)
5. [Test Data](#test-data)
6. [Continuous Integration](#continuous-integration)

## Running Tests

### Basic Test Execution

Run all tests:
```bash
cd /path/to/scagaire
python3 -m unittest discover -s scagaire/tests/ -p '*_test.py'
```

Run tests verbosely:
```bash
python3 -m unittest discover -s scagaire/tests/ -p '*_test.py' -v
```

Run specific test file:
```bash
python3 -m unittest scagaire/tests/Scagaire_test.py
```

Run specific test method:
```bash
python3 -m unittest scagaire/tests/Scagaire_test.TestScagaire.test_abricate097_staph
```

### Using the Test Script

Scagaire includes a convenience script:
```bash
./run_tests.sh
```

## Test Structure

### Directory Layout

```
scagaire/tests/
├── data/                  # Test fixtures and data files
│   ├── abricate/
│   ├── rgi/
│   ├── staramr/
│   └── scagaire/
├── FilterResults_test.py
├── IdentifyResults_test.py
├── Scagaire_test.py
├── ScagaireDownload_test.py
├── SpeciesDatabase_test.py
├── Summary_test.py
├── parserAbricate097_test.py
├── parserAbricate098_test.py
├── parserRgi_test.py
├── parserSpeciesToGenes_test.py
└── parserStaramr_test.py
```

### Test Naming Conventions

- **Files**: `ModuleName_test.py`
- **Classes**: `TestModuleName`
- **Methods**: `test_specific_behavior`

Example:
```python
# File: Scagaire_test.py
class TestScagaire(unittest.TestCase):
    def test_abricate097_staph(self):
        """Test filtering Abricate 0.9.7 results for S. aureus."""
        pass
```

## Test Coverage

### Checking Coverage

Install coverage tool:
```bash
pip install coverage
```

Run tests with coverage:
```bash
coverage run -m unittest discover -s scagaire/tests/ -p '*_test.py'
```

View coverage report:
```bash
coverage report --include="scagaire/*.py,scagaire/parser/*.py"
```

Generate HTML coverage report:
```bash
coverage html --include="scagaire/*.py,scagaire/parser/*.py"
# Open htmlcov/index.html in browser
```

### Current Coverage

As of the latest version:
```
Module                              Coverage
--------------------------------------------- 
scagaire/Scagaire.py                   79%
scagaire/FilterResults.py             100%
scagaire/IdentifyResults.py            96%
scagaire/parser/SpeciesToGenes.py      80%
... (see coverage report for complete data)
TOTAL                                  82%
```

**Target**: ≥80% coverage for all modules

### Coverage Goals

- **Core modules**: ≥90% coverage
- **Parsers**: ≥90% coverage
- **Utilities**: ≥80% coverage
- **Overall**: ≥80% coverage

## Writing Tests

### Test Template

```python
import unittest
import os
from scagaire.ModuleName import ClassName

class TestClassName(unittest.TestCase):
    """Tests for ClassName."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Get test data directory
        self.data_dir = os.path.join(
            os.path.dirname(__file__),
            'data',
            'module_name'
        )
        # Initialize test objects
        self.test_file = os.path.join(self.data_dir, 'test_data.txt')
    
    def test_basic_functionality(self):
        """Test basic use case."""
        # Arrange
        obj = ClassName(self.test_file, verbose=False)
        
        # Act
        result = obj.method()
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)
    
    def test_empty_input(self):
        """Test handling of empty input."""
        obj = ClassName(self.test_file, verbose=False)
        result = obj.method()
        self.assertEqual(len(result), 0)
    
    def test_invalid_input(self):
        """Test error handling for invalid input."""
        with self.assertRaises(ValueError):
            obj = ClassName('nonexistent.txt', verbose=False)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary files if created
        pass
```

### Testing Guidelines

#### 1. Test One Thing

Each test should verify one specific behavior:

```python
# Good: Tests one specific behavior
def test_filter_keeps_species_genes(self):
    """Test that filter keeps genes from target species."""
    results = filter_by_species("E. coli", genes)
    self.assertTrue(all(g.species == "E. coli" for g in results))

# Bad: Tests multiple things
def test_filtering(self):
    """Test filtering."""
    results = filter_by_species("E. coli", genes)
    self.assertGreater(len(results), 0)
    self.assertEqual(results[0].species, "E. coli")
    self.assertIn("blaCTX-M", [r.gene for r in results])
```

#### 2. Use Descriptive Names

```python
# Good: Clear what's being tested
def test_parser_handles_empty_file(self):
    """Test parser returns empty list for empty file."""
    pass

# Bad: Vague
def test_parser(self):
    """Test parser."""
    pass
```

#### 3. Include Docstrings

```python
def test_filter_minimum_occurances(self):
    """
    Test filtering with minimum occurrence threshold.
    
    Genes with fewer occurrences than threshold should be excluded.
    """
    pass
```

#### 4. Test Edge Cases

```python
def test_empty_input(self):
    """Test with empty input."""
    
def test_single_item(self):
    """Test with single item."""
    
def test_maximum_size(self):
    """Test with very large input."""
    
def test_special_characters(self):
    """Test with special characters in names."""
```

#### 5. Test Error Conditions

```python
def test_missing_file(self):
    """Test FileNotFoundError for missing file."""
    with self.assertRaises(FileNotFoundError):
        parse_file('nonexistent.txt')

def test_invalid_format(self):
    """Test ValueError for invalid format."""
    with self.assertRaises(ValueError):
        parse_results('invalid_format.txt')
```

### Assertion Methods

Common assertions:
```python
# Equality
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Truth
self.assertTrue(condition)
self.assertFalse(condition)

# Identity
self.assertIs(a, b)
self.assertIsNot(a, b)

# Membership
self.assertIn(a, collection)
self.assertNotIn(a, collection)

# Exceptions
with self.assertRaises(ExceptionType):
    function_that_raises()

# Comparisons
self.assertGreater(a, b)
self.assertLess(a, b)
self.assertGreaterEqual(a, b)

# Collections
self.assertListEqual(list1, list2)
self.assertDictEqual(dict1, dict2)
```

## Test Data

### Creating Test Files

Test data lives in `scagaire/tests/data/`:

```
data/
├── abricate/
│   ├── abricate097_results.tsv
│   └── abricate098_results.tsv
├── rgi/
│   └── rgi_results.txt
├── staramr/
│   └── resfinder.tsv
└── scagaire/
    └── species_to_genes.tsv
```

### Test Data Guidelines

1. **Minimal**: Use minimal data to test behavior
2. **Representative**: Cover typical and edge cases
3. **Documented**: Comment what each file tests
4. **Versioned**: Commit test data to repository

### Creating Test Fixtures

```python
import tempfile
import os

class TestMyClass(unittest.TestCase):
    def setUp(self):
        """Create temporary test files."""
        # Create temp directory
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test file
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(self.test_file, 'w') as f:
            f.write("test data\n")
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
```

## Continuous Integration

### Travis CI

Scagaire uses Travis CI for continuous integration. Configuration in `.travis.yml`:

```yaml
language: python
python:
  - "3.6"
  - "3.7"
  - "3.8"

install:
  - pip install -r requirements.txt

script:
  - python3 -m unittest discover -s scagaire/tests/
  - coverage run -m unittest discover -s scagaire/tests/
  - coverage report

after_success:
  - codecov
```

### Local Pre-commit Checks

Before committing, run:
```bash
# Run tests
python3 -m unittest discover -s scagaire/tests/ -v

# Check coverage
coverage run -m unittest discover -s scagaire/tests/
coverage report --fail-under=80

# Lint code
pylint scagaire/
```

## Debugging Tests

### Running Tests in Debug Mode

```python
# Add to test method:
import pdb; pdb.set_trace()

# Or use Python debugger:
python -m pdb -m unittest scagaire/tests/Scagaire_test.py
```

### Verbose Output

```bash
# Maximum verbosity
python3 -m unittest discover -s scagaire/tests/ -v 2>&1 | less

# Show print statements
python3 -m unittest discover -s scagaire/tests/ -v -b
```

### Testing with Debug Flag

Some classes have debug flags:
```python
obj = Scagaire(options)
obj.debug = True  # Enable debug output
obj.run()
```

## Best Practices

1. **Run tests frequently**: After each change
2. **Write tests first**: TDD approach
3. **Keep tests fast**: Mock slow operations
4. **Make tests independent**: No test dependencies
5. **Use meaningful assertions**: Clear failure messages
6. **Test error paths**: Not just happy paths
7. **Maintain coverage**: Keep above 80%
8. **Review test failures**: Understand why tests fail
9. **Update tests with code**: Keep in sync
10. **Document complex tests**: Explain non-obvious behavior

## Common Patterns

### Testing Parsers

```python
def test_parser_valid_file(self):
    """Test parser with valid input."""
    parser = MyParser(self.test_file, verbose=False)
    self.assertTrue(parser.is_valid())
    self.assertEqual(len(parser.results), expected_count)
    self.assertEqual(parser.results[0].gene, "expected_gene")
```

### Testing Filters

```python
def test_filter_by_species(self):
    """Test species filtering."""
    results = filter_results.filter_by_species("E. coli")
    self.assertGreater(len(results), 0)
    self.assertTrue(all(r.gene in expected_genes for r in results))
```

### Testing Database Operations

```python
def test_database_query(self):
    """Test database query."""
    db = SpeciesToGenes(self.db_file, verbose=False)
    species = db.all_species()
    self.assertIn("Escherichia coli", species)
    genes = db.filter_by_species("Escherichia coli", "ncbi")
    self.assertGreater(len(genes), 0)
```

## Troubleshooting

### Tests Fail Intermittently

- Check for race conditions
- Verify no shared state between tests
- Check filesystem timing issues

### Coverage Not Updating

```bash
# Clean coverage data
rm -rf .coverage htmlcov/

# Re-run with coverage
coverage run -m unittest discover -s scagaire/tests/
coverage report
```

### Import Errors

```bash
# Ensure package installed in development mode
pip install -e .

# Check PYTHONPATH
export PYTHONPATH=/path/to/scagaire:$PYTHONPATH
```
