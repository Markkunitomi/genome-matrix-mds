"""Command-line interface for genome-matrix-mds."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .clustering import DBSCANAnalyzer
from .visualization import MDSPlotter
from .utils import DataLoader


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Genomic distance matrix analysis using MDS and DBSCAN clustering"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # MDS command
    mds_parser = subparsers.add_parser("mds", help="Run MDS analysis")
    mds_parser.add_argument(
        "distance_matrix",
        help="Path to distance matrix file"
    )
    mds_parser.add_argument(
        "--metadata",
        help="Path to metadata file (default: Data/Genome_metadata.tsv)"
    )
    mds_parser.add_argument(
        "--output",
        "-o",
        default="mds_plot.png",
        help="Output plot filename"
    )
    mds_parser.add_argument(
        "--data-dir",
        default="Data",
        help="Data directory path"
    )
    
    # DBSCAN command
    dbscan_parser = subparsers.add_parser("dbscan", help="Run DBSCAN analysis")
    dbscan_parser.add_argument(
        "distance_matrix",
        help="Path to distance matrix file"
    )
    dbscan_parser.add_argument(
        "--epsilon",
        type=float,
        default=0.1,
        help="DBSCAN epsilon parameter"
    )
    dbscan_parser.add_argument(
        "--min-samples",
        type=int,
        default=5,
        help="DBSCAN min_samples parameter"
    )
    dbscan_parser.add_argument(
        "--metadata",
        help="Path to metadata file"
    )
    dbscan_parser.add_argument(
        "--output",
        "-o",
        default="dbscan_results",
        help="Output filename prefix"
    )
    dbscan_parser.add_argument(
        "--data-dir",
        default="Data",
        help="Data directory path"
    )
    
    # Parameter sweep command
    sweep_parser = subparsers.add_parser("sweep", help="Run parameter sweep")
    sweep_parser.add_argument(
        "distance_matrix",
        help="Path to distance matrix file"
    )
    sweep_parser.add_argument(
        "--eps-range",
        nargs=3,
        type=float,
        default=[0.01, 0.2, 0.01],
        help="Epsilon range: min max step"
    )
    sweep_parser.add_argument(
        "--min-samples-range",
        nargs=3,
        type=int,
        default=[3, 10, 1],
        help="Min samples range: min max step"
    )
    sweep_parser.add_argument(
        "--metadata",
        help="Path to metadata file"
    )
    sweep_parser.add_argument(
        "--output",
        "-o",
        default="parameter_sweep",
        help="Output filename prefix"
    )
    sweep_parser.add_argument(
        "--data-dir",
        default="Data",
        help="Data directory path"
    )
    
    return parser


def run_mds_analysis(args: argparse.Namespace) -> None:
    """Run MDS analysis."""
    try:
        # Load data
        loader = DataLoader(args.data_dir)
        distance_df, indices = loader.load_distance_matrix(args.distance_matrix)
        
        # Load metadata if available
        if args.metadata:
            metadata_df = loader.load_metadata(args.metadata)
            taxonomy_mappings = loader.create_taxonomy_mappings(metadata_df)
            species_labels = loader.prepare_labels(indices, taxonomy_mappings, "species")
        else:
            species_labels = [f"Sample_{i}" for i in range(len(indices))]
        
        # Run MDS
        plotter = MDSPlotter()
        coordinates = plotter.run_mds(distance_df.values)
        
        # Create plot
        plot_df = plotter.create_mds_dataframe(coordinates, indices, species_labels)
        fig = plotter.plot_mds_by_species(plot_df, save_path=args.output)
        
        print(f"MDS plot saved to: {args.output}")
        
    except Exception as e:
        print(f"Error running MDS analysis: {e}", file=sys.stderr)
        sys.exit(1)


def run_dbscan_analysis(args: argparse.Namespace) -> None:
    """Run DBSCAN analysis."""
    try:
        # Load data
        loader = DataLoader(args.data_dir)
        distance_df, indices = loader.load_distance_matrix(args.distance_matrix)
        
        # Load metadata
        if args.metadata:
            metadata_df = loader.load_metadata(args.metadata)
            taxonomy_mappings = loader.create_taxonomy_mappings(metadata_df)
            species_labels = loader.prepare_labels(indices, taxonomy_mappings, "species")
        else:
            species_labels = [f"Sample_{i}" for i in range(len(indices))]
        
        # Run DBSCAN
        analyzer = DBSCANAnalyzer()
        stats, labels = analyzer.run_dbscan(
            distance_df.values,
            species_labels,
            args.epsilon,
            args.min_samples
        )
        
        # Print results
        print("DBSCAN Results:")
        print(f"Epsilon: {args.epsilon}")
        print(f"Min samples: {args.min_samples}")
        print(f"Number of clusters: {stats[2]}")
        print(f"Number of outliers: {stats[3]}")
        print(f"Homogeneity score: {stats[4]:.3f}")
        print(f"Completeness score: {stats[5]:.3f}")
        
        # Save results
        output_file = f"{args.output}_eps{args.epsilon}_min{args.min_samples}.tsv"
        analyzer.save_results([stats], ".", args.output)
        print(f"Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error running DBSCAN analysis: {e}", file=sys.stderr)
        sys.exit(1)


def run_parameter_sweep(args: argparse.Namespace) -> None:
    """Run parameter sweep."""
    try:
        # Load data
        loader = DataLoader(args.data_dir)
        distance_df, indices = loader.load_distance_matrix(args.distance_matrix)
        
        # Load metadata
        if args.metadata:
            metadata_df = loader.load_metadata(args.metadata)
            taxonomy_mappings = loader.create_taxonomy_mappings(metadata_df)
            species_labels = loader.prepare_labels(indices, taxonomy_mappings, "species")
        else:
            species_labels = [f"Sample_{i}" for i in range(len(indices))]
        
        # Run parameter sweep
        analyzer = DBSCANAnalyzer()
        stats_list, all_labels = analyzer.run_parameter_sweep(
            distance_df.values,
            species_labels,
            epsilon_range=tuple(args.eps_range),
            min_samples_range=tuple(args.min_samples_range)
        )
        
        # Save results
        analyzer.save_results(stats_list, ".", args.output)
        
        print(f"Parameter sweep completed with {len(stats_list)} combinations")
        print(f"Results saved to: {args.output}.tsv")
        
        # Find optimal parameters
        n_species = len(set(species_labels))
        optimal_params = analyzer.find_optimal_parameters(stats_list, n_species)
        
        print(f"\\nOptimal parameters for {n_species} species:")
        for eps, min_samples in optimal_params[:5]:  # Show top 5
            print(f"  Epsilon: {eps:.3f}, Min samples: {min_samples}")
        
    except Exception as e:
        print(f"Error running parameter sweep: {e}", file=sys.stderr)
        sys.exit(1)


def main(argv: Optional[list] = None) -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "mds":
        run_mds_analysis(args)
    elif args.command == "dbscan":
        run_dbscan_analysis(args)
    elif args.command == "sweep":
        run_parameter_sweep(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()