# Notebook Explorations

This directory contains the original Jupyter notebooks that were used during the development and exploration phase of this project. These notebooks have been **superseded by the modern Python package** in the `src/` directory.

## 📋 **What's Here**

### **Core Analysis Notebooks**
- `Distance_matrix_to_MDS.ipynb` - Original MDS analysis implementation
- `Distance_matrix_to_MDS_analysis.ipynb` - Enhanced MDS workflow
- `Distance_matrix_to_DBSCAN_Silhouette.ipynb` - DBSCAN with silhouette analysis
- `Distance_matrix_to_DBSCAN_per_class_scoring.ipynb` - Per-class DBSCAN evaluation

### **Species-Specific Analyses**
- `Distance_matrix_to_MDS_Campylobacter.ipynb` - Campylobacter genome analysis
- `Distance_matrix_to_MDS_E_coli.ipynb` - E. coli genome analysis
- `Distance_matrix_to_MDS_Listeria.ipynb` - Listeria genome analysis
- `Distance_matrix_to_MDS_Salmonella.ipynb` - Salmonella genome analysis
- `Distance_matrix_to_MDS_Salmonella_real.ipynb` - Real Salmonella dataset analysis

### **Additional Methods**
- `Distance_matrix_to_KNN.ipynb` - K-nearest neighbors analysis
- `Distance_matrix_to_hierarchical_tree.ipynb` - Hierarchical clustering
- `Distance_matrix_to_violin_plot.ipynb` - Distance distribution visualization
- `Genome_veiwer_MDS.ipynb` - Interactive genome visualization

### **Clustering Explorations**
- `Subclusters.ipynb` - Sub-cluster analysis
- `Subclusters-Copy1.ipynb` - Alternative clustering approaches
- `Subclusters-Copy2.ipynb` - Extended clustering experiments
- `Subclusters copy.ipynb` - Backup clustering analysis

### **Reference Data**
- `refseq_complete.ipynb` - RefSeq database analysis

## 📋 **Usage Notes**

### **Two Ways to Use This Work**
1. **Modern Package** (Recommended for new projects):
   - **Command line**: `python main.py` or `python run.py`
   - **Python API**: `from genome_matrix_mds import MDSPlotter, DBSCANAnalyzer`
   - **Examples**: Check the `examples/` directory

2. **Research Notebooks** (Great for learning and exploration):
   - Step-by-step analysis workflows
   - Detailed parameter exploration
   - Species-specific case studies
   - Method comparison studies

### **Why Keep These Notebooks?**
1. **Historical record** of the development process
2. **Research insights** and experimental approaches
3. **Method validation** and comparison studies
4. **Species-specific findings** that informed the final package design

### **Dependencies**
These notebooks may require:
- Jupyter/JupyterLab
- Various Python packages (versions may be outdated)
- Original data files that may not be included

### **Data Compatibility**
Some notebooks may reference:
- Hardcoded file paths
- Specific dataset versions
- Deprecated function calls

## 🔬 **Research Value**

These notebooks contain valuable research insights including:
- **Parameter optimization studies** for different bacterial species
- **Method comparisons** between clustering algorithms
- **Validation experiments** with real genomic data
- **Visualization techniques** for genomic distance matrices

## 🚀 **Getting Started**

### **For Quick Analysis** (Recommended):
```bash
# Quick start (no installation)
python run.py

# Or use specific commands
python main.py mds your_data.dist
python main.py dbscan your_data.dist --epsilon 0.1
```

### **For Learning & Research**:
- Open any notebook to see detailed workflows
- Explore parameter optimization studies
- Understand method development process
- Compare different approaches side-by-side

See the main [README.md](../README.md) and [QUICK_START.md](../QUICK_START.md) for current usage instructions.

---

*These notebooks represent the exploratory data analysis phase that led to the development of the genome-matrix-mds package. They are preserved for historical and research reference purposes.*