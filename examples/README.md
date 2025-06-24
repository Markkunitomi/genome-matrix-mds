# Examples

This directory contains examples to help you get started with genome-matrix-mds.

## 🚀 Quick Start for Beginners

### Option 1: Run the Example Script (Recommended)

The easiest way to get started is to run our example script with synthetic data:

```bash
# Navigate to the examples directory
cd examples

# Run the basic usage example
python basic_usage.py
```

This will:
- Generate synthetic genomic data automatically
- Run MDS analysis and create plots
- Perform DBSCAN clustering 
- Optimize clustering parameters
- Save all results to files

**No data files needed!** - The script creates example data for you.

### Option 2: Command Line Interface

If you prefer command-line tools:

```bash
# Create MDS plot with example data
genome-mds mds ../Data/your_matrix.dist --output my_plot.png

# Run clustering analysis
genome-mds dbscan ../Data/your_matrix.dist --epsilon 0.1 --min-samples 5
```

See [cli_examples.md](cli_examples.md) for detailed CLI usage.

## 📁 Files in This Directory

- **`basic_usage.py`** - Complete Python example with synthetic data
- **`cli_examples.md`** - Command-line interface examples and tips
- **`README.md`** - This file

## 🎯 What You'll Learn

After running the examples, you'll understand how to:

1. **Load genomic distance data** - From files or generate synthetic data
2. **Create MDS visualizations** - See your genomes in 2D space
3. **Perform DBSCAN clustering** - Find groups of related genomes
4. **Optimize parameters** - Automatically find the best clustering settings
5. **Interpret results** - Understand homogeneity, completeness, and clustering metrics

## 📊 Expected Output

Running `basic_usage.py` creates these files:

```
📊 example_mds_plot.png           - Colorful 2D plot of your genomes
🔬 example_clustering_plot.png    - Shows clusters found by DBSCAN
📋 example_parameter_sweep.tsv    - Parameter optimization results
📈 example_summary.csv           - Summary of all analysis results
```

## 💡 Next Steps

Once you've run the examples:

1. **Try with your own data** - Replace the synthetic data with your distance matrices
2. **Experiment with parameters** - Adjust epsilon and min_samples values
3. **Explore the API** - Look at the source code to understand the functions
4. **Read the documentation** - Check the main README.md for advanced features

## 🆘 Need Help?

If you run into issues:

1. **Check your Python environment** - Make sure the package is installed
2. **Verify file paths** - Ensure your data files exist and are readable
3. **Start simple** - Use the basic_usage.py script first
4. **Check error messages** - They often contain helpful information

## 🔬 Understanding Your Results

### MDS Plots
- **Each dot = one genome**
- **Colors = different species**  
- **Distance = genetic similarity** (closer = more similar)

### Clustering Results
- **Homogeneity score** (0-1): How "pure" each cluster is
- **Completeness score** (0-1): How well species are grouped together
- **Number of clusters**: Groups found in your data
- **Outliers**: Genomes that don't fit any group

### Good Results Look Like:
- High homogeneity (>0.7) and completeness (>0.7) scores
- Number of clusters close to number of species
- Clear separation in MDS plots between different species

Happy analyzing! 🧬