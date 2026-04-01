# Commands Cheat Sheet — Computational Metagenomics Workshop

## Quick Reference for Every Tool

---

## Linux Essentials

```bash
# ── Navigation ──
pwd                          # Where am I?
ls -lh                       # List files (human-readable sizes)
cd /path/to/dir              # Change directory
cd ..                        # Go up one level
cd ~                         # Go to home

# ── File Operations ──
cp source dest               # Copy file
mv source dest               # Move/rename
rm file                      # Delete (irreversible!)
rm -r directory/             # Delete directory
mkdir -p path/to/new/dir     # Create nested directories

# ── Viewing Files ──
head -n 20 file              # First 20 lines
tail -n 20 file              # Last 20 lines
less file                    # Scroll (q to quit)
wc -l file                   # Count lines
cat file                     # Print entire file

# ── Compressed Files ──
gzip file                    # Compress
gunzip file.gz               # Decompress
zcat file.gz | head          # View without decompressing

# ── Searching ──
grep "pattern" file          # Search in file
grep -c "^>" file.fasta      # Count FASTA sequences
grep -r "pattern" directory/ # Search recursively

# ── FASTQ Utilities ──
echo $(( $(wc -l < file.fastq) / 4 ))         # Count reads
echo $(( $(zcat file.fastq.gz | wc -l) / 4 )) # Count reads (compressed)
head -4 file.fastq                              # View first read

# ── System ──
top                          # Monitor CPU/memory
df -h                        # Disk space
du -sh directory/            # Directory size
nproc                        # Number of CPU cores
free -h                      # Available memory
```

---

## Conda Environment Management

```bash
conda create -n metagenomics python=3.10 -y   # Create environment
conda activate metagenomics                     # Activate
conda deactivate                                # Deactivate
conda env list                                  # List all environments
conda list                                      # List installed packages
conda install -c bioconda tool_name -y          # Install from bioconda
conda remove -n env_name --all                  # Delete environment
```

---

## Day 1: 16S Amplicon (QIIME2)

```bash
# ── Import Data ──
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path raw_reads/ \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path demux.qza

# ── Visualize Quality ──
qiime demux summarize \
  --i-data demux.qza \
  --o-visualization demux.qzv

# ── Denoise with DADA2 ──
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux.qza \
  --p-trunc-len-f 280 --p-trunc-len-r 250 \
  --p-trim-left-f 17 --p-trim-left-r 21 \
  --p-n-threads 4 \
  --o-table table.qza \
  --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats stats.qza

# ── Summarize ──
qiime feature-table summarize --i-table table.qza --o-visualization table.qzv --m-sample-metadata-file metadata.tsv
qiime feature-table tabulate-seqs --i-data rep-seqs.qza --o-visualization rep-seqs.qzv

# ── Taxonomy ──
qiime feature-classifier classify-sklearn \
  --i-classifier silva-138-99-nb-classifier.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza

qiime taxa barplot --i-table table.qza --i-taxonomy taxonomy.qza --m-metadata-file metadata.tsv --o-visualization taxa-barplot.qzv

# ── Filter ──
qiime taxa filter-table --i-table table.qza --i-taxonomy taxonomy.qza --p-exclude "mitochondria,chloroplast" --o-filtered-table filtered-table.qza

# ── Phylogenetic Tree ──
qiime alignment mafft --i-sequences rep-seqs.qza --o-alignment aligned.qza
qiime alignment mask --i-alignment aligned.qza --o-masked-alignment masked.qza
qiime phylogeny fasttree --i-alignment masked.qza --o-tree unrooted-tree.qza
qiime phylogeny midpoint-root --i-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza

# ── Diversity ──
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny rooted-tree.qza \
  --i-table filtered-table.qza \
  --p-sampling-depth 10000 \
  --m-metadata-file metadata.tsv \
  --output-dir diversity-results/

# ── Alpha Significance ──
qiime diversity alpha-group-significance --i-alpha-diversity diversity-results/shannon_vector.qza --m-metadata-file metadata.tsv --o-visualization shannon-sig.qzv

# ── Beta Significance (PERMANOVA) ──
qiime diversity beta-group-significance --i-distance-matrix diversity-results/bray_curtis_distance_matrix.qza --m-metadata-file metadata.tsv --m-metadata-column condition --p-method permanova --o-visualization permanova.qzv

# ── Export ──
qiime tools export --input-path table.qza --output-path exported/
biom convert -i exported/feature-table.biom -o exported/feature-table.tsv --to-tsv
```

---

## Day 2: Shotgun Metagenomics

### FastQC
```bash
fastqc raw_reads/*.fastq.gz --outdir fastqc_out/ --threads 4
multiqc fastqc_out/ -o multiqc_report/
```

### Trimmomatic
```bash
trimmomatic PE -phred33 -threads 4 \
  R1.fastq.gz R2.fastq.gz \
  R1_paired.fq.gz R1_unpaired.fq.gz \
  R2_paired.fq.gz R2_unpaired.fq.gz \
  ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:True \
  LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:50
```

### Kraken2
```bash
kraken2 --db /path/to/db --paired --threads 8 \
  --output sample.kraken --report sample.kreport \
  --gzip-compressed R1_paired.fq.gz R2_paired.fq.gz
```

### Bracken
```bash
bracken -d /path/to/db -i sample.kreport -o sample.bracken \
  -w sample.breport -r 150 -l S -t 10
```

### MEGAHIT (Assembly)
```bash
megahit -1 R1_paired.fq.gz -2 R2_paired.fq.gz \
  -o assembly_out --min-contig-len 1000 -t 8
```

