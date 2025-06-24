"""Visualization tools for genomic distance matrix analysis."""

from typing import Optional, Tuple, List, Dict, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from sklearn import manifold
from sklearn.metrics import silhouette_samples


class MDSPlotter:
    """Create MDS plots and visualizations for genomic distance matrices."""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 9)) -> None:
        """
        Initialize the MDS plotter.
        
        Args:
            figsize: Figure size for plots
        """
        self.figsize = figsize
        plt.rcParams["figure.figsize"] = figsize
    
    def run_mds(
        self,
        distance_matrix: np.ndarray,
        n_components: int = 2,
        random_state: int = 42,
    ) -> np.ndarray:
        """
        Run Multidimensional Scaling on distance matrix.
        
        Args:
            distance_matrix: Precomputed distance matrix
            n_components: Number of dimensions for MDS
            random_state: Random state for reproducibility
            
        Returns:
            MDS coordinates
        """
        mds = manifold.MDS(
            n_components=n_components,
            dissimilarity="precomputed",
            random_state=random_state
        )
        
        results = mds.fit(distance_matrix)
        return results.embedding_
    
    def create_mds_dataframe(
        self,
        coordinates: np.ndarray,
        labels: List[str],
        species: List[str],
    ) -> pd.DataFrame:
        """
        Create DataFrame for MDS plotting.
        
        Args:
            coordinates: MDS coordinates
            labels: Sample labels/accessions
            species: Species labels
            
        Returns:
            DataFrame with coordinates and metadata
        """
        df = pd.DataFrame({
            'x': coordinates[:, 0],
            'y': coordinates[:, 1],
            'label': labels,
            'species': species
        })
        
        return df
    
    def plot_mds_by_species(
        self,
        plot_df: pd.DataFrame,
        title: str = "MDS Plot by Species",
        show_legend: bool = True,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Create MDS scatter plot colored by species.
        
        Args:
            plot_df: DataFrame with x, y coordinates and species
            title: Plot title
            show_legend: Whether to show legend
            save_path: Path to save plot (optional)
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.margins(0.2)
        
        groups = plot_df.groupby('species')
        n_species = len(groups)
        
        # Use tab10 colormap for better species distinction
        colors = cm.tab10(np.linspace(0, 1, min(10, n_species)))
        if n_species > 10:
            colors = cm.viridis(np.linspace(0, 1, n_species))
        
        for i, (species, group) in enumerate(groups):
            color = colors[i % len(colors)]
            alpha = max(0.3, 1.0 / (len(group) ** 0.2))  # Adjust alpha based on group size
            
            ax.scatter(
                group['x'],
                group['y'],
                c=[color],
                label=species,
                s=80,
                alpha=alpha,
                edgecolors='black',
                linewidth=0.5
            )
        
        ax.set_xlabel('MDS Dimension 1')
        ax.set_ylabel('MDS Dimension 2')
        ax.set_title(title)
        
        if show_legend and n_species <= 20:  # Only show legend if not too many species
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_dbscan_clusters(
        self,
        coordinates: np.ndarray,
        cluster_labels: np.ndarray,
        core_samples_mask: Optional[np.ndarray] = None,
        title: str = "DBSCAN Clustering Results",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Plot DBSCAN clustering results on MDS coordinates.
        
        Args:
            coordinates: MDS coordinates
            cluster_labels: DBSCAN cluster labels
            core_samples_mask: Mask for core samples
            title: Plot title
            save_path: Path to save plot (optional)
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        unique_labels = set(cluster_labels)
        n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
        
        colors = cm.viridis(np.linspace(0, 1, len(unique_labels)))
        
        for k, color in zip(unique_labels, colors):
            if k == -1:
                # Black for noise points
                color = [0, 0, 0, 0.5]
            
            class_member_mask = (cluster_labels == k)
            
            if core_samples_mask is not None:
                # Plot core samples
                xy_core = coordinates[class_member_mask & core_samples_mask]
                ax.scatter(
                    xy_core[:, 0], xy_core[:, 1],
                    c=[color], s=100, alpha=0.8,
                    edgecolors='black', linewidth=1,
                    label=f'Cluster {k}' if k != -1 else 'Noise'
                )
                
                # Plot non-core samples
                xy_non_core = coordinates[class_member_mask & ~core_samples_mask]
                ax.scatter(
                    xy_non_core[:, 0], xy_non_core[:, 1],
                    c=[color], s=50, alpha=0.5,
                    edgecolors='black', linewidth=0.5
                )
            else:
                # Plot all samples the same way
                xy = coordinates[class_member_mask]
                ax.scatter(
                    xy[:, 0], xy[:, 1],
                    c=[color], s=80, alpha=0.8,
                    edgecolors='black', linewidth=0.5,
                    label=f'Cluster {k}' if k != -1 else 'Noise'
                )
        
        ax.set_xlabel('MDS Dimension 1')
        ax.set_ylabel('MDS Dimension 2')
        ax.set_title(f'{title}\\nEstimated number of clusters: {n_clusters}')
        
        if len(unique_labels) <= 15:  # Only show legend if not too many clusters
            ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_silhouette_analysis(
        self,
        distance_matrix: np.ndarray,
        cluster_labels: np.ndarray,
        title: str = "Silhouette Analysis",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Create silhouette analysis plot.
        
        Args:
            distance_matrix: Precomputed distance matrix
            cluster_labels: Cluster labels
            title: Plot title
            save_path: Path to save plot (optional)
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(16, 12))
        
        silhouette_vals = silhouette_samples(distance_matrix, cluster_labels, metric='precomputed')
        silhouette_avg = np.mean(silhouette_vals)
        
        unique_labels = np.unique(cluster_labels)
        unique_labels = unique_labels[unique_labels != -1]  # Remove noise cluster
        
        y_lower = 10
        colors = cm.jet(np.linspace(0, 1, len(unique_labels)))
        
        for i, (cluster_id, color) in enumerate(zip(unique_labels, colors)):
            cluster_silhouette_vals = silhouette_vals[cluster_labels == cluster_id]
            cluster_silhouette_vals.sort()
            
            size_cluster = cluster_silhouette_vals.shape[0]
            y_upper = y_lower + size_cluster
            
            ax.barh(
                range(y_lower, y_upper),
                cluster_silhouette_vals,
                height=1.0,
                edgecolor='none',
                color=color
            )
            
            # Add cluster label
            ax.text(-0.05, y_lower + 0.5 * size_cluster, str(cluster_id))
            y_lower = y_upper + 10
        
        ax.axvline(x=silhouette_avg, color="red", linestyle="--", linewidth=2)
        ax.set_xlabel('Silhouette Coefficient Values')
        ax.set_ylabel('Cluster Label')
        ax.set_title(f'{title}\\nAverage Silhouette Score: {silhouette_avg:.3f}')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_parameter_heatmap(
        self,
        stats_df: pd.DataFrame,
        metric_column: str = 'Homogeneity_score',
        title: Optional[str] = None,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Create heatmap of parameter sweep results.
        
        Args:
            stats_df: DataFrame with parameter sweep results
            metric_column: Column to use for heatmap values
            title: Plot title
            save_path: Path to save plot (optional)
            
        Returns:
            Matplotlib figure
        """
        # Pivot the data for heatmap
        pivot_df = stats_df.pivot(
            index='Min_samples',
            columns='Epsilon',
            values=metric_column
        )
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        im = ax.imshow(pivot_df.values, cmap='viridis', aspect='auto')
        
        # Set ticks and labels
        ax.set_xticks(range(len(pivot_df.columns)))
        ax.set_yticks(range(len(pivot_df.index)))
        ax.set_xticklabels([f'{x:.3f}' for x in pivot_df.columns])
        ax.set_yticklabels(pivot_df.index)
        
        ax.set_xlabel('Epsilon')
        ax.set_ylabel('Min Samples')
        
        if title is None:
            title = f'Parameter Sweep: {metric_column}'
        ax.set_title(title)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(metric_column)
        
        # Add value annotations
        for i in range(len(pivot_df.index)):
            for j in range(len(pivot_df.columns)):
                value = pivot_df.iloc[i, j]
                if not np.isnan(value):
                    text = ax.text(j, i, f'{value:.3f}', 
                                 ha="center", va="center", color="white")
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig