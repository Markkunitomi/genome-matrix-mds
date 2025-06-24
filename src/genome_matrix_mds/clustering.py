"""DBSCAN clustering analysis for genomic distance matrices."""

from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.metrics import silhouette_score
import csv


class DBSCANAnalyzer:
    """Perform DBSCAN clustering analysis on genomic distance matrices."""
    
    def __init__(self) -> None:
        """Initialize the DBSCAN analyzer."""
        self.results: Dict[str, Any] = {}
    
    def run_dbscan(
        self,
        distance_matrix: np.ndarray,
        labels_true: np.ndarray,
        epsilon: float,
        min_samples: int,
    ) -> Tuple[List[Union[int, float]], np.ndarray]:
        """
        Run DBSCAN clustering on distance matrix.
        
        Args:
            distance_matrix: Precomputed distance matrix
            labels_true: True labels for evaluation
            epsilon: DBSCAN epsilon parameter
            min_samples: DBSCAN min_samples parameter
            
        Returns:
            Tuple of (statistics, cluster_labels)
        """
        db = DBSCAN(
            eps=float(epsilon), 
            min_samples=int(min_samples), 
            metric='precomputed'
        ).fit(distance_matrix)
        
        labels = db.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_outliers = np.count_nonzero(labels == -1)
        
        # Calculate clustering metrics
        homogeneity_score = metrics.homogeneity_score(labels_true, labels)
        completeness_score = metrics.completeness_score(labels_true, labels)
        v_measure = metrics.v_measure_score(labels_true, labels)
        adjusted_rand_score = metrics.adjusted_rand_score(labels_true, labels)
        adjusted_mutual_info_score = metrics.adjusted_mutual_info_score(labels_true, labels)
        
        stats = [
            min_samples,
            epsilon,
            n_clusters,
            n_outliers,
            homogeneity_score,
            completeness_score,
            v_measure,
            adjusted_rand_score,
            adjusted_mutual_info_score
        ]
        
        return stats, labels
    
    def run_parameter_sweep(
        self,
        distance_matrix: np.ndarray,
        labels_true: np.ndarray,
        epsilon_range: Tuple[float, float, float] = (0.01, 0.1, 0.001),
        min_samples_range: Tuple[int, int, int] = (5, 10, 1),
    ) -> Tuple[List[List[Any]], List[np.ndarray]]:
        """
        Run DBSCAN parameter sweep.
        
        Args:
            distance_matrix: Precomputed distance matrix
            labels_true: True labels for evaluation
            epsilon_range: (min, max, step) for epsilon parameter
            min_samples_range: (min, max, step) for min_samples parameter
            
        Returns:
            Tuple of (statistics_list, all_labels)
        """
        eps_low, eps_high, eps_step = epsilon_range
        min_low, min_high, min_step = min_samples_range
        
        all_stats = []
        all_labels = []
        
        # Convert epsilon range to integer for precise iteration
        eps_low_int = int(eps_low * 1000)
        eps_high_int = int(eps_high * 1000)
        eps_step_int = int(eps_step * 1000)
        
        for min_samples in range(min_low, min_high + min_step, min_step):
            for eps_int in range(eps_low_int, eps_high_int + eps_step_int, eps_step_int):
                epsilon = eps_int / 1000.0
                
                stats, labels = self.run_dbscan(
                    distance_matrix, labels_true, epsilon, min_samples
                )
                
                all_stats.append(stats)
                all_labels.append(labels)
        
        return all_stats, all_labels
    
    def calculate_silhouette_scores(
        self,
        distance_matrix: np.ndarray,
        all_labels: List[np.ndarray],
    ) -> List[float]:
        """
        Calculate silhouette scores for all clustering results.
        
        Args:
            distance_matrix: Precomputed distance matrix
            all_labels: List of cluster label arrays
            
        Returns:
            List of silhouette scores
        """
        silhouette_scores = []
        
        for labels in all_labels:
            if len(set(labels)) > 1:  # Need at least 2 clusters
                score = silhouette_score(distance_matrix, labels, metric='precomputed')
                silhouette_scores.append(score)
            else:
                silhouette_scores.append(-1.0)  # Invalid score
        
        return silhouette_scores
    
    def find_optimal_parameters(
        self,
        stats_list: List[List[Any]],
        target_clusters: int,
    ) -> List[Tuple[float, int]]:
        """
        Find optimal parameters based on target number of clusters.
        
        Args:
            stats_list: List of statistics from parameter sweep
            target_clusters: Target number of clusters
            
        Returns:
            List of (epsilon, min_samples) tuples that produce closest to target clusters
        """
        cluster_counts = [stats[2] for stats in stats_list]  # n_clusters is at index 2
        
        # Find parameters that produce closest to target clusters
        best_diff = float('inf')
        optimal_params = []
        
        for i, count in enumerate(cluster_counts):
            diff = abs(count - target_clusters)
            if diff < best_diff:
                best_diff = diff
                optimal_params = [(stats_list[i][1], stats_list[i][0])]  # (epsilon, min_samples)
            elif diff == best_diff:
                optimal_params.append((stats_list[i][1], stats_list[i][0]))
        
        return optimal_params
    
    def save_results(
        self,
        stats_list: List[List[Any]],
        output_path: str,
        prefix: str = "dbscan_results",
    ) -> None:
        """
        Save DBSCAN results to TSV file.
        
        Args:
            stats_list: List of statistics from parameter sweep
            output_path: Directory to save results
            prefix: Filename prefix
        """
        headers = [
            'Min_samples',
            'Epsilon',
            'N_clusters',
            'N_outliers',
            'Homogeneity_score',
            'Completeness_score',
            'V_measure',
            'Adjusted_rand_score',
            'Adjusted_mutual_info_score'
        ]
        
        filename = f"{output_path}/{prefix}.tsv"
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(headers)
            for stats in stats_list:
                writer.writerow(stats)