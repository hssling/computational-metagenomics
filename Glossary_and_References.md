# Glossary, Key References & Further Learning

## Computational Metagenomics Workshop — IIT Madras, April 2026

---

## A-Z Glossary of Key Terms

### A
- **Adapter:** Short synthetic DNA sequences ligated to fragments during library prep; must be removed before analysis
- **Alpha diversity:** Diversity within a single sample (richness, evenness, phylogenetic diversity)
- **Amplicon:** A targeted PCR-amplified DNA fragment (e.g., 16S rRNA V3-V4 region)
- **ANCOM/ANCOM-BC:** Analysis of Composition of Microbiomes — compositional-aware differential abundance method
- **ASV (Amplicon Sequence Variant):** Exact biological sequence resolved by denoising; replaces OTU as the standard unit

### B
- **BAM:** Binary Alignment Map — compressed binary version of SAM format
- **Barcode (Index):** Short unique DNA sequence added to each sample for multiplexing; allows pooled sequencing
- **Beta diversity:** Diversity between samples; quantified as a distance/dissimilarity matrix
- **Binning:** Grouping contigs into genome bins based on composition and coverage patterns
- **BIOM:** Biological Observation Matrix — standard format for OTU/ASV abundance tables
- **Bracken:** Bayesian Reestimation of Abundance with KrakEN — refines Kraken2 species-level estimates
- **Bray-Curtis dissimilarity:** Abundance-weighted beta diversity metric (0 = identical, 1 = completely different)

### C
- **CheckM/CheckM2:** Tool assessing MAG completeness and contamination using single-copy marker genes
- **Chimera:** Artificial sequence formed during PCR when an incomplete extension serves as primer for a different template
- **CLR (Centered Log-Ratio):** Transformation for compositional data: log(value/geometric mean)
- **COGs (Clusters of Orthologous Groups):** Functional classification system for proteins based on evolutionary relationships
- **Compositional data:** Data where values represent proportions summing to a constant (e.g., relative abundances sum to 1)
- **Contig:** Contiguous sequence assembled from overlapping reads
- **Coverage (Depth):** Average number of times each base position is sequenced (e.g., 30x coverage)

### D
- **DADA2:** Divisive Amplicon Denoising Algorithm — infers exact ASVs by modeling sequencing errors
- **DAS Tool:** Meta-binner that combines results from multiple binning algorithms
- **de Bruijn graph:** Graph-based data structure used by most assemblers; nodes are k-mers, edges are overlaps
- **Denoising:** Statistical process to distinguish true biological sequences from sequencing errors
- **DESeq2:** Differential expression/abundance tool using negative binomial GLM with shrinkage estimation
- **Dysbiosis:** Imbalance in microbial community composition, often associated with disease

### E
- **eggNOG-mapper:** Tool for functional annotation using orthologous groups
- **Enterotype:** Proposed classification of human gut microbiomes into discrete community types (Bacteroides, Prevotella, Ruminococcus-dominated)

### F
- **Faith's PD (Phylogenetic Diversity):** Alpha diversity metric = sum of branch lengths connecting observed taxa
- **FASTA:** File format for sequences (>header followed by sequence)
- **FASTQ:** File format for sequences + quality scores (4 lines per read)
- **FastQC:** Quality control tool producing visual reports of sequencing data quality
- **FMT (Fecal Microbiota Transplant):** Transfer of stool from healthy donor to patient

### G
- **GFF (General Feature Format):** File format for genomic annotations (gene locations, types)
- **GTDB (Genome Taxonomy Database):** Standardized taxonomy based on genome phylogeny
- **GTDBTk:** GTDB Toolkit — classifies genomes using GTDB reference tree

### H
- **HiFi reads:** PacBio high-fidelity reads (>Q20 accuracy from circular consensus sequencing)
- **Holobiont:** Host organism + its entire microbiome considered as a single biological entity
- **Host depletion:** Removal of host DNA sequences from metagenomic data before analysis

### I
- **ITS (Internal Transcribed Spacer):** Fungal barcode region between rRNA genes
- **Illumina:** Dominant short-read sequencing platform using sequencing-by-synthesis chemistry

### K
- **KEGG (Kyoto Encyclopedia of Genes and Genomes):** Database of metabolic pathways and biological functions
- **k-mer:** Substring of length k from a DNA sequence (e.g., k=35 means all 35-bp substrings)
- **Kraken2:** Ultrafast taxonomic classifier using exact k-mer matching against reference database

