"""Utility functions for data loading and processing."""

from typing import Dict, List, Tuple, Optional, Union, Any
import pickle
import pandas as pd
import numpy as np
from pathlib import Path


class DataLoader:
    """Load and process genomic distance matrices and metadata."""
    
    def __init__(self, data_dir: Union[str, Path] = "Data") -> None:
        """
        Initialize data loader.
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir)
    
    def load_distance_matrix(
        self,
        filename: str,
        remove_query_column: bool = True,
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        Load distance matrix from file.
        
        Args:
            filename: Name of distance matrix file
            remove_query_column: Whether to remove the #query column
            
        Returns:
            Tuple of (distance_matrix_df, sample_indices)
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Distance matrix file not found: {filepath}")
        
        df = pd.read_table(filepath)
        
        if remove_query_column and "#query" in df.columns:
            df = df.drop("#query", axis=1)
        
        indices = list(df.columns)
        
        return df, indices
    
    def load_metadata(
        self,
        filename: str = "Genome_metadata.tsv",
    ) -> pd.DataFrame:
        """
        Load genome metadata.
        
        Args:
            filename: Name of metadata file
            
        Returns:
            Metadata DataFrame
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Metadata file not found: {filepath}")
        
        return pd.read_table(filepath)
    
    def load_pickle_data(
        self,
        filename: str,
    ) -> Any:
        """
        Load pickled data.
        
        Args:
            filename: Name of pickle file
            
        Returns:
            Unpickled data
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Pickle file not found: {filepath}")
        
        with open(filepath, 'rb') as handle:
            return pickle.load(handle)
    
    def create_taxonomy_mappings(
        self,
        metadata_df: pd.DataFrame,
        accession_col: str = "accession",
        species_col: str = "species",
        genus_col: str = "genus",
        family_col: str = "family",
    ) -> Dict[str, Dict[str, str]]:
        """
        Create taxonomy mapping dictionaries.
        
        Args:
            metadata_df: Metadata DataFrame
            accession_col: Column name for accessions
            species_col: Column name for species
            genus_col: Column name for genus
            family_col: Column name for family
            
        Returns:
            Dictionary with taxonomy mappings
        """
        mappings = {
            'species': dict(zip(metadata_df[accession_col], metadata_df[species_col])),
            'genus': dict(zip(metadata_df[accession_col], metadata_df[genus_col])),
            'family': dict(zip(metadata_df[accession_col], metadata_df[family_col]))
        }
        
        return mappings
    
    def filter_distance_matrix(
        self,
        distance_df: pd.DataFrame,
        sample_indices: List[str],
        target_accessions: List[str],
    ) -> Tuple[pd.DataFrame, List[str], List[int]]:
        """
        Filter distance matrix to include only target accessions.
        
        Args:
            distance_df: Full distance matrix DataFrame
            sample_indices: All sample indices
            target_accessions: Target accessions to keep
            
        Returns:
            Tuple of (filtered_df, filtered_indices, positions)
        """
        positions = []
        filtered_indices = []
        
        for acc in target_accessions:
            if acc in sample_indices:
                pos = sample_indices.index(acc)
                positions.append(pos)
                filtered_indices.append(acc)
        
        if not positions:
            raise ValueError("No target accessions found in distance matrix")
        
        # Filter both rows and columns
        filtered_df = distance_df.iloc[positions, positions]
        
        return filtered_df, filtered_indices, positions
    
    def prepare_labels(
        self,
        accessions: List[str],
        taxonomy_mappings: Dict[str, Dict[str, str]],
        taxonomic_level: str = "species",
    ) -> List[str]:
        """
        Prepare taxonomic labels for accessions.
        
        Args:
            accessions: List of accession IDs
            taxonomy_mappings: Taxonomy mapping dictionaries
            taxonomic_level: Level of taxonomy (species, genus, family)
            
        Returns:
            List of taxonomic labels
        """
        if taxonomic_level not in taxonomy_mappings:
            raise ValueError(f"Taxonomic level '{taxonomic_level}' not available")
        
        mapping = taxonomy_mappings[taxonomic_level]
        labels = []
        
        for acc in accessions:
            if acc in mapping:
                labels.append(mapping[acc])
            else:
                labels.append("Unknown")
        
        return labels
    
    def save_processed_data(
        self,
        data: Any,
        filename: str,
        output_dir: Union[str, Path] = "processed_data",
    ) -> None:
        """
        Save processed data to pickle file.
        
        Args:
            data: Data to save
            filename: Output filename
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        filepath = output_path / filename
        
        with open(filepath, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def validate_data_consistency(
        self,
        distance_matrix: pd.DataFrame,
        accessions: List[str],
        taxonomy_mappings: Dict[str, Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Validate data consistency across inputs.
        
        Args:
            distance_matrix: Distance matrix DataFrame
            accessions: List of accessions
            taxonomy_mappings: Taxonomy mappings
            
        Returns:
            Validation report dictionary
        """
        report = {
            'matrix_shape': distance_matrix.shape,
            'n_accessions': len(accessions),
            'accessions_in_mappings': {},
            'missing_accessions': {},
            'warnings': []
        }
        
        # Check if matrix is square
        if distance_matrix.shape[0] != distance_matrix.shape[1]:
            report['warnings'].append("Distance matrix is not square")
        
        # Check accession coverage in taxonomy mappings
        for level, mapping in taxonomy_mappings.items():
            found = sum(1 for acc in accessions if acc in mapping)
            missing = [acc for acc in accessions if acc not in mapping]
            
            report['accessions_in_mappings'][level] = found
            report['missing_accessions'][level] = missing
            
            if missing:
                report['warnings'].append(
                    f"Missing {len(missing)} accessions in {level} mapping"
                )
        
        return report


def load_example_data() -> Dict[str, Any]:
    """
    Load example data for testing and demonstrations.
    
    Returns:
        Dictionary with example datasets
    """
    # This would be used for testing and examples
    np.random.seed(42)
    
    # Generate synthetic distance matrix
    n_samples = 50
    n_species = 5
    
    # Create block-structured distance matrix
    distance_matrix = np.random.rand(n_samples, n_samples)
    distance_matrix = (distance_matrix + distance_matrix.T) / 2  # Make symmetric
    np.fill_diagonal(distance_matrix, 0)  # Diagonal should be zero
    
    # Generate sample labels
    accessions = [f"sample_{i:03d}" for i in range(n_samples)]
    species_labels = [f"Species_{i % n_species + 1}" for i in range(n_samples)]
    genus_labels = [f"Genus_{(i // 5) % 3 + 1}" for i in range(n_samples)]
    family_labels = [f"Family_{(i // 15) % 2 + 1}" for i in range(n_samples)]
    
    taxonomy_mappings = {
        'species': dict(zip(accessions, species_labels)),
        'genus': dict(zip(accessions, genus_labels)),
        'family': dict(zip(accessions, family_labels))
    }
    
    return {
        'distance_matrix': distance_matrix,
        'accessions': accessions,
        'taxonomy_mappings': taxonomy_mappings,
        'species_labels': species_labels,
        'genus_labels': genus_labels,
        'family_labels': family_labels
    }