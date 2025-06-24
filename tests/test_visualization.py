"""Tests for visualization module."""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

from genome_matrix_mds.visualization import MDSPlotter


class TestMDSPlotter:
    """Test MDSPlotter class."""
    
    def test_init(self):
        """Test MDSPlotter initialization."""
        plotter = MDSPlotter()
        assert plotter.figsize == (12, 9)
        
        # Test custom figsize
        custom_plotter = MDSPlotter(figsize=(10, 8))
        assert custom_plotter.figsize == (10, 8)
    
    def test_run_mds(self, sample_distance_matrix):
        """Test MDS computation."""
        plotter = MDSPlotter()
        
        coordinates = plotter.run_mds(sample_distance_matrix)
        
        # Check output shape
        assert coordinates.shape == (sample_distance_matrix.shape[0], 2)
        assert isinstance(coordinates, np.ndarray)
        
        # Test with different parameters
        coordinates_3d = plotter.run_mds(
            sample_distance_matrix, 
            n_components=3, 
            random_state=123
        )
        assert coordinates_3d.shape == (sample_distance_matrix.shape[0], 3)
    
    def test_create_mds_dataframe(self, sample_accessions, sample_labels):
        """Test MDS DataFrame creation."""
        plotter = MDSPlotter()
        
        # Create mock coordinates
        coordinates = np.random.rand(len(sample_accessions), 2)
        
        df = plotter.create_mds_dataframe(coordinates, sample_accessions, sample_labels)
        
        # Check DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_accessions)
        assert list(df.columns) == ['x', 'y', 'label', 'species']
        assert list(df['label']) == sample_accessions
        assert list(df['species']) == sample_labels
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.tight_layout')
    @patch('matplotlib.pyplot.subplots')
    def test_plot_mds_by_species(self, mock_subplots, mock_tight_layout, mock_savefig):
        """Test MDS plotting by species."""
        # Setup mocks
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        plotter = MDSPlotter()
        
        # Create test data
        plot_df = pd.DataFrame({
            'x': np.random.rand(20),
            'y': np.random.rand(20),
            'species': ['Species_1'] * 10 + ['Species_2'] * 10
        })
        
        result = plotter.plot_mds_by_species(
            plot_df, 
            title="Test Plot",
            save_path="test.png"
        )
        
        # Check that plot was created
        mock_subplots.assert_called_once()
        mock_ax.margins.assert_called_once_with(0.2)
        mock_ax.set_xlabel.assert_called_once_with('MDS Dimension 1')
        mock_ax.set_ylabel.assert_called_once_with('MDS Dimension 2')
        mock_ax.set_title.assert_called_once_with("Test Plot")
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with("test.png", dpi=300, bbox_inches='tight')
        
        assert result == mock_fig
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.tight_layout')
    @patch('matplotlib.pyplot.subplots')
    def test_plot_dbscan_clusters(self, mock_subplots, mock_tight_layout, mock_savefig):
        """Test DBSCAN cluster plotting."""
        # Setup mocks
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        plotter = MDSPlotter()
        
        # Create test data
        coordinates = np.random.rand(20, 2)
        cluster_labels = np.array([0, 0, 1, 1, 2, 2, -1, -1] + [0] * 12)
        core_samples_mask = np.random.choice([True, False], size=20)
        
        result = plotter.plot_dbscan_clusters(
            coordinates,
            cluster_labels,
            core_samples_mask,
            title="Test DBSCAN",
            save_path="dbscan.png"
        )
        
        # Check that plot was created
        mock_subplots.assert_called_once()
        mock_ax.set_xlabel.assert_called_once_with('MDS Dimension 1')
        mock_ax.set_ylabel.assert_called_once_with('MDS Dimension 2')
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with("dbscan.png", dpi=300, bbox_inches='tight')
        
        assert result == mock_fig
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.tight_layout')
    @patch('matplotlib.pyplot.subplots')
    def test_plot_silhouette_analysis(self, mock_subplots, mock_tight_layout, mock_savefig):
        """Test silhouette analysis plotting."""
        # Setup mocks
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        plotter = MDSPlotter()
        
        # Create test data
        distance_matrix = np.random.rand(20, 20)
        distance_matrix = (distance_matrix + distance_matrix.T) / 2
        np.fill_diagonal(distance_matrix, 0)
        
        cluster_labels = np.array([0, 0, 1, 1, 2, 2] + [0] * 14)
        
        with patch('genome_matrix_mds.visualization.silhouette_samples') as mock_silhouette:
            mock_silhouette.return_value = np.random.rand(20)
            
            result = plotter.plot_silhouette_analysis(
                distance_matrix,
                cluster_labels,
                title="Test Silhouette",
                save_path="silhouette.png"
            )
        
        # Check that plot was created
        mock_subplots.assert_called_once_with(figsize=(16, 12))
        mock_ax.set_xlabel.assert_called_once_with('Silhouette Coefficient Values')
        mock_ax.set_ylabel.assert_called_once_with('Cluster Label')
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with("silhouette.png", dpi=300, bbox_inches='tight')
        
        assert result == mock_fig
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.tight_layout')
    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.colorbar')
    def test_plot_parameter_heatmap(self, mock_colorbar, mock_subplots, 
                                   mock_tight_layout, mock_savefig):
        """Test parameter heatmap plotting."""
        # Setup mocks
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        mock_ax.imshow.return_value = MagicMock()
        
        plotter = MDSPlotter()
        
        # Create test data
        stats_df = pd.DataFrame({
            'Min_samples': [3, 3, 4, 4],
            'Epsilon': [0.1, 0.2, 0.1, 0.2],
            'Homogeneity_score': [0.8, 0.85, 0.75, 0.9]
        })
        
        result = plotter.plot_parameter_heatmap(
            stats_df,
            metric_column='Homogeneity_score',
            title="Test Heatmap",
            save_path="heatmap.png"
        )
        
        # Check that plot was created
        mock_subplots.assert_called_once()
        mock_ax.imshow.assert_called_once()
        mock_ax.set_xlabel.assert_called_once_with('Epsilon')
        mock_ax.set_ylabel.assert_called_once_with('Min Samples')
        mock_ax.set_title.assert_called_once_with("Test Heatmap")
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with("heatmap.png", dpi=300, bbox_inches='tight')
        
        assert result == mock_fig
    
    def test_plot_with_no_legend(self):
        """Test plotting with legend disabled."""
        plotter = MDSPlotter()
        
        # Create data with many species (should not show legend)
        plot_df = pd.DataFrame({
            'x': np.random.rand(50),
            'y': np.random.rand(50),
            'species': [f'Species_{i}' for i in range(50)]  # 50 different species
        })
        
        with patch('matplotlib.pyplot.subplots') as mock_subplots:
            mock_fig = MagicMock()
            mock_ax = MagicMock()
            mock_subplots.return_value = (mock_fig, mock_ax)
            
            plotter.plot_mds_by_species(plot_df, show_legend=True)
            
            # With 50 species, legend should not be called
            mock_ax.legend.assert_not_called()