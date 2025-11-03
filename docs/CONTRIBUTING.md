# Contributing to Scagaire

Thank you for your interest in contributing to Scagaire! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contribution Workflow](#contribution-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Submitting Changes](#submitting-changes)
9. [Reporting Bugs](#reporting-bugs)
10. [Feature Requests](#feature-requests)

## Code of Conduct

### Our Commitment

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race
- Ethnicity
- Age
- Religion
- Nationality

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or exclusionary behavior
- Trolling, insulting comments, or personal attacks
- Publishing others' private information
- Any conduct inappropriate in a professional setting

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.6 or later
- Git installed and configured
- Basic knowledge of Python and bioinformatics
- Familiarity with AMR concepts (helpful but not required)

### Finding Issues to Work On

1. Check the [issue tracker](https://github.com/quadram-institute-bioscience/scagaire/issues)
2. Look for issues tagged `good first issue` or `help wanted`
3. Read the issue description and comments
4. Comment on the issue to express interest

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/scagaire.git
cd scagaire
```

### 2. Create Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

### 3. Install Development Tools

```bash
# Install testing and linting tools
pip install pytest pytest-cov coverage
pip install pylint black flake8
```

### 4. Verify Installation

```bash
# Run tests to verify setup
python3 -m unittest discover -s scagaire/tests/

# Check code coverage
coverage run -m unittest discover -s scagaire/tests/
coverage report
```

## Contribution Workflow

### 1. Create a Branch

```bash
# Update your fork
git checkout master
git pull upstream master

# Create a feature branch
git checkout -b feature/your-feature-name
# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch naming conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions or modifications
- `refactor/` - Code refactoring

### 2. Make Changes

- Keep changes focused and atomic
- Write clear, descriptive commit messages
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
python3 -m unittest discover -s scagaire/tests/ -v

# Check code coverage
coverage run -m unittest discover -s scagaire/tests/
coverage report --include="scagaire/*.py,scagaire/parser/*.py"

# Coverage should be ≥80%
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: brief description"
```

**Commit message guidelines**:
- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed
- Reference issue numbers: "Fixes #123"

**Examples**:
```
Add support for parsing Abricate 1.0 format

- Add new parser class for version 1.0
- Update format detection logic
- Add tests for new format
Fixes #45
```

### 5. Push Changes

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifics:

#### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 120 characters
- **Imports**: Group stdlib, third-party, local; alphabetically within groups
- **Quotes**: Use single quotes for strings (except docstrings)

#### Naming Conventions

```python
# Classes: PascalCase
class AmrParser:
    pass

# Functions/methods: snake_case
def filter_by_species(species):
    pass

# Constants: UPPER_CASE
DEFAULT_DATABASE = 'species_to_genes.tsv'

# Private methods: leading underscore
def _internal_helper():
    pass
```

#### Documentation

**Module docstrings**:
```python
"""
Module name - Brief description

Longer description explaining the module's purpose,
key classes, and usage examples.
"""
```

**Class docstrings**:
```python
class MyClass:
    """
    Brief class description.
    
    Longer description of class purpose and behavior.
    
    Attributes:
        attribute1 (type): Description
        attribute2 (type): Description
    """
```

**Function/method docstrings**:
```python
def my_function(param1, param2):
    """
    Brief function description.
    
    Longer description if needed.
    
    Args:
        param1 (type): Description
        param2 (type): Description
        
    Returns:
        type: Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
```

### Code Quality

#### Use Type Hints (Encouraged)

```python
from typing import List, Optional

def filter_results(species: str, min_count: int = 0) -> List[str]:
    """Filter results by species."""
    pass
```

#### Error Handling

```python
# Do: Catch specific exceptions
try:
    result = parse_file(filename)
except FileNotFoundError:
    sys.exit(f"Error: File {filename} not found")
except ValueError as e:
    sys.exit(f"Error: Invalid file format - {e}")

# Don't: Catch all exceptions
try:
    result = parse_file(filename)
except:  # Bad!
    pass
```

#### Comments

```python
# Good: Explain WHY, not WHAT
# Filter out genes below threshold to reduce false positives
filtered = [g for g in genes if g.score >= threshold]

# Bad: State the obvious
# Loop through genes
for gene in genes:
    pass
```

## Testing Guidelines

### Test Structure

Tests are in `scagaire/tests/`:
```
scagaire/tests/
├── data/           # Test data files
├── *_test.py      # Test modules
```

### Writing Tests

```python
import unittest
from scagaire.MyModule import MyClass

class TestMyClass(unittest.TestCase):
    """Tests for MyClass."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = "test_data.txt"
    
    def test_basic_functionality(self):
        """Test basic use case."""
        obj = MyClass(self.test_data)
        result = obj.method()
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Test edge case handling."""
        # Test code here
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        # Cleanup code here
        pass
```

### Test Guidelines

1. **One test per behavior**: Each test should test one specific behavior
2. **Descriptive names**: Use clear, descriptive test names
3. **Test data**: Place test data in `scagaire/tests/data/`
4. **Independence**: Tests should not depend on each other
5. **Coverage**: Aim for ≥80% code coverage
6. **Edge cases**: Test boundary conditions and error cases

### Running Tests

```bash
# Run all tests
python3 -m unittest discover -s scagaire/tests/ -v

# Run specific test file
python3 -m unittest scagaire/tests/Scagaire_test.py

# Run specific test case
python3 -m unittest scagaire/tests/Scagaire_test.TestScagaire.test_abricate097_staph

# Run with coverage
coverage run -m unittest discover -s scagaire/tests/
coverage report
coverage html  # Generate HTML report
```

## Documentation

### Documentation Requirements

All contributions should include:

1. **Code comments**: For complex logic
2. **Docstrings**: For all public classes/functions
3. **README updates**: If changing user-facing features
4. **User guide updates**: For new features
5. **API documentation**: For new modules/classes

### Documentation Style

- Use Markdown for documentation files
- Keep line length ≤100 characters for readability
- Use code blocks with language specification
- Include examples for complex features

## Submitting Changes

### Pull Request Process

1. **Update your branch**:
   ```bash
   git checkout master
   git pull upstream master
   git checkout feature/your-feature
   git rebase master
   ```

2. **Push changes**:
   ```bash
   git push origin feature/your-feature
   ```

3. **Create pull request** on GitHub:
   - Provide clear title and description
   - Reference related issues
   - List changes made
   - Include any breaking changes
   - Add screenshots for UI changes

4. **Respond to reviews**:
   - Address reviewer comments
   - Push updates to same branch
   - Request re-review when ready

### Pull Request Template

```markdown
## Description
Brief description of changes

## Related Issues
Fixes #123
Related to #456

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Code coverage ≥80%
- [ ] Manual testing completed

## Documentation
- [ ] Code comments added
- [ ] Docstrings updated
- [ ] User guide updated (if applicable)
- [ ] README updated (if applicable)

## Breaking Changes
None / List any breaking changes
```

## Reporting Bugs

### Before Reporting

1. Check if bug already reported
2. Verify with latest version
3. Collect reproduction steps
4. Gather system information

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.8.5]
- Scagaire version: [e.g., 1.0.0]
- Installation method: [conda/pip/docker]

## Additional Context
Any other relevant information
```

## Feature Requests

### Proposing Features

1. Check existing feature requests
2. Describe use case and rationale
3. Provide examples of expected behavior
4. Consider implementation complexity

### Feature Request Template

```markdown
## Feature Description
Clear description of proposed feature

## Use Case
Why is this feature needed?
Who would benefit?

## Proposed Solution
How should this work?

## Alternatives Considered
Other approaches considered

## Additional Context
Examples, mockups, or references
```

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Issues**: Check existing issues or create new one
- **Email**: Contact maintainers (see AUTHORS file)
- **Documentation**: Review docs/ directory

## Recognition

Contributors are recognized in:
- AUTHORS file
- Release notes
- GitHub contributors page

Thank you for contributing to Scagaire!
