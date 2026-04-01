# Book Project

This directory contains the professional-grade book package built from the workshop material and review manuscripts in this repository.

## Outputs

Generated files are written to `generated/outputs/`:

1. `Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.md`
2. `Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.docx`
3. `Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.epub`
4. `Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.html`
5. `book_stats.json`

## Build

Run the book builder from the repository root or from this directory:

```powershell
python .\Book_Project\build_book_package.py
```

## Structure

- `front_matter/`: title page, copyright, preface, usage notes
- `generated/chapters/`: chapterized book source generated from the project corpus
- `generated/outputs/`: compiled book outputs
- `publication/`: publishing and submission package
- `assets/`: cover and branding assets
