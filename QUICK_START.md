# 🚀 Quick Start Guide

**Get started in 30 seconds - no installation required!**

## Super Simple Method

1. **Clone the repository**
   ```bash
   git clone https://github.com/Markkunitomi/genome-matrix-mds.git
   cd genome-matrix-mds
   ```

2. **Run the interactive script**
   ```bash
   python run.py
   ```
   
   That's it! 🎉

## What You Need

Just Python with these packages (most people already have them):
- numpy
- pandas 
- scikit-learn
- matplotlib

If missing, install with:
```bash
pip install -r requirements.txt
```

## What You Get

After running `python run.py`, you'll have:

- 📊 **mds_example.png** - Beautiful 2D plot of genomic relationships
- 🔬 **dbscan_example.png** - Clustering analysis results

## More Options

```bash
# Run different analyses
python main.py example          # Basic example (same as run.py)
python main.py mds data.dist    # Your own MDS analysis
python main.py dbscan data.dist # Your own clustering
python main.py --help          # See all options
```

## Using Your Own Data

Your distance matrix should be a tab-separated file like:
```
#query	sample_001	sample_002	sample_003
sample_001	0.000	0.123	0.456
sample_002	0.123	0.000	0.234
sample_003	0.456	0.234	0.000
```

Then run:
```bash
python main.py mds your_matrix.dist
```

## Need Help?

- Check the `examples/` directory
- Read the main [README.md](README.md)
- Look at the example outputs to understand the results

**Happy analyzing! 🧬**