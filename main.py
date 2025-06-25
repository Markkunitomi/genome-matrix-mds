#!/usr/bin/env python3
"""
Main script for genome-matrix-mds package.

This script allows you to use the package without installation.
Simply run: python main.py [command] [options]

Examples:
    python main.py mds Data/distance_matrix.dist
    python main.py dbscan Data/distance_matrix.dist --epsilon 0.1
    python main.py example
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path so we can import our modules
script_dir = Path(__file__).parent
src_dir = script_dir / "src"
sys.path.insert(0, str(src_dir))

def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    
    try:
        import sklearn
    except ImportError:
        missing_deps.append("scikit-learn")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nPlease install them with:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("   or")
        print(f"   conda install {' '.join(missing_deps)}")
        sys.exit(1)
    
    print("✅ All dependencies found!")

def run_example():
    """Run the basic usage example."""
    print("🧬 Running basic usage example...")
    
    # Import and run the example
    from genome_matrix_mds.utils import load_example_data
    from genome_matrix_mds import MDSPlotter, DBSCANAnalyzer
    
    # Load example data
    print("\n1. Loading example data...")
    data = load_example_data()
    
    distance_matrix = data['distance_matrix']
    accessions = data['accessions']
    species_labels = data['species_labels']
    
    print(f"   ✓ Loaded {len(accessions)} samples")
    print(f"   ✓ Found {len(set(species_labels))} species")
    
    # Run MDS
    print("\n2. Running MDS analysis...")
    plotter = MDSPlotter()
    coordinates = plotter.run_mds(distance_matrix)
    
    plot_df = plotter.create_mds_dataframe(coordinates, accessions, species_labels)
    fig = plotter.plot_mds_by_species(
        plot_df,
        title="MDS Plot - Example Data",
        save_path="mds_example.png"
    )
    print("   ✓ MDS plot saved as 'mds_example.png'")
    
    # Run DBSCAN
    print("\n3. Running DBSCAN clustering...")
    analyzer = DBSCANAnalyzer()
    stats, cluster_labels = analyzer.run_dbscan(
        distance_matrix,
        species_labels,
        epsilon=0.3,
        min_samples=3
    )
    
    print(f"   ✓ Found {stats[2]} clusters")
    print(f"   ✓ Homogeneity score: {stats[4]:.3f}")
    
    # Create clustering plot
    fig = plotter.plot_dbscan_clusters(
        coordinates,
        cluster_labels,
        title="DBSCAN Results - Example Data",
        save_path="dbscan_example.png"
    )
    print("   ✓ Clustering plot saved as 'dbscan_example.png'")
    
    print("\n🎉 Example complete! Check the generated PNG files.")

def main():
    """Main entry point for the script."""
    print("🧬 Genome Matrix MDS - Standalone Script")
    print("=" * 45)
    
    # Check dependencies first
    check_dependencies()
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python main.py example                     # Run example with synthetic data")
        print("  python main.py mds <distance_matrix>       # Create MDS plot")
        print("  python main.py dbscan <distance_matrix>    # Run DBSCAN clustering")
        print("  python main.py sweep <distance_matrix>     # Parameter optimization")
        print("\nExamples:")
        print("  python main.py example")
        print("  python main.py mds Data/distance_matrix.dist")
        print("  python main.py dbscan Data/distance_matrix.dist --epsilon 0.1")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "example":
        run_example()
    else:
        # Use the existing CLI module but modify sys.argv
        from genome_matrix_mds.cli import main as cli_main
        
        # Remove 'main.py' from argv and call the CLI
        sys.argv = [sys.argv[0]] + sys.argv[1:]
        cli_main()

if __name__ == "__main__":
    main()