### Read Mapping (for Binning)
```bash
bowtie2-build assembly_out/final.contigs.fa contigs_index
bowtie2 -x contigs_index -1 R1.fq.gz -2 R2.fq.gz -S mapped.sam -p 8
samtools sort -@ 8 -o mapped.sorted.bam mapped.sam
samtools index mapped.sorted.bam
```

### MetaBAT2 (Binning)
```bash
jgi_summarize_bam_contig_depths --outputDepth depth.txt mapped.sorted.bam
metabat2 -i assembly_out/final.contigs.fa -a depth.txt -o bins/bin -m 1500 -t 8
```

### MaxBin2 (Binning)
```bash
run_MaxBin.pl -contig assembly_out/final.contigs.fa \
  -reads R1_paired.fq.gz -reads2 R2_paired.fq.gz \
  -out maxbin_bins/bin -thread 8
```

### DAS Tool (Bin Refinement)
```bash
Fasta_to_Contig2Bin.sh -i bins_metabat2/ -e fa > metabat2_c2b.tsv
Fasta_to_Contig2Bin.sh -i bins_maxbin2/ -e fasta > maxbin2_c2b.tsv
DAS_Tool -i metabat2_c2b.tsv,maxbin2_c2b.tsv -l MetaBAT2,MaxBin2 \
  -c final.contigs.fa -o das_tool_out --search_engine diamond --write_bins 1 -t 8
```

### CheckM (Quality)
```bash
checkm lineage_wf bins_dir/ checkm_out/ -x fa -t 8 --tab_table -f checkm_results.tsv
# Or CheckM2:
checkm2 predict --input bins_dir/ --output-directory checkm2_out/ -x fa --threads 8
```

### GTDBTk (Taxonomy)
```bash
export GTDBTK_DATA_PATH=/path/to/gtdbtk_data/
gtdbtk classify_wf --genome_dir bins_dir/ --out_dir gtdbtk_out/ -x fa --cpus 8
```

### Prokka (Annotation)
```bash
prokka bin.fa --outdir prokka_out --prefix bin_name --kingdom Bacteria --cpus 8 --metagenome
```

### eggNOG-mapper (COGs/KEGG)
```bash
emapper.py -i proteins.faa --output cog_out -m diamond --cpu 8 --data_dir /path/to/eggnog_data/
```

---

## Day 3: Statistical Analysis (R)

### Load Data into phyloseq
```R
library(phyloseq)
ps <- phyloseq(
  otu_table(as.matrix(otu), taxa_are_rows=TRUE),
  tax_table(as.matrix(tax)),
  sample_data(meta),
  phy_tree(tree)
)
```

### Filter
```R
ps <- filter_taxa(ps, function(x) sum(x > 0) >= 0.1 * nsamples(ps), prune=TRUE)
```

### Alpha Diversity
```R
ps_rare <- rarefy_even_depth(ps, rngseed=42)
plot_richness(ps_rare, x="condition", measures=c("Observed","Shannon"))
wilcox.test(Shannon ~ condition, data=alpha_df)
```

### Beta Diversity
```R
bc <- distance(ps_rare, "bray")
pcoa <- ordinate(ps_rare, "PCoA", bc)
plot_ordination(ps_rare, pcoa, color="condition") + stat_ellipse()
adonis2(bc ~ condition, data=as(sample_data(ps_rare),"data.frame"), permutations=999)
betadisper(bc, sample_data(ps_rare)$condition) |> permutest()
```

### DESeq2 Differential Abundance
```R
library(DESeq2)
dds <- phyloseq_to_deseq2(ps, ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast=c("condition","disease","healthy"), alpha=0.05)
sig <- subset(as.data.frame(res), padj < 0.05)
```

### ALDEx2 Differential Abundance
```R
library(ALDEx2)
aldex_res <- aldex(counts, conditions, mc.samples=128, test="t", effect=TRUE)
sig <- subset(aldex_res, wi.eBH < 0.05 & abs(effect) > 1)
```

---

## File Format Quick Reference

| What | Extension | Description |
|------|-----------|-------------|
| Raw reads | `.fastq.gz` | Sequences + quality scores (compressed) |
| Reference sequences | `.fasta` / `.fa` | Sequences only |
| Alignment | `.sam` / `.bam` | Read-to-reference mappings |
| QIIME2 artifact | `.qza` | Data + provenance |
| QIIME2 viz | `.qzv` | Interactive visualization |
| OTU table | `.biom` | Biological observation matrix |
| Annotation | `.gff` | Gene features + coordinates |
| Tree | `.nwk` / `.tre` | Phylogenetic tree (Newick format) |
| Kraken report | `.kreport` | Taxonomic classification summary |
| Tabular | `.tsv` / `.csv` | General data tables |

---

## Troubleshooting Quick Fixes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `command not found` | Tool not installed or env not activated | `conda activate metagenomics` |
| `Permission denied` | No execute permission | `chmod +x script.sh` |
| `No space left on device` | Disk full | `df -h` to check; clear temp files |
| `Killed` or `MemoryError` | Out of RAM | Reduce threads; use smaller dataset |
| QIIME2 import fails | Wrong file format or naming | Check Casava format: `SampleID_S1_L001_R1_001.fastq.gz` |
| DADA2 low merge rate | Truncation too aggressive | Increase `--p-trunc-len` values |
| CheckM very slow | Large database loading | Increase `--pplacer_threads`; use CheckM2 |
| GTDBTk fails | Reference data not found | Check `$GTDBTK_DATA_PATH` is set correctly |
| R package missing | Not installed | `install.packages("name")` or `BiocManager::install("name")` |
| DESeq2 fails | Zero-only rows or single sample groups | Filter low-count taxa; ensure ≥2 samples/group |

---

*This cheat sheet is your quick reference during and after the workshop. Print it!*
