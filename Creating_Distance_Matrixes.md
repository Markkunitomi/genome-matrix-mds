## Creating Distance Matrixes

Downloaded 9917 genomes from RefSeq > Bacteria > Complete  

Print full file paths

```
find /Users/charlotte.darby\@ibm.com/ncbi-genomes-2018-06-13 | grep "fna.gz" > ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt
wc -l ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt
    9917 ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt
```

Note: Dash sketch size is specified as 2^N bytes (1 Mash minimizer = 8 bytes in Dash sketch)

### Mash sketch size 1000; Dash sketch size 13

The Mash k21_s1000 sketch size (all genomes pasted) is 82.1MB

```
time Mash/mash sketch -l /Users/charlotte.darby\@ibm.com/ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt -p 6 -o refseq-genomes-mash-sketch/k21_s1000
...
Writing to refseq-genomes-mash-sketch/k21_s1000.msh...

real	13m40.256s
user	80m39.003s
sys	0m48.982s
```
 
```
time Mash/mash dist -t -p 6 refseq-genomes-mash-sketch/k21_s1000.msh refseq-genomes-mash-sketch/k21_s1000.msh > refseq-genomes-mash-sketch/mash_dist.k21.s1000.txt

real	6m4.192s
user	36m49.658s
sys	0m4.083s
```

MASH was modified to print its estimate of Jaccard similarity instead of adjusted "mash_dist"

```
time Mash/mash dist -t -j -p 6 -d 0 refseq-complete-mash-sketch-dist/k21_s1000.msh refseq-complete-mash-sketch-dist/k21_s1000.msh > refseq-complete-mash-sketch-dist/jaccard.k21.s1000.txt

real	7m1.954s
user	41m10.078s
sys	0m3.096s
```

Combined, the Dash k21_s13 sketch sizes are 79.3MB

```
time ./dash/dash sketch -k 21 -S 13 -p 6 -F ../ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt -P /Users/charlotte.darby\@ibm.com/Documents/refseq-genomes-dash-sketch/
[int bns::sketch_main(int, char**)] Unset sketch size. Setting to log2(# bits in the largest file) [20]
[W:int bns::sketch_main(int, char**)] Number of blooms provided (-1) was too small to represent the required count. Resizing to 1

real	1m53.195s
user	10m51.974s
sys	0m11.827s
```

List the names of all sketch files

```
find /Users/charlotte.darby\@ibm.com/Documents/refseq-genomes-dash-sketch | grep "21.spacing.13" > refseq-genomes-dash-sketch/SKETCHES_k21s13.txt
```

Note that Dash distance matrix has row/column names with postfix ".w.21.13.hll" and the lower triangular is "-" characters

```
time ./dash/dash dist -H -k 21 -S 13 -p 6 -O refseq-genomes-dash-sketch/jaccard_dist.k21.s13.txt -F refseq-genomes-dash-sketch/SKETCHES_k21s13.txt -o refseq-genomes-dash-sketch/jaccard_genome_sizes.k21.s13.txt

real	7m3.227s
user	41m59.891s
sys	0m5.495s
```

Dash default prints estimated Jaccard similarity but `-M` adjusts the distance in the same way as Mash does

```
time ./dash/dash dist -H -k 21 -S 13 -p 6 -O refseq-genomes-dash-sketch/mash_dist.k21.s13.txt -F refseq-genomes-dash-sketch/SKETCHES_k21s13.txt -o refseq-genomes-dash-sketch/mash_dist_genome_sizes.k21.s13.txt -M

real	7m4.963s
user	42m11.501s
sys	0m6.473s
```

### Mash sketch size 4096; Dash sketch size 15

The Mash k21_s4096 sketch size (all genomes pasted) is 327.8MB

```
time Mash/mash sketch -l /Users/charlotte.darby\@ibm.com/ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt -p 6 -s 4096 -o refseq-genomes-mash-sketch/k21_s4096


real	14m9.447s
user	83m14.252s
sys	0m52.687s
```

```
time Mash/mash dist -t -p 6 refseq-genomes-mash-sketch/k21_s4096.msh refseq-genomes-mash-sketch/k21_s4096.msh > refseq-genomes-mash-sketch/mash_dist.k21.s4096.txt

real	23m30.593s
user	141m39.646s
sys	0m4.152s
```

MASH was modified to print its estimate of Jaccard similarity instead of adjusted "mash_dist"

```
time Mash/mash dist -t -j -p 6 -d 0 refseq-complete-mash-sketch-dist/k21_s4096.msh refseq-complete-mash-sketch-dist/k21_s4096.msh > refseq-complete-mash-sketch-dist/jaccard.k21.s4096.txt
```

Combined, the Dash k21_s13 sketch sizes are 327.3MB

```
time ./dash/dash sketch -k 21 -S 15 -p 6 -F ../ncbi-genomes-2018-06-13/GENOME_FILE_NAMES.txt -P /Users/charlotte.darby\@ibm.com/Documents/refseq-genomes-dash-sketch/
[int bns::sketch_main(int, char**)] Unset sketch size. Setting to log2(# bits in the largest file) [20]
[W:int bns::sketch_main(int, char**)] Number of blooms provided (-1) was too small to represent the required count. Resizing to 1

real	1m57.571s
user	11m15.117s
sys	0m13.651s
```

Note that Dash distance matrix has row/column names with postfix ".w.21.13.hll" and the lower triangular is "-" characters

```
find /Users/charlotte.darby\@ibm.com/Documents/refseq-genomes-dash-sketch | grep "21.spacing.15" > refseq-genomes-dash-sketch/SKETCHES_k21s15.txt
```

Note that Dash distance matrix has row/column names with postfix ".w.21.13.hll" and the lower triangular is "-" characters

```
time ./dash/dash dist -H -k 21 -S 15 -p 6 -O refseq-genomes-dash-sketch/jaccard_dist.k21.s15.txt -F refseq-genomes-dash-sketch/SKETCHES_k21s15.txt -o refseq-genomes-dash-sketch/jaccard_genome_sizes.k21.s15.txt

real	27m20.252s
user	163m13.701s
sys	0m14.045s
```

Dash default prints estimated Jaccard similarity but `-M` adjusts the distance in the same way as Mash does

```
time ./dash/dash dist -H -k 21 -S 15 -p 6 -O refseq-genomes-dash-sketch/mash_dist.k21.s15.txt -F refseq-genomes-dash-sketch/SKETCHES_k21s15.txt -o refseq-genomes-dash-sketch/mash_dist_genome_sizes.k21.s15.txt -M

real	27m10.048s
user	162m5.372s
sys	0m12.245s
```