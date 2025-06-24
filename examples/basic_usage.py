#!/usr/bin/env python3
"""
Basic Usage Example for Genome Matrix MDS

This example shows how to use the genome-matrix-mds package for beginners.
We'll use synthetic data to demonstrate the main features.
"""

import numpy as np
import pandas as pd
from genome_matrix_mds import DataLoader, MDSPlotter, DBSCANAnalyzer
from genome_matrix_mds.utils import load_example_data

def main():
    print("🧬 Genome Matrix MDS - Basic Usage Example")
    print("=" * 50)
    
    # Step 1: Load example data (no files needed!)
    print("\n1. Loading example data...")
    data = load_example_data()
    
    distance_matrix = data['distance_matrix']
    accessions = data['accessions'] 
    species_labels = data['species_labels']
    
    print(f"   ✓ Loaded {len(accessions)} samples")
    print(f"   ✓ Found {len(set(species_labels))} species")
    print(f"   ✓ Distance matrix shape: {distance_matrix.shape}")
    
    # Step 2: Run MDS analysis
    print("\n2. Running MDS analysis...")
    plotter = MDSPlotter()
    coordinates = plotter.run_mds(distance_matrix)
    
    # Create DataFrame for plotting
    plot_df = plotter.create_mds_dataframe(coordinates, accessions, species_labels)
    print(f"   ✓ MDS coordinates computed")
    
    # Step 3: Create MDS plot
    print("\n3. Creating MDS visualization...")
    fig = plotter.plot_mds_by_species(
        plot_df, 
        title="MDS Plot - Example Genomic Data",
        save_path="example_mds_plot.png"
    )
    print("   ✓ MDS plot saved as 'example_mds_plot.png'")
    
    # Step 4: Run DBSCAN clustering
    print("\n4. Running DBSCAN clustering...")
    analyzer = DBSCANAnalyzer()
    
    # Single clustering run
    stats, cluster_labels = analyzer.run_dbscan(
        distance_matrix=distance_matrix,
        labels_true=species_labels,
        epsilon=0.3,
        min_samples=3
    )
    
    print(f"   ✓ Found {stats[2]} clusters")
    print(f"   ✓ {stats[3]} outliers detected")
    print(f"   ✓ Homogeneity score: {stats[4]:.3f}")
    print(f"   ✓ Completeness score: {stats[5]:.3f}")
    
    # Step 5: Create clustering visualization
    print("\n5. Creating clustering visualization...")
    fig = plotter.plot_dbscan_clusters(
        coordinates=coordinates,
        cluster_labels=cluster_labels,
        title="DBSCAN Clustering Results",
        save_path="example_clustering_plot.png"
    )
    print("   ✓ Clustering plot saved as 'example_clustering_plot.png'")
    
    # Step 6: Parameter optimization (optional)
    print("\n6. Finding optimal clustering parameters...")
    stats_list, all_labels = analyzer.run_parameter_sweep(
        distance_matrix=distance_matrix,
        labels_true=species_labels,
        epsilon_range=(0.1, 0.5, 0.1),    # min, max, step
        min_samples_range=(2, 6, 1)        # min, max, step
    )
    
    n_species = len(set(species_labels))
    optimal_params = analyzer.find_optimal_parameters(stats_list, target_clusters=n_species)
    
    print(f"   ✓ Target clusters: {n_species} (number of species)")
    print(f"   ✓ Best parameters found:")
    for eps, min_samples in optimal_params[:3]:  # Show top 3
        print(f"     - Epsilon: {eps:.1f}, Min samples: {min_samples}")
    
    # Step 7: Save results
    print("\n7. Saving analysis results...")
    
    # Save clustering results
    analyzer.save_results(stats_list, ".", "example_parameter_sweep")
    print("   ✓ Parameter sweep results saved as 'example_parameter_sweep.tsv'")
    
    # Create summary report
    summary = {
        'n_samples': len(accessions),
        'n_species': len(set(species_labels)),
        'n_clusters_found': stats[2],
        'n_outliers': stats[3],
        'homogeneity_score': stats[4],
        'completeness_score': stats[5],
        'best_epsilon': optimal_params[0][0] if optimal_params else 'N/A',
        'best_min_samples': optimal_params[0][1] if optimal_params else 'N/A'
    }
    
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv("example_summary.csv", index=False)
    print("   ✓ Summary saved as 'example_summary.csv'")
    
    print("\n🎉 Analysis complete! Files created:")
    print("   📊 example_mds_plot.png - MDS visualization")
    print("   🔬 example_clustering_plot.png - DBSCAN results") 
    print("   📋 example_parameter_sweep.tsv - Parameter optimization")
    print("   📈 example_summary.csv - Analysis summary")
    
    print("\n💡 Next steps:")
    print("   - Open the PNG files to view your plots")
    print("   - Check the CSV/TSV files for detailed results")
    print("   - Try with your own distance matrix files!")

if __name__ == "__main__":
    main()