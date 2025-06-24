# Command Line Interface Examples

This guide shows how to use the `genome-mds` command-line tool for common genomic analysis tasks.

## Prerequisites

Make sure the package is installed:
```bash
pip install genome-matrix-mds
# or for development:
pip install -e .
```

## Quick Start

### 1. Basic MDS Plot

Create a 2D visualization of your distance matrix:

```bash
genome-mds mds your_distance_matrix.dist
```

This creates `mds_plot.png` showing your samples in 2D space.

### 2. MDS with Metadata

Include taxonomic information for colored plots:

```bash
genome-mds mds distance_matrix.dist \
  --metadata genome_metadata.tsv \
  --output my_mds_plot.png
```

### 3. DBSCAN Clustering

Find clusters in your genomic data:

```bash
genome-mds dbscan distance_matrix.dist \
  --epsilon 0.1 \
  --min-samples 5 \
  --output clustering_results
```

### 4. Parameter Optimization

Find the best clustering parameters automatically:

```bash
genome-mds sweep distance_matrix.dist \
  --eps-range 0.01 0.3 0.01 \
  --min-samples-range 3 10 1 \
  --output parameter_sweep_results
```

## Real-World Examples

### Example 1: Bacterial Genome Analysis

```bash
# Step 1: Visualize bacterial genomes
genome-mds mds bacterial_genomes.dist \
  --metadata bacterial_metadata.tsv \
  --output bacterial_mds.png \
  --data-dir /path/to/data

# Step 2: Find optimal clusters
genome-mds sweep bacterial_genomes.dist \
  --eps-range 0.05 0.2 0.01 \
  --min-samples-range 3 8 1 \
  --metadata bacterial_metadata.tsv \
  --output bacterial_sweep

# Step 3: Run clustering with optimal parameters
genome-mds dbscan bacterial_genomes.dist \
  --epsilon 0.12 \
  --min-samples 5 \
  --metadata bacterial_metadata.tsv \
  --output bacterial_clusters
```

### Example 2: Viral Sequence Analysis

```bash
# Quick viral genome clustering
genome-mds dbscan viral_distances.dist \
  --epsilon 0.08 \
  --min-samples 3 \
  --metadata viral_taxonomy.tsv \
  --output viral_analysis
```

### Example 3: Large Dataset Analysis

```bash
# For large datasets, use parameter sweep first
genome-mds sweep large_genome_matrix.dist \
  --eps-range 0.01 0.5 0.02 \
  --min-samples-range 5 20 2 \
  --output large_dataset_sweep

# Then use the best parameters found
genome-mds dbscan large_genome_matrix.dist \
  --epsilon 0.15 \
  --min-samples 8 \
  --output large_dataset_clusters
```

## File Formats

### Distance Matrix Format
```
#query	genome_001	genome_002	genome_003
genome_001	0.000	0.123	0.456
genome_002	0.123	0.000	0.234
genome_003	0.456	0.234	0.000
```

### Metadata Format
```
accession	species	genus	family
genome_001	Escherichia coli	Escherichia	Enterobacteriaceae
genome_002	Salmonella enterica	Salmonella	Enterobacteriaceae
genome_003	Listeria monocytogenes	Listeria	Listeriaceae
```

## Understanding the Output

### MDS Plots
- **Points**: Each point represents one genome
- **Colors**: Different colors represent different species/taxa
- **Proximity**: Closer points are more genetically similar

### DBSCAN Results
- **Clusters**: Groups of related genomes
- **Outliers**: Genomes that don't fit any cluster (shown in black)
- **Metrics**: 
  - Homogeneity: How pure each cluster is (0-1, higher is better)
  - Completeness: How well species are grouped (0-1, higher is better)

### Parameter Sweep
- **TSV file**: Contains results for all parameter combinations
- **Optimal parameters**: Automatically identified based on target cluster count

## Tips for Success

1. **Start simple**: Use default parameters first
2. **Visualize first**: Always create MDS plots before clustering
3. **Optimize parameters**: Use parameter sweep for best results
4. **Check metadata**: Ensure your metadata file matches your distance matrix
5. **Interpret results**: Low homogeneity might indicate you need different parameters

## Troubleshooting

### Common Issues

**"File not found"**
```bash
# Make sure file paths are correct
ls -la your_distance_matrix.dist
```

**"No clusters found"**
```bash
# Try smaller epsilon values
genome-mds dbscan your_matrix.dist --epsilon 0.05 --min-samples 3
```

**"Too many small clusters"**
```bash
# Try larger epsilon or min-samples values
genome-mds dbscan your_matrix.dist --epsilon 0.2 --min-samples 8
```

**"Memory issues with large datasets"**
```bash
# For very large matrices, consider subsampling first
# Or use a machine with more RAM
```

## Getting Help

```bash
# General help
genome-mds --help

# Command-specific help
genome-mds mds --help
genome-mds dbscan --help
genome-mds sweep --help
```