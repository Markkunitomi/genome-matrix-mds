"""Tests for clustering module."""

import pytest
import numpy as np
from unittest.mock import patch, mock_open

from genome_matrix_mds.clustering import DBSCANAnalyzer


class TestDBSCANAnalyzer:
    """Test DBSCANAnalyzer class."""
    
    def test_init(self):
        """Test DBSCANAnalyzer initialization."""
        analyzer = DBSCANAnalyzer()
        assert analyzer.results == {}
    
    def test_run_dbscan(self, sample_distance_matrix, sample_labels):
        """Test single DBSCAN run."""
        analyzer = DBSCANAnalyzer()
        
        stats, labels = analyzer.run_dbscan(
            sample_distance_matrix,
            np.array(sample_labels),
            epsilon=0.3,
            min_samples=3
        )
        
        # Check return types
        assert isinstance(stats, list)
        assert isinstance(labels, np.ndarray)
        assert len(stats) == 9  # Number of statistics returned
        assert len(labels) == len(sample_labels)
        
        # Check statistics are reasonable
        assert stats[0] == 3  # min_samples
        assert stats[1] == 0.3  # epsilon
        assert isinstance(stats[2], (int, np.integer))  # n_clusters
        assert isinstance(stats[3], (int, np.integer))  # n_outliers
        assert 0 <= stats[4] <= 1  # homogeneity_score
        assert 0 <= stats[5] <= 1  # completeness_score
    
    def test_run_parameter_sweep(self, sample_distance_matrix, sample_labels):
        """Test parameter sweep functionality."""
        analyzer = DBSCANAnalyzer()
        
        stats_list, all_labels = analyzer.run_parameter_sweep(
            sample_distance_matrix,
            np.array(sample_labels),
            epsilon_range=(0.1, 0.3, 0.1),
            min_samples_range=(2, 4, 1)
        )
        
        # Should have 3 epsilon values * 3 min_samples values = 9 combinations
        expected_combinations = 3 * 3
        assert len(stats_list) == expected_combinations
        assert len(all_labels) == expected_combinations
        
        # Check each result
        for stats, labels in zip(stats_list, all_labels):
            assert len(stats) == 9
            assert len(labels) == len(sample_labels)
    
    def test_calculate_silhouette_scores(self, sample_distance_matrix):
        """Test silhouette score calculation."""
        analyzer = DBSCANAnalyzer()
        
        # Create some dummy cluster labels
        labels1 = np.array([0, 0, 1, 1, 2, 2] + [0] * 14)  # Valid clustering
        labels2 = np.array([0] * 20)  # All same cluster (invalid)
        all_labels = [labels1, labels2]
        
        scores = analyzer.calculate_silhouette_scores(sample_distance_matrix, all_labels)
        
        assert len(scores) == 2
        assert isinstance(scores[0], float)
        assert scores[1] == -1.0  # Invalid clustering
    
    def test_find_optimal_parameters(self):
        """Test finding optimal parameters."""
        analyzer = DBSCANAnalyzer()
        
        # Create mock statistics (min_samples, epsilon, n_clusters, ...)
        stats_list = [
            [3, 0.1, 5, 2, 0.8, 0.7, 0.75, 0.6, 0.65],  # 5 clusters
            [3, 0.2, 4, 1, 0.85, 0.8, 0.82, 0.7, 0.75],  # 4 clusters (target)
            [4, 0.1, 6, 3, 0.75, 0.65, 0.7, 0.55, 0.6],   # 6 clusters
            [4, 0.2, 4, 0, 0.9, 0.85, 0.87, 0.8, 0.82],   # 4 clusters (target)
        ]
        
        optimal_params = analyzer.find_optimal_parameters(stats_list, target_clusters=4)
        
        # Should return parameters that produce 4 clusters
        expected_params = [(0.2, 3), (0.2, 4)]  # (epsilon, min_samples)
        assert len(optimal_params) == 2
        assert set(optimal_params) == set(expected_params)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_save_results(self, mock_writer, mock_file):
        """Test saving results to file."""
        analyzer = DBSCANAnalyzer()
        
        stats_list = [
            [3, 0.1, 5, 2, 0.8, 0.7, 0.75, 0.6, 0.65],
            [3, 0.2, 4, 1, 0.85, 0.8, 0.82, 0.7, 0.75],
        ]
        
        analyzer.save_results(stats_list, "/test/path", "test_prefix")
        
        # Check file was opened correctly
        mock_file.assert_called_once_with("/test/path/test_prefix.tsv", 'w', newline='')
        
        # Check writer was created and used
        mock_writer.assert_called_once()
        writer_instance = mock_writer.return_value
        
        # Should write header + 2 data rows
        assert writer_instance.writerow.call_count == 3
    
    def test_run_dbscan_edge_cases(self, sample_distance_matrix):
        """Test DBSCAN with edge cases."""
        analyzer = DBSCANAnalyzer()
        
        # Test with very high epsilon (should create few clusters)
        labels_all_same = ["Species_1"] * 20
        stats, labels = analyzer.run_dbscan(
            sample_distance_matrix,
            np.array(labels_all_same),
            epsilon=1.0,
            min_samples=2
        )
        
        # Should have few clusters with high epsilon
        assert stats[2] <= 5  # n_clusters should be small
        
        # Test with very low epsilon (should create many small clusters/outliers)
        stats, labels = analyzer.run_dbscan(
            sample_distance_matrix,
            np.array(labels_all_same),
            epsilon=0.01,
            min_samples=2
        )
        
        # Should have many outliers with very low epsilon
        assert stats[3] > 0  # n_outliers should be > 0