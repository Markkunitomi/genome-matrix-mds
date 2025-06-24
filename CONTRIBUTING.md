# Contributing to Genome Matrix MDS

Thank you for your interest in contributing to genome-matrix-mds! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/genome-matrix-mds.git
   cd genome-matrix-mds
   ```

2. **Set up development environment**
   ```bash
   # Create conda environment
   conda create -n genome-mds-dev python=3.11
   conda activate genome-mds-dev
   
   # Install in development mode
   pip install -e ".[dev]"
   
   # Install pre-commit hooks
   pre-commit install
   ```

3. **Verify setup**
   ```bash
   # Run tests
   pytest
   
   # Run linting
   ruff check src tests
   
   # Run type checking
   mypy src
   ```

## Development Workflow

### Before Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Understand the codebase structure**
   ```
   src/genome_matrix_mds/
   ├── __init__.py          # Main package exports
   ├── clustering.py        # DBSCAN analysis
   ├── visualization.py     # MDS plotting
   ├── utils.py            # Data loading utilities
   └── cli.py              # Command-line interface
   ```

### Making Changes

1. **Write code following our standards**
   - Use type hints throughout
   - Follow the existing code style
   - Add docstrings to all public functions
   - Keep functions focused and modular

2. **Add tests for new functionality**
   ```bash
   # Tests should be in tests/ directory
   # Use descriptive test names
   # Test both success and failure cases
   ```

3. **Update documentation**
   - Update docstrings
   - Add examples if needed
   - Update README.md if adding new features

### Code Quality Standards

We use several tools to maintain code quality:

- **Ruff**: Fast Python linter
- **Black**: Code formatting
- **MyPy**: Static type checking
- **Pytest**: Testing framework

Run all checks:
```bash
make check-all
# or individually:
make lint
make type-check
make test
```

### Testing Guidelines

1. **Write tests for all new code**
   - Unit tests for individual functions
   - Integration tests for workflows
   - Use fixtures for common test data

2. **Test file naming**
   ```
   tests/
   ├── test_clustering.py
   ├── test_visualization.py
   ├── test_utils.py
   └── conftest.py  # Shared fixtures
   ```

3. **Example test structure**
   ```python
   def test_function_name():
       # Arrange
       input_data = create_test_data()
       
       # Act
       result = function_under_test(input_data)
       
       # Assert
       assert result.is_valid()
       assert len(result) == expected_length
   ```

## Types of Contributions

### Bug Fixes

1. **Create an issue first** (unless it's a trivial fix)
2. **Include test case** that reproduces the bug
3. **Fix the bug** and ensure test passes
4. **Update documentation** if needed

### New Features

1. **Discuss the feature** in an issue first
2. **Design the API** - consider usability and consistency
3. **Implement with tests** - comprehensive test coverage
4. **Document thoroughly** - docstrings, examples, CLI help
5. **Update examples** if the feature affects user workflows

### Documentation Improvements

- Fix typos, improve clarity
- Add examples and use cases
- Improve installation instructions
- Add troubleshooting guides

## Submitting Changes

### Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest
   ```

2. **Ensure code quality checks pass**
   ```bash
   ruff check src tests
   mypy src
   ```

3. **Update the changelog** (if significant change)

4. **Create pull request**
   - Use the provided PR template
   - Write clear description of changes
   - Link to related issues
   - Add screenshots for UI changes

5. **Respond to review feedback**
   - Address all comments
   - Make requested changes
   - Ask for clarification if needed

### Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb in present tense
- Reference issues when applicable

```bash
# Good examples:
git commit -m "Add silhouette analysis to clustering module"
git commit -m "Fix memory leak in distance matrix loading"
git commit -m "Update CLI help text for MDS command"

# Reference issues:
git commit -m "Fix clustering crash with small datasets (fixes #123)"
```

## Getting Help

- **Questions**: Open a discussion or issue
- **Bug reports**: Use the bug report template
- **Feature requests**: Use the feature request template
- **General help**: Check the examples/ directory

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and contribute
- Focus on what's best for the community

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing to genome-matrix-mds! 🧬