### L
- **LCA (Lowest Common Ancestor):** Taxonomic classification strategy — when a k-mer matches multiple taxa, assign to their common ancestor
- **Library preparation:** Process of preparing DNA for sequencing (fragmentation, adapter ligation, amplification)
- **Long-read sequencing:** Platforms producing reads >10 kb (Oxford Nanopore, PacBio)

### M
- **MAG (Metagenome-Assembled Genome):** Near-complete genome reconstructed from metagenomic data through assembly + binning
- **Marker gene:** Conserved gene used for taxonomic identification (e.g., 16S rRNA, ITS)
- **Metadata:** Information about samples (patient age, collection site, pH, temperature, etc.)
- **MetaBAT2:** Metagenome Binning with Abundance and Tetra-nucleotide frequencies
- **MEGAHIT:** Memory-efficient metagenome assembler using succinct de Bruijn graphs
- **Metagenome:** The collective genomes of all microorganisms in an environmental sample
- **Microbiome:** The community of microorganisms (bacteria, archaea, fungi, viruses) in a given environment
- **MIMAG:** Minimum Information about a Metagenome-Assembled Genome (quality standards)
- **Mock community:** Known mixture of microorganisms used as a positive control
- **Multiplexing:** Pooling multiple barcoded samples in a single sequencing run

### N
- **N50:** Assembly quality metric — 50% of the total assembly length is contained in contigs of this size or larger
- **Nanopore sequencing:** Long-read technology measuring electrical current changes as DNA passes through a protein pore
- **Negative control:** Sample processed identically but without biological input (detects contamination)
- **NMDS (Non-metric Multidimensional Scaling):** Ordination method preserving rank-order distances

### O
- **OTU (Operational Taxonomic Unit):** Cluster of sequences at 97% similarity threshold (legacy method, replaced by ASVs)
- **Ordination:** Dimensionality reduction technique for visualizing sample relationships (PCoA, NMDS, PCA)

### P
- **Paired-end sequencing:** Sequencing both ends of a DNA fragment, producing R1 (forward) and R2 (reverse) reads
- **PCoA (Principal Coordinates Analysis):** Ordination method that preserves distance relationships between samples
- **PERMANOVA (adonis2):** Permutational ANOVA — tests whether groups differ in community composition
- **PERMDISP:** Tests homogeneity of group dispersions (companion to PERMANOVA)
- **Phred score (Q-score):** Quality score: Q = -10 × log₁₀(error probability); Q30 = 1 in 1000 error rate
- **Phyloseq:** R package for microbiome data analysis and visualization
- **Prokka:** Rapid prokaryotic genome annotation tool (identifies genes, rRNA, tRNA)

### Q
- **QIIME2:** Quantitative Insights Into Microbial Ecology — comprehensive amplicon analysis platform
- **Quality trimming:** Removing low-quality bases from read ends to improve downstream analysis

### R
- **Rarefaction:** Random subsampling to equalize sequencing depth across samples
- **Read:** A single sequenced DNA fragment (typically 150-300 bp for Illumina)
- **Relative abundance:** Proportion of a taxon in a sample (sums to 1.0 across all taxa)

