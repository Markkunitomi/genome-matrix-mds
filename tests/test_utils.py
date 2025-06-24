"""Tests for utils module."""

import pytest
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from genome_matrix_mds.utils import DataLoader, load_example_data


class TestDataLoader:
    """Test DataLoader class."""
    
    def test_init(self):
        """Test DataLoader initialization."""
        loader = DataLoader()
        assert loader.data_dir == Path("Data")
        
        # Test custom data directory
        custom_loader = DataLoader("custom_data")
        assert custom_loader.data_dir == Path("custom_data")
    
    @patch('pandas.read_table')
    @patch('pathlib.Path.exists')
    def test_load_distance_matrix(self, mock_exists, mock_read_table):
        """Test distance matrix loading."""
        mock_exists.return_value = True
        
        # Create mock DataFrame
        mock_df = pd.DataFrame({
            '#query': ['sample_1', 'sample_2'],
            'sample_1': [0.0, 0.5],
            'sample_2': [0.5, 0.0]
        })
        mock_read_table.return_value = mock_df
        
        loader = DataLoader()
        df, indices = loader.load_distance_matrix("test_matrix.dist")
        
        # Check that #query column was removed
        assert '#query' not in df.columns
        assert indices == ['sample_1', 'sample_2']
        
        # Test without removing query column
        df, indices = loader.load_distance_matrix("test_matrix.dist", remove_query_column=False)
        mock_read_table.assert_called()
    
    @patch('pathlib.Path.exists')
    def test_load_distance_matrix_file_not_found(self, mock_exists):
        """Test error handling when distance matrix file doesn't exist."""
        mock_exists.return_value = False
        
        loader = DataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_distance_matrix("nonexistent.dist")
    
    @patch('pandas.read_table')
    @patch('pathlib.Path.exists')
    def test_load_metadata(self, mock_exists, mock_read_table):
        """Test metadata loading."""
        mock_exists.return_value = True
        
        mock_df = pd.DataFrame({
            'accession': ['ACC_001', 'ACC_002'],
            'species': ['Species_1', 'Species_2'],
            'genus': ['Genus_1', 'Genus_1']
        })
        mock_read_table.return_value = mock_df
        
        loader = DataLoader()
        result = loader.load_metadata()
        
        assert isinstance(result, pd.DataFrame)
        mock_read_table.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_load_metadata_file_not_found(self, mock_exists):
        """Test error handling when metadata file doesn't exist."""
        mock_exists.return_value = False
        
        loader = DataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_metadata("nonexistent.tsv")
    
    @patch('builtins.open', new_callable=mock_open, read_data=b'test_data')
    @patch('pickle.load')
    @patch('pathlib.Path.exists')
    def test_load_pickle_data(self, mock_exists, mock_pickle_load, mock_file):
        """Test pickle data loading."""
        mock_exists.return_value = True
        mock_pickle_load.return_value = {'test': 'data'}
        
        loader = DataLoader()
        result = loader.load_pickle_data("test.pkl")
        
        assert result == {'test': 'data'}
        mock_pickle_load.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_load_pickle_data_file_not_found(self, mock_exists):
        """Test error handling when pickle file doesn't exist."""
        mock_exists.return_value = False
        
        loader = DataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_pickle_data("nonexistent.pkl")
    
    def test_create_taxonomy_mappings(self, sample_metadata_df):
        """Test taxonomy mappings creation."""
        loader = DataLoader()
        
        mappings = loader.create_taxonomy_mappings(sample_metadata_df)
        
        assert 'species' in mappings
        assert 'genus' in mappings
        assert 'family' in mappings
        
        # Check mapping structure
        assert len(mappings['species']) == len(sample_metadata_df)
        assert mappings['species']['ACC_000'] == 'Species_1'
        assert mappings['genus']['ACC_000'] == 'Genus_1'
        assert mappings['family']['ACC_000'] == 'Family_1'
    
    def test_filter_distance_matrix(self, distance_dataframe, sample_accessions):
        """Test distance matrix filtering."""
        loader = DataLoader()
        
        # Filter to first 10 accessions
        target_accessions = sample_accessions[:10]
        
        filtered_df, filtered_indices, positions = loader.filter_distance_matrix(
            distance_dataframe,
            sample_accessions,
            target_accessions
        )
        
        assert len(filtered_indices) == 10
        assert filtered_df.shape == (10, 10)
        assert len(positions) == 10
        assert positions == list(range(10))
    
    def test_filter_distance_matrix_no_matches(self, distance_dataframe, sample_accessions):
        """Test error handling when no target accessions are found."""
        loader = DataLoader()
        
        # Use accessions that don't exist in the matrix
        target_accessions = ['NONEXISTENT_001', 'NONEXISTENT_002']
        
        with pytest.raises(ValueError):
            loader.filter_distance_matrix(
                distance_dataframe,
                sample_accessions,
                target_accessions
            )
    
    def test_prepare_labels(self, taxonomy_mappings):
        """Test label preparation."""
        loader = DataLoader()
        
        accessions = ['ACC_000', 'ACC_001', 'ACC_002']
        
        # Test species labels
        species_labels = loader.prepare_labels(accessions, taxonomy_mappings, 'species')
        assert len(species_labels) == 3
        assert species_labels[0] == 'Species_1'
        
        # Test genus labels
        genus_labels = loader.prepare_labels(accessions, taxonomy_mappings, 'genus')
        assert genus_labels[0] == 'Genus_1'
        
        # Test unknown accession
        accessions_with_unknown = accessions + ['UNKNOWN_ACC']
        labels = loader.prepare_labels(accessions_with_unknown, taxonomy_mappings, 'species')
        assert labels[-1] == 'Unknown'
    
    def test_prepare_labels_invalid_level(self, taxonomy_mappings):
        """Test error handling for invalid taxonomic level."""
        loader = DataLoader()
        
        with pytest.raises(ValueError):
            loader.prepare_labels(['ACC_000'], taxonomy_mappings, 'invalid_level')
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('pickle.dump')
    @patch('pathlib.Path.mkdir')
    def test_save_processed_data(self, mock_mkdir, mock_pickle_dump, mock_file):
        """Test processed data saving."""
        loader = DataLoader()
        
        test_data = {'test': 'data'}
        loader.save_processed_data(test_data, "test.pkl", "output")
        
        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_pickle_dump.assert_called_once_with(
            test_data, mock_file.return_value.__enter__.return_value, 
            protocol=pickle.HIGHEST_PROTOCOL
        )
    
    def test_validate_data_consistency(self, distance_dataframe, 
                                     sample_accessions, taxonomy_mappings):
        """Test data consistency validation."""
        loader = DataLoader()
        
        report = loader.validate_data_consistency(
            distance_dataframe,
            sample_accessions,
            taxonomy_mappings
        )
        
        assert 'matrix_shape' in report
        assert 'n_accessions' in report
        assert 'accessions_in_mappings' in report
        assert 'missing_accessions' in report
        assert 'warnings' in report
        
        assert report['matrix_shape'] == distance_dataframe.shape
        assert report['n_accessions'] == len(sample_accessions)
    
    def test_validate_data_consistency_non_square_matrix(self, sample_accessions, 
                                                        taxonomy_mappings):
        """Test validation with non-square matrix."""
        loader = DataLoader()
        
        # Create non-square matrix
        non_square_matrix = pd.DataFrame(np.random.rand(10, 15))
        
        report = loader.validate_data_consistency(
            non_square_matrix,
            sample_accessions,
            taxonomy_mappings
        )
        
        assert "Distance matrix is not square" in report['warnings']


def test_load_example_data():
    """Test example data loading."""
    data = load_example_data()
    
    assert 'distance_matrix' in data
    assert 'accessions' in data
    assert 'taxonomy_mappings' in data
    assert 'species_labels' in data
    assert 'genus_labels' in data
    assert 'family_labels' in data
    
    # Check data structure
    assert isinstance(data['distance_matrix'], np.ndarray)
    assert data['distance_matrix'].shape == (50, 50)
    assert len(data['accessions']) == 50
    assert len(data['species_labels']) == 50
    
    # Check that distance matrix is symmetric
    matrix = data['distance_matrix']
    assert np.allclose(matrix, matrix.T)
    
    # Check that diagonal is zero
    assert np.allclose(np.diag(matrix), 0)