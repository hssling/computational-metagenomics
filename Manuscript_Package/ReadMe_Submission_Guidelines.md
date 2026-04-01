# Submission Package Notes

## Contents
1. `Main_Manuscript.md` and `Main_Manuscript_Reviewed_Final.docx`: tutorial review manuscript with abstract, main text, figure captions, tables, declarations, and references.
2. `Title_Page.md` and `Title_Page.docx`: title page containing author details, correspondence information, keywords, and submission metadata.
3. `Cover_Letter.md` and `Cover_Letter.docx`: journal-ready cover letter.
4. `figures/`: publication-style tutorial figures used in the manuscript.
5. `generate_figures.py`: script used to regenerate the illustrative figures.

## Editorial Positioning
- Suggested target journal: *Briefings in Bioinformatics*
- Suggested article type: Tutorial Review
- Manuscript scope: educational synthesis and methodological roadmap

## Important Notes
- The manuscript is framed as a tutorial review, not as an original clinical or experimental study.
- The figures are explicitly labeled as schematics or illustrative example outputs.
- Standard declarations have been included: author contributions, funding, competing interests, ethics, consent, data availability, acknowledgements, and author information.
- The current package uses a separate title page and a main manuscript suitable for journal submission workflows.

## Regeneration
If any text or figure changes are made, regenerate outputs from the `Manuscript_Package` directory using:

```powershell
python .\generate_figures.py
pandoc .\Title_Page.md -o .\Title_Page.docx
pandoc .\Cover_Letter.md -o .\Cover_Letter.docx
pandoc .\Main_Manuscript.md -o .\Main_Manuscript_Reviewed_Final.docx --resource-path='.;figures'
```

## Legacy Files
- Older files such as `Main_Manuscript_Final.docx` may remain in the directory if they were open or locked during regeneration.
- The reviewed submission-ready manuscript produced in this pass is `Main_Manuscript_Reviewed_Final.docx`.
