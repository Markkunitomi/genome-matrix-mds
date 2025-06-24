"""Pytest configuration and fixtures."""

import pytest
import numpy as np
import pandas as pd
from typing import Dict, Any

from genome_matrix_mds.utils import load_example_data


@pytest.fixture
def sample_distance_matrix() -> np.ndarray:
    """Create a sample distance matrix for testing."""
    np.random.seed(42)
    n_samples = 20
    
    # Create block-structured distance matrix
    matrix = np.random.rand(n_samples, n_samples) * 0.5
    matrix = (matrix + matrix.T) / 2  # Make symmetric
    np.fill_diagonal(matrix, 0)  # Diagonal should be zero
    
    return matrix


@pytest.fixture
def sample_labels() -> list:
    """Create sample taxonomic labels."""
    n_samples = 20
    n_species = 4
    return [f"Species_{i % n_species + 1}" for i in range(n_samples)]


@pytest.fixture
def sample_accessions() -> list:
    """Create sample accession IDs."""
    return [f"ACC_{i:03d}" for i in range(20)]


@pytest.fixture
def taxonomy_mappings() -> Dict[str, Dict[str, str]]:
    """Create sample taxonomy mappings."""
    accessions = [f"ACC_{i:03d}" for i in range(20)]
    species = [f"Species_{i % 4 + 1}" for i in range(20)]
    genus = [f"Genus_{i % 2 + 1}" for i in range(20)]
    family = ["Family_1"] * 20
    
    return {
        'species': dict(zip(accessions, species)),
        'genus': dict(zip(accessions, genus)),
        'family': dict(zip(accessions, family))
    }


@pytest.fixture
def sample_metadata_df() -> pd.DataFrame:
    """Create sample metadata DataFrame."""
    n_samples = 20
    return pd.DataFrame({
        'accession': [f"ACC_{i:03d}" for i in range(n_samples)],
        'species': [f"Species_{i % 4 + 1}" for i in range(n_samples)],
        'genus': [f"Genus_{i % 2 + 1}" for i in range(n_samples)],
        'family': ["Family_1"] * n_samples,
        'other_info': [f"info_{i}" for i in range(n_samples)]
    })


@pytest.fixture
def example_data() -> Dict[str, Any]:
    """Load example data for testing."""
    return load_example_data()


@pytest.fixture
def distance_dataframe(sample_distance_matrix: np.ndarray, 
                      sample_accessions: list) -> pd.DataFrame:
    """Create a distance matrix DataFrame."""
    return pd.DataFrame(
        sample_distance_matrix,
        index=sample_accessions,
        columns=sample_accessions
    )