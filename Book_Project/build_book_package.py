from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOT = Path(__file__).resolve().parent
FRONT_MATTER = BOOK_ROOT / "front_matter"
GENERATED = BOOK_ROOT / "generated"
CHAPTER_DIR = GENERATED / "chapters"
OUTPUT_DIR = GENERATED / "outputs"

AUTHOR = "Dr Siddalingaiah H S"
TITLE = "Computational Metagenomics and Modern Biomedical Omics"
SUBTITLE = "A Practical Handbook from 16S Analysis to Spatial and Multiomic Interpretation"


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    replacements = {
        "â€”": "-",
        "–": "-",
        "—": "-",
        "â€“": "-",
        "â†’": "->",
        "→": "->",
        "â”€": "-",
        "─": "-",
        "â€˜": "'",
        "â€™": "'",
        "’": "'",
        "â€œ": '"',
        "â€": '"',
        "“": '"',
        "”": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def collapse_blank_lines(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    return text + "\n"


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def strip_tables_and_images(text: str) -> str:
    lines = text.splitlines()
    cleaned: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("!["):
            continue
        if line.startswith("Table:"):
            in_table = True
            continue
        if in_table:
            if line.startswith("|") or line.strip() == "":
                if line.strip() == "":
                    in_table = False
                continue
            in_table = False
        cleaned.append(line)
    return "\n".join(cleaned)


def clean_overview_chapter(text: str) -> str:
    learning = extract_section(text, "## Workshop Learning Objectives", "## Who Is This Workshop For?")
    audience = extract_section(text, "## Who Is This Workshop For?", "## Pre-Workshop Preparation")
    big_picture = extract_section(text, "## The Big Picture: What Is a Metagenomics Workflow?", "## Tips for Workshop Success")
    keep = "\n\n".join([learning, audience, big_picture]).strip()
    keep = keep.replace("## Workshop Learning Objectives", "## Learning Objectives")
    keep = keep.replace("## Who Is This Workshop For?", "## Intended Audience")
    keep = keep.replace("By the end of this 3-day workshop, participants will be able to:", "By the end of this handbook, readers should be able to:")
    keep = keep.replace("No prior bioinformatics experience required - we start from scratch", "No prior bioinformatics experience is assumed at entry level, although later chapters build toward advanced practice.")
    lines = keep.splitlines()
    rewritten: list[str] = []
    in_mermaid = False
    in_tip = False
    inserted_workflow = False
    inserted_tip = False
    for line in lines:
        if line.strip() == "```mermaid":
            in_mermaid = True
            if not inserted_workflow:
                rewritten.append(
                    "A metagenomics workflow can be read as a sequence of linked decisions: sample collection leads to DNA extraction and library preparation; library preparation leads to selection of either targeted amplicon sequencing or untargeted shotgun sequencing; both pathways eventually feed into statistical analysis, interpretation, and reporting. Amplicon analysis is best suited to broad taxonomic profiling, while shotgun workflows open the door to functional inference, strain resolution, and genome-resolved reconstruction."
                )
                inserted_workflow = True
            continue
        if in_mermaid:
            if line.strip() == "```":
                in_mermaid = False
            continue
        if line.startswith("> [!TIP]"):
            in_tip = True
            if not inserted_tip:
                rewritten.append(
                    "As a practical rule, targeted amplicon sequencing is often sufficient when the main question is taxonomic composition, whereas shotgun metagenomics is more appropriate when the study requires functional characterization, strain-level distinction, or genome recovery."
                )
                inserted_tip = True
            continue
        if in_tip:
            if line.strip() == "" or line.startswith("---"):
                in_tip = False
                if line.startswith("---"):
                    rewritten.append(line)
            continue
        rewritten.append(line)
    keep = "\n".join(rewritten)
    keep = re.sub(r"> \[!TIP\].*?(?=\n---|\Z)", "", keep, flags=re.S)
    return collapse_blank_lines(keep)


def clean_setup_appendix(text: str) -> str:
    prep = extract_section(text, "## Pre-Workshop Preparation", "## 3-Day Workshop Schedule at a Glance")
    formats = extract_section(text, "## File Formats You Will Encounter", "## The Big Picture: What Is a Metagenomics Workflow?")
    combined = "\n\n".join([prep, formats]).strip()
    combined = combined.replace("## Pre-Workshop Preparation", "## Environment Preparation")
    combined = combined.replace("### 4. Command Line Basics (Self-Assessment)", "### 4. Command-Line Basics")
    combined = combined.replace("#### Create the Workshop Conda Environment", "#### Create the Working Conda Environment")
    combined = combined.replace("If you are using a workshop-provided computer, all tools will be pre-installed. This section is for participants using their own laptops.", "These setup notes assume the reader is preparing an independent workstation for training and manuscript development.")
    return collapse_blank_lines(combined)


def extract_section(text: str, start_heading: str, end_heading: str | None = None) -> str:
    start = text.find(start_heading)
    if start == -1:
        return ""
    end = text.find(end_heading, start) if end_heading else -1
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def clean_day_notes(text: str) -> str:
    lines = text.splitlines()
    cleaned: list[str] = []
    skip_block = False
    for line in lines:
        if line.startswith("# DAY ") or line.startswith("## April "):
            continue
        if line.startswith("# SESSION "):
            continue
        if re.match(r"^## Day \d+ Assignment", line) or re.match(r"^## Day \d+ Key Takeaways", line):
            skip_block = True
            continue
        if skip_block and line.startswith("## "):
            skip_block = False
        if skip_block:
            continue
        cleaned.append(line)
    return collapse_blank_lines("\n".join(cleaned))


def clean_manuscript(text: str) -> str:
    start = re.search(r"^## 1\. ", text, flags=re.M)
    if not start:
        return collapse_blank_lines(text)
    end = re.search(r"^## Declarations", text, flags=re.M)
    body = text[start.start() : end.start() if end else len(text)]
    body = strip_tables_and_images(body)
    return collapse_blank_lines(body)


def clean_commands(text: str) -> str:
    lines = text.splitlines()
    cleaned = [line for line in lines if not line.startswith("# Commands Cheat") and "Computational Metagenomics Workshop" not in line]
    return collapse_blank_lines("\n".join(cleaned))


def clean_glossary(text: str) -> str:
    lines = text.splitlines()
    cleaned = [line for line in lines if not line.startswith("# Glossary") and "Computational Metagenomics Workshop" not in line]
    return collapse_blank_lines("\n".join(cleaned))


def chapter_text(number: int, title: str, intro: str, bodies: list[str]) -> str:
    sections = [f"# Chapter {number}. {title}", "", intro.strip(), ""]
    for body in bodies:
        body = body.strip()
        if body:
            sections.append(body)
            sections.append("")
    return collapse_blank_lines("\n".join(sections))


CHAPTER_SPECS = [
    {
        "slug": "01_orientation_and_study_design",
        "title": "Orientation and Study Design",
        "intro": (
            "This opening chapter frames computational metagenomics as a practical decision discipline rather than a loose collection of tools. "
            "It establishes the logic of good study design, clarifies who this handbook is for, and introduces the sample-to-inference workflow "
            "that recurs throughout the rest of the book."
        ),
        "sources": [(ROOT / "00_Workshop_Overview_and_Setup.md", clean_overview_chapter)],
    },
    {
        "slug": "02_foundations_of_metagenomics",
        "title": "Foundations of Metagenomics",
        "intro": (
            "This chapter introduces the conceptual basis of metagenomics, differentiates amplicon and shotgun approaches, and outlines the "
            "experimental logic required before any sequence file is processed."
        ),
        "sources": [(ROOT / "Day1_Foundations_and_16S_Amplicon.md", clean_day_notes)],
    },
    {
        "slug": "03_shotgun_metagenomics_and_function",
        "title": "Shotgun Metagenomics and Functional Interpretation",
        "intro": (
            "Shotgun metagenomics expands the analytic field from broad community profiling to strain-level, gene-level, and genome-resolved inference. "
            "This chapter follows the read-processing, assembly, taxonomic, functional, and machine-learning logic needed to turn raw reads into biological insight."
        ),
        "sources": [(ROOT / "Day2_Shotgun_Metagenomics.md", clean_day_notes)],
    },
    {
        "slug": "04_statistical_analysis_and_inference",
        "title": "Statistical Analysis and Reproducible Inference",
        "intro": (
            "Microbiome datasets are compositional, sparse, and often confounded by uneven sampling and metadata complexity. "
            "This chapter consolidates the normalization, diversity, ordination, and differential-abundance methods required for defensible inference."
        ),
        "sources": [(ROOT / "Day3_Statistical_Analysis.md", clean_day_notes)],
    },
    {
        "slug": "05_human_computational_metagenomics",
        "title": "Human Computational Metagenomics",
        "intro": (
            "Host-associated metagenomics introduces a different level of technical and interpretive difficulty. "
            "Clinical sampling, host-read subtraction, contamination control, privacy, and translational framing all become central."
        ),
        "sources": [(ROOT / "Manuscript_Package_Human" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "06_genomics_and_transcriptomics",
        "title": "Genomics and Transcriptomics in Biomedical Practice",
        "intro": (
            "Computational biology now routinely moves beyond microbiome profiling into human genomics and transcriptomics. "
            "This chapter extends the workflow logic to variant discovery, transcript quantification, interpretation, and clinical reporting."
        ),
        "sources": [(ROOT / "Manuscript_Package_Genomics_Transcriptomics" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "07_multiomics_integration",
        "title": "Multiomics Integration",
        "intro": (
            "Once multiple molecular layers are collected, the main challenge is no longer assay generation but coherent integration. "
            "This chapter covers study design, preprocessing, latent representations, missing data, and translational overclaim in multiomics work."
        ),
        "sources": [(ROOT / "Manuscript_Package_Multiomics" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "08_single_cell_and_spatial_omics",
        "title": "Single-Cell and Spatial Omics",
        "intro": (
            "Single-cell and spatial approaches bring cellular heterogeneity and tissue architecture into the computational workflow. "
            "The analytical burden now includes annotation, mapping, segmentation, local interaction analysis, and pathology-grounded interpretation."
        ),
        "sources": [(ROOT / "Manuscript_Package_SingleCell_Spatial" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "09_spatiotemporal_omics",
        "title": "Spatiotemporal Omics",
        "intro": (
            "Static tissue maps are often insufficient when the biological question concerns progression, development, treatment response, or repair. "
            "This chapter addresses dynamic tissue-resolved analysis, including registration, temporal alignment, trajectory logic, and uncertainty."
        ),
        "sources": [(ROOT / "Manuscript_Package_Spatiotemporal_Omics" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "10_emerging_omics_technologies",
        "title": "Emerging Omics Technologies",
        "intro": (
            "The omics field continues to expand into spatial proteomics, perturb-omics, epitranscriptomics, exposomics, and liquid biopsy multiomics. "
            "This chapter evaluates those platforms through the lens of computational maturity, fit-for-purpose design, and publication realism."
        ),
        "sources": [(ROOT / "Manuscript_Package_Emerging_Omics" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "11_integrated_biomedical_omics",
        "title": "Integrated Biomedical Omics",
        "intro": (
            "This chapter provides the umbrella view: how genomics, transcriptomics, multiomics, single-cell, spatial, and spatiotemporal assays fit into a single decision hierarchy. "
            "The emphasis is on choosing the minimum complexity that answers the biological question without inflating uncertainty."
        ),
        "sources": [(ROOT / "Manuscript_Package_Umbrella_Review" / "Main_Manuscript.md", clean_manuscript)],
    },
    {
        "slug": "12_appendix_setup_and_cli",
        "title": "Appendix A. Environment Setup and Command-Line Practice",
        "intro": (
            "The command line remains the operating environment for a large fraction of computational omics. "
            "This appendix preserves the practical setup and shell guidance developed for the workshop material."
        ),
        "sources": [
            (ROOT / "00_Workshop_Overview_and_Setup.md", clean_setup_appendix),
            (ROOT / "Commands_CheatSheet.md", clean_commands),
        ],
    },
    {
        "slug": "13_appendix_glossary_and_references",
        "title": "Appendix B. Glossary and Further Reading",
        "intro": (
            "This appendix consolidates terminology, landmark papers, software references, and further learning resources to support continued study."
        ),
        "sources": [(ROOT / "Glossary_and_References.md", clean_glossary)],
    },
]


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


def build() -> None:
    CHAPTER_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chapter_files: list[Path] = []
    stats: dict[str, int] = {}

    for idx, spec in enumerate(CHAPTER_SPECS, start=1):
        bodies = []
        for src, cleaner in spec["sources"]:
            bodies.append(cleaner(read_text(src)))
        text = chapter_text(idx, spec["title"], spec["intro"], bodies)
        out = CHAPTER_DIR / f"{spec['slug']}.md"
        out.write_text(text, encoding="utf-8")
        chapter_files.append(out)
        stats[out.name] = word_count(text)

    front_files = sorted(FRONT_MATTER.glob("*.md"))
    combined_parts = [read_text(p) for p in front_files] + [read_text(p) for p in chapter_files]
    combined = collapse_blank_lines("\n\n".join(combined_parts))
    manuscript = OUTPUT_DIR / "Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.md"
    manuscript.write_text(combined, encoding="utf-8")
    stats["total_words"] = word_count(combined)
    (OUTPUT_DIR / "book_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")

    metadata = BOOK_ROOT / "book_metadata.yaml"
    run(
        [
            "pandoc",
            str(metadata),
            str(manuscript),
            "--toc",
            "--standalone",
            "-o",
            str(OUTPUT_DIR / "Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.docx"),
        ],
        ROOT,
    )
    run(
        [
            "pandoc",
            str(metadata),
            str(manuscript),
            "--toc",
            "--standalone",
            "-o",
            str(OUTPUT_DIR / "Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.epub"),
        ],
        ROOT,
    )
    run(
        [
            "pandoc",
            str(metadata),
            str(manuscript),
            "--toc",
            "--standalone",
            "-o",
            str(OUTPUT_DIR / "Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.html"),
        ],
        ROOT,
    )
    pdf_metadata = BOOK_ROOT / "pdf_config.yaml"
    run(
        [
            "pandoc",
            str(pdf_metadata),
            str(manuscript),
            "--toc",
            "--standalone",
            "--pdf-engine=xelatex",
            "-o",
            str(OUTPUT_DIR / "Computational_Metagenomics_and_Modern_Biomedical_Omics_Book.pdf"),
        ],
        ROOT,
    )


if __name__ == "__main__":
    build()
