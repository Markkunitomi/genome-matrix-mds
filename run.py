#!/usr/bin/env python3
"""
Quick start script for genome-matrix-mds.

This is the simplest way to get started - just run this file!
"""

import subprocess
import sys

def main():
    print("🧬 Genome Matrix MDS - Quick Start")
    print("=" * 35)
    print()
    print("This will run a complete example analysis with synthetic data.")
    print("No installation or data files required!")
    print()
    
    response = input("Continue? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Goodbye! 👋")
        return
    
    print("\n" + "="*50)
    
    # Run the example
    try:
        result = subprocess.run([sys.executable, "main.py", "example"], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n" + "="*50)
            print("🎉 SUCCESS! Check these files:")
            print("   📊 mds_example.png - Your genomic data visualization")
            print("   🔬 dbscan_example.png - Clustering results")
            print()
            print("💡 Next steps:")
            print("   - Open the PNG files to see your results")
            print("   - Try: python main.py --help")
            print("   - Check the examples/ directory for more")
        else:
            print("❌ Something went wrong. Check the error messages above.")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()