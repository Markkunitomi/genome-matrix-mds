# Genome Matrix MDS

A Python package for genomic distance matrix analysis and visualization using Multidimensional Scaling (MDS) and DBSCAN clustering.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- **Distance Matrix Analysis**: Load and process genomic distance matrices
- **Multidimensional Scaling (MDS)**: Visualize high-dimensional genomic relationships in 2D/3D space
- **DBSCAN Clustering**: Perform density-based clustering with parameter optimization
- **Taxonomic Visualization**: Color-coded plots by species, genus, or family
- **Parameter Sweeping**: Automated optimization of clustering parameters
- **Command-Line Interface**: Easy-to-use CLI for common workflows
- **Type-Safe**: Full type hints throughout the codebase
- **Well-Tested**: High test coverage with pytest

## Installation

### From PyPI (when published)

```bash
pip install genome-matrix-mds
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/username/genome-matrix-mds.git
cd genome-matrix-mds

# Install in development mode
pip install -e ".[dev]"

# Or use make for development setup
make dev-setup
```

## Quick Start

### Command Line Usage

#### MDS Analysis
```bash
# Basic MDS plot
genome-mds mds distance_matrix.dist --output mds_plot.png

# With metadata
genome-mds mds distance_matrix.dist --metadata genome_metadata.tsv --output mds_plot.png
```

#### DBSCAN Clustering
```bash
# Single DBSCAN run
genome-mds dbscan distance_matrix.dist --epsilon 0.1 --min-samples 5

# Parameter sweep
genome-mds sweep distance_matrix.dist --eps-range 0.01 0.2 0.01 --min-samples-range 3 10 1
```

### Python API

```python
from genome_matrix_mds import DataLoader, MDSPlotter, DBSCANAnalyzer

# Load data
loader = DataLoader("Data")
distance_df, indices = loader.load_distance_matrix("distance_matrix.dist")
metadata_df = loader.load_metadata("genome_metadata.tsv")

# Create taxonomy mappings
taxonomy_mappings = loader.create_taxonomy_mappings(metadata_df)
species_labels = loader.prepare_labels(indices, taxonomy_mappings, "species")

# Run MDS
plotter = MDSPlotter()
coordinates = plotter.run_mds(distance_df.values)

# Create and save plot
plot_df = plotter.create_mds_dataframe(coordinates, indices, species_labels)
fig = plotter.plot_mds_by_species(plot_df, save_path="mds_plot.png")

# Run DBSCAN clustering
analyzer = DBSCANAnalyzer()
stats, labels = analyzer.run_dbscan(distance_df.values, species_labels, epsilon=0.1, min_samples=5)

print(f"Number of clusters: {stats[2]}")
print(f"Homogeneity score: {stats[4]:.3f}")
```

## Data Format

### Distance Matrix
Tab-separated file with optional `#query` column:
```
#query	sample_001	sample_002	sample_003
sample_001	0.000	0.123	0.456
sample_002	0.123	0.000	0.789
sample_003	0.456	0.789	0.000
```

### Metadata
Tab-separated file with taxonomic information:
```
accession	species	genus	family
sample_001	Escherichia coli	Escherichia	Enterobacteriaceae
sample_002	Salmonella enterica	Salmonella	Enterobacteriaceae
sample_003	Listeria monocytogenes	Listeria	Listeriaceae
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
make dev-setup

# Run tests
make test

# Run tests with coverage
make test-cov

# Code formatting
make format

# Linting
make lint

# Type checking
make type-check

# Run all checks
make check-all
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=genome_matrix_mds

# Run specific test file
pytest tests/test_clustering.py

# Run with verbose output
pytest -v
```

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks for code quality

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks (`make check-all`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Citation

If you use this software in your research, please cite:

```bibtex
@software{genome_matrix_mds,
  title={Genome Matrix MDS: Genomic Distance Matrix Analysis and Visualization},
  author={Kunitomi, Mark},
  year={2024},
  url={https://github.com/username/genome-matrix-mds}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of scikit-learn for machine learning algorithms
- Visualization powered by matplotlib
- Inspired by genomic analysis workflows in bacterial taxonomy