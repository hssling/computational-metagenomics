# Workshop Context Summary & Developer Hand-off

## Project Overview: Computational Metagenomics Workshop
**Theme:** Methods and Applications (16S Amplicon + Shotgun Pipeline)
**Date:** April 7th - 9th, 2026
**Host:** NPTEL+ | IIT Madras
**Instructors:** Prof. Karthik Raman, Dr. Aarti Ravindran, Dr. Pratyay Sengupta

## Project Status: COMPLETED
All core deliverables have been created and polished with **Rich Aesthetics** (Mermaid diagrams, GitHub alerts, tables).

### Deliverables Inventory

| Filename | Purpose | Highlights |
|----------|---------|------------|
| `00_Workshop_Overview_and_Setup.md` | Master Guide | Mermaid workflow, WSL2/Conda setup, detailed schedule |
| `Day1_Foundations_and_16S_Amplicon.md` | Day 1 Materials | 16S theory, QIIME2 workflow, OTU vs ASV, ASV-based Pipeline |
| `Day2_Shotgun_Metagenomics.md` | Day 2 Materials | Shotgun seq, Assembly (MEGAHIT), Binning (MetaBAT2/MaxBin2), MAG Quality |
| `Day3_Statistical_Analysis.md` | Day 3 Materials | Compositionality, Normalization (CLR/Rarefaction), Alpha/Beta Diversity, DESeq2 |
| `Commands_CheatSheet.md` | Quick Reference | One-liner commands for all tools (QIIME2, Kraken2, R, Linux) |
| `Glossary_and_References.md` | Academic Context | A-Z Key terms, Landmark papers, Databases, Recommended reading |
| `TODO.md` | Project Tracking | Tracks the development and polish process |

## Key Technical Concepts Integrated
- **Amplicon:** ASV (Amplicon Sequence Variant) focus over OTUs using DADA2.
- **Shotgun:** Metagenome-Assembled Genomes (MAGs) recovery and quality assessment (CheckM/GTDB-Tk).
- **Statistics:** Handling compositional data using Centered Log-Ratio (CLR) and PERMANOVA.

## Maintenance Notes
- All diagrams use Mermaid syntax for modern, scalable rendering.
- Markdown files follow GitHub-style alert syntax (`> [!NOTE]`, etc.).
- File links use absolute paths or internal references appropriate for the workspace.

## Memory Log for Future AI Agents
> [!IMPORTANT]
> This workshop is designed for a 3-day high-intensity program at IIT Madras. The content starts from absolute Linux basics and scales to complex MAG recovery and machine learning. All scripts and commands provided are vetted for standard bioinformatics environments (Ubuntu/WSL2).
