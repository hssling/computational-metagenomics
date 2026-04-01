# Submission Package Notes

## Contents
1. `Main_Manuscript.md` and `Main_Manuscript_Reviewed_Final.docx`: tutorial review manuscript focused on human-associated computational metagenomics.
2. `Human_Computational_Metagenomics_Complete.docx`: combined title page plus manuscript in one fully embedded document.
3. `Title_Page.md` and `Title_Page.docx`: title page with author and correspondence metadata.
4. `Cover_Letter.md` and `Cover_Letter.docx`: journal-ready cover letter.
5. `figures/`: publication-style schematic and illustrative figures.
6. `generate_figures.py`: script used to regenerate the figures.

## Editorial Positioning
- Suggested target journal: *Briefings in Bioinformatics*
- Suggested article type: Tutorial Review
- Scope: host-associated human metagenomics with emphasis on host-read removal, contamination control, metadata-aware statistics, ethics, and translational interpretation

## Important Notes
- This manuscript is framed as a tutorial review, not as a new clinical study.
- Figures are explicitly labeled as schematic or illustrative examples.
- Standard declarations are included.
- The package separates the title page from the main manuscript for standard journal submission workflows.

## Regeneration
Use the following commands from `Manuscript_Package_Human`:

```powershell
python .\generate_figures.py
pandoc .\Title_Page.md -o .\Title_Page.docx
pandoc .\Cover_Letter.md -o .\Cover_Letter.docx
pandoc .\Main_Manuscript.md -o .\Main_Manuscript_Reviewed_Final.docx --resource-path='.;figures'
pandoc .\Title_Page.md .\Main_Manuscript.md -o .\Human_Computational_Metagenomics_Complete.docx --resource-path='.;figures'
```