### S
- **SAM (Sequence Alignment Map):** Text format storing read alignments against a reference
- **Scaffold:** Ordered and oriented contigs connected by paired-end information (with gaps)
- **Shannon index (H'):** Alpha diversity metric combining richness and evenness: H' = -Σ pᵢ ln(pᵢ)
- **Shotgun metagenomics:** Untargeted sequencing of all DNA in a sample (no PCR targeting)
- **SILVA:** Comprehensive ribosomal RNA database for taxonomy assignment
- **Simpson index (1-D):** Alpha diversity: probability that two random reads come from different taxa
- **SparCC:** Sparse Correlations for Compositional data — correlation method for compositional microbiome data

### T
- **Taxonomic profiling:** Identifying and quantifying the organisms present in a sample
- **Tetranucleotide frequency:** Frequency of all 4-bp combinations in a sequence — species-specific "DNA signature" used in binning
- **Trimmomatic:** Tool for adapter removal and quality trimming of Illumina reads

### U
- **UniFrac:** Phylogeny-based beta diversity metric; unweighted (presence/absence) or weighted (abundance)

### V
- **V-regions (V1-V9):** Variable regions of the 16S rRNA gene used for taxonomic identification
- **Volcano plot:** Scatterplot of log2 fold change vs. -log10 p-value for differential abundance visualization

---

## Landmark Papers (Must-Read)

### Foundational

| Year | Paper | Citation | Key Contribution |
|------|-------|----------|-----------------|
| 1998 | Metagenomics coined | Handelsman et al., *Chem Biol* | First use of "metagenomics" term |
| 2007 | Human Microbiome Project | Turnbaugh et al., *Nature* | Launched systematic study of human microbiome |
| 2010 | MetaHIT consortium | Qin et al., *Nature* | Catalogued 3.3 million microbial genes in human gut |
| 2011 | Enterotypes | Arumugam et al., *Nature* | Proposed gut microbiome community types |
| 2012 | HMP Phase 1 results | Human Microbiome Project Consortium, *Nature* | Characterized healthy human microbiome |

### Methods

| Year | Paper | Key Contribution |
|------|-------|-----------------|
| 2016 | DADA2 | Callahan et al., *Nature Methods* — ASV denoising algorithm |
| 2019 | QIIME2 | Bolyen et al., *Nature Biotechnology* — Comprehensive amplicon platform |
| 2014 | Kraken | Wood & Salzberg, *Genome Biology* — Ultrafast taxonomic classification |
| 2015 | MetaBAT | Kang et al., *PeerJ* — Metagenome binning |
| 2019 | GTDB | Parks et al., *Nature Biotechnology* — Genome-based taxonomy |
| 2018 | CheckM | Parks et al., *Genome Research* — MAG quality assessment |
| 2014 | DESeq2 | Love et al., *Genome Biology* — Differential expression/abundance |
| 2014 | ALDEx2 | Fernandes et al., *Microbiome* — Compositional differential abundance |

### Clinical Impact

| Year | Paper | Key Finding |
|------|-------|-------------|
| 2013 | FMT for C. difficile | van Nood et al., *NEJM* — 94% cure rate with FMT |
| 2018 | Microbiome & immunotherapy | Routy et al., *Science* — Gut bacteria predict cancer therapy response |
| 2019 | Microbiome & depression | Valles-Colomer et al., *Nature Microbiology* — Gut-brain axis mechanisms |

---

## Key Databases & Web Resources

### Sequence & Taxonomy Databases

| Resource | URL | Purpose |
|----------|-----|---------|
| **SILVA** | silva.de | 16S/18S/23S rRNA reference database |
| **Greengenes2** | greengenes2.ucsd.edu | 16S rRNA database (genome-informed) |
| **GTDB** | gtdb.ecogenomic.org | Genome-based taxonomy |
| **NCBI GenBank** | ncbi.nlm.nih.gov/genbank | General nucleotide database |
| **UNITE** | unite.ut.ee | Fungal ITS database |
| **RDP** | rdp.cme.msu.edu | Ribosomal Database Project |

### Functional Databases

| Resource | URL | Purpose |
|----------|-----|---------|
| **KEGG** | kegg.jp | Metabolic pathways and functions |
| **COG/eggNOG** | eggnog-mapper.embl.de | Orthologous group annotation |
| **Pfam** | pfam.xfam.org | Protein family database |
| **UniProt** | uniprot.org | Protein sequences and functions |
| **CAZy** | cazy.org | Carbohydrate-active enzymes |
| **CARD** | card.mcmaster.ca | Antimicrobial resistance genes |
| **VFDB** | mgc.ac.cn/VFs | Virulence factors database |

### Analysis Platforms & Tools

| Resource | URL | Purpose |
|----------|-----|---------|
| **QIIME2 View** | view.qiime2.org | View QIIME2 visualizations online |
| **Galaxy** | usegalaxy.org | Web-based analysis platform |
| **MG-RAST** | metagenomics.anl.gov | Metagenome annotation server |
| **KBase** | kbase.us | DOE Systems Biology Platform |
| **iVikodak** | web.rniapps.net/iVikodak | Functional metagenomics |

### Microbiome-Specific Repositories

| Resource | URL | Purpose |
|----------|-----|---------|
| **EBI MGnify** | ebi.ac.uk/metagenomics | Metagenome data analysis & archiving |
| **GMrepo** | gmrepo.humangut.info | Curated human gut microbiome data |
| **curatedMetagenomicData** | bioconductor.org | Standardized human metagenomes (R) |
| **MicrobiomeDB** | microbiomedb.org | Microbiome data discovery |
| **QIITA** | qiita.ucsd.edu | Microbiome multi-study platform |

---

## Recommended Books

| Book | Authors | Best For |
|------|---------|----------|
| **Metagenomics: Methods and Protocols** | Streit & Daniel (eds.) | Comprehensive lab + computational methods |
| **Bioinformatics and Functional Genomics** | Pevsner | General bioinformatics foundation |
| **Statistical Analysis of Microbiome Data with R** | Xia, Sun & Chen | R-based statistical methods |
| **The Human Superorganism** | Dietert | Accessible introduction to the microbiome |
| **I Contain Multitudes** | Ed Yong | Popular science — engaging microbiome overview |
| **An Introduction to Systems Biology** | Karthik Raman | Systems-level thinking for biology (by workshop instructor!) |

---

## Online Courses & Tutorials

### Free Courses
1. **QIIME2 Tutorials** — docs.qiime2.org — Official step-by-step tutorials
2. **Bioinformatics Workbook** — bioinformaticsworkbook.org — ISU metagenomics tutorial
3. **Happy Belly Bioinformatics** — astrobiomike.github.io — Beginner-friendly metagenomics
4. **Microbiome Helper** — github.com/LangilleLab/microbiome_helper — Workflow tutorials
5. **EDAMAME course** — edamame-course.org — Environmental genomics workshop materials

### YouTube Channels
- **StatQuest** (Josh Starmer) — Statistical concepts explained visually
- **Riffomonas Project** (Pat Schloss) — R for microbiome analysis
- **iBiology** — Research talks including metagenomics

---

## Software Version Reference

*Versions current as of workshop date (April 2026). Always check for updates.*

| Tool | Category | Typical Version |
|------|----------|-----------------|
| QIIME2 | Amplicon platform | 2024.10+ |
| DADA2 | ASV denoising | 1.28+ |
| FastQC | Quality check | 0.12+ |
| MultiQC | QC aggregation | 1.21+ |
| Trimmomatic | Read trimming | 0.39+ |
| Kraken2 | Taxonomic classification | 2.1.3+ |
| Bracken | Abundance estimation | 2.9+ |
| MEGAHIT | Metagenome assembly | 1.2.9+ |
| MetaBAT2 | Binning | 2.15+ |
| MaxBin2 | Binning | 2.2.7+ |
| DAS Tool | Bin refinement | 1.1.6+ |
| CheckM/CheckM2 | MAG quality | 1.2.2+ / 1.0+ |
| GTDBTk | Genome taxonomy | 2.3+ |
| Prokka | Gene annotation | 1.14+ |
| eggNOG-mapper | Functional annotation | 2.1+ |
| phyloseq (R) | Microbiome analysis | 1.44+ |
| vegan (R) | Ecological statistics | 2.6+ |
| DESeq2 (R) | Differential abundance | 1.40+ |
| ALDEx2 (R) | Compositional DA | 1.32+ |

---

## Post-Workshop: What to Do Next

### Immediate (Week 1)
- [ ] Practice the complete pipeline on workshop demo data
- [ ] Try running the pipeline on a publicly available dataset (e.g., from MGnify)
- [ ] Review your notes and fill in any gaps using this material

### Short-Term (Month 1)
- [ ] Apply skills to your own research data
- [ ] Read 2-3 landmark papers relevant to your field
- [ ] Join the QIIME2 Forum (forum.qiime2.org) for community support
- [ ] Explore the Bioconductor microbiome packages in R

### Long-Term (Months 2-6)
- [ ] Learn shell scripting to automate your workflows
- [ ] Explore additional tools (HUMAnN3 for functional profiling, PhyloPhlAn, etc.)
- [ ] Consider multi-omics integration (metatranscriptomics, metabolomics)
- [ ] Attend conferences: ISME, ASM Microbe, ISMB
- [ ] Consider contributing to open-source bioinformatics tools

---

*"The microbiome is an ecosystem. To understand it, you need both biology and computation. This workshop gave you the computational tools — now go explore the biology."*

---

*End of Workshop Materials*
