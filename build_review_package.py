from pathlib import Path
from textwrap import dedent
import json
import subprocess
import sys
import re
from manuscript_profiles import expand_section


AUTHOR = {
    "name": "Dr Siddalingaiah H S",
    "aff": "Professor, Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, India",
    "email": "hssling@yahoo.com",
    "phone": "+91 8941087719",
    "orcid": "0000-0002-4771-8285",
}


FIG_SCRIPT = """from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
ROOT=Path(r'{root}')
FIG_DIR=ROOT/'figures'; FIG_DIR.mkdir(parents=True,exist_ok=True)
TITLES={titles}
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({{'figure.dpi':240,'savefig.dpi':240,'savefig.bbox':'tight','font.family':'DejaVu Sans','axes.titlesize':14,'axes.labelsize':12}})
def save(p): plt.savefig(p,facecolor='white'); plt.close()
fig,ax=plt.subplots(figsize=(13.4,6.8)); ax.set_xlim(0,16); ax.set_ylim(0,10); ax.axis('off')
for x,y,w,h,t,c in [(0.8,6.6,2.7,1.3,'Question','#355070'),(4.1,6.6,2.8,1.3,'Assay design','#6d597a'),(7.5,6.6,3.0,1.3,'Computation','#b56576'),(11.1,7.4,2.7,1.3,'Interpretation','#2a9d8f'),(11.1,5.8,2.7,1.3,'Reporting','#e76f51')]:
 p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=0.12',edgecolor=c,facecolor=c,linewidth=1.6,alpha=0.94); ax.add_patch(p); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color='white',weight='bold')
for s,e in [((3.55,7.25),(4.05,7.25)),((6.95,7.25),(7.45,7.25)),((10.55,7.25),(11.0,8.05)),((10.55,7.05),(11.0,6.45))]:
 ax.add_patch(FancyArrowPatch(s,e,arrowstyle='-|>',mutation_scale=18,linewidth=2,color='#333333'))
ax.set_title(TITLES[0],weight='bold'); save(FIG_DIR/'fig1_workflow.png')
rng=np.random.default_rng(42); data=rng.normal(size=(10,10))
fig,ax=plt.subplots(figsize=(8.2,6.2)); im=ax.imshow(data,cmap='coolwarm',aspect='auto'); fig.colorbar(im, ax=ax, shrink=0.8); ax.set_title(TITLES[1],weight='bold'); save(FIG_DIR/'fig2_matrix.png')
rng=np.random.default_rng(2026); x1=rng.normal(-0.25,0.14,36); y1=rng.normal(0.12,0.12,36); x2=rng.normal(0.24,0.14,36); y2=rng.normal(-0.08,0.12,36)
fig,ax=plt.subplots(figsize=(8.1,6.1)); ax.scatter(x1,y1,s=70,c='#2a9d8f',edgecolors='black',linewidths=0.6,label='Group A'); ax.scatter(x2,y2,s=70,c='#e76f51',edgecolors='black',linewidths=0.6,label='Group B')
ax.axhline(0,color='#888',linestyle='--',linewidth=0.9); ax.axvline(0,color='#888',linestyle='--',linewidth=0.9); ax.legend(frameon=True); ax.set_title(TITLES[2],weight='bold'); save(FIG_DIR/'fig3_projection.png')
fig,ax=plt.subplots(figsize=(8.4,6.0)); cats=['Design','QC','Modeling','Interpretation','Reporting']; vals=[4,5,4,5,4]
ax.bar(cats,vals,color=['#355070','#6d597a','#b56576','#2a9d8f','#e76f51']); ax.set_ylim(0,6); ax.set_ylabel('Relative emphasis'); ax.set_title(TITLES[3],weight='bold'); save(FIG_DIR/'fig4_strategy.png')
print('Figures generated successfully.')
"""


def run(cmd, cwd):
    subprocess.run(cmd, cwd=str(cwd), check=True)


def clean_heading(heading):
    return re.sub(r"^\d+\.\s*", "", heading).strip()


def word_count(text):
    return len(re.findall(r"\b\w+\b", text))

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: build_review_package.py <json-file>")
    meta = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    pkg = Path(meta["dir"])
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "figures").mkdir(exist_ok=True)

    expanded_sections = [
        f"## {heading}\n{expand_section(meta['title'], heading, body, i, len(meta['sections']))}"
        for i, (heading, body) in enumerate(meta["sections"])
    ]
    sections = "\n\n".join(expanded_sections)
    refs = "\n".join([f"{i+1}. {r}" for i, r in enumerate(meta["refs"])])

    manuscript = dedent(f"""# {meta['title']}

## Abstract
{meta['abstract']}

## Keywords
{meta['keywords']}

{sections}

![{meta['figs'][0]}. This figure is a publication-style schematic prepared for tutorial reporting.](figures/fig1_workflow.png){{ width=90% }}

![{meta['figs'][1]}. This figure is an illustrative formatted example and does not represent a new study dataset.](figures/fig2_matrix.png){{ width=82% }}

Table: Practical decision matrix for computational study planning.

| Question type | Preferred analytical emphasis | Key reporting requirement |
| --- | --- | --- |
| Discovery-oriented | Broad exploratory analysis | Clear filtering and exploratory limits |
| Comparative cohort study | Statistical testing and covariate handling | Design formula and confounder reporting |
| Translational or clinical | Robust interpretation and validation | Explicit limitations and reproducibility |
| Atlas-building or systems analysis | Integration and uncertainty quantification | Transparent preprocessing and annotation logic |

Table: Minimum publication-ready computational reporting checklist.

| Domain | Minimum expectation |
| --- | --- |
| Study design | Primary question, inclusion logic, metadata plan |
| Data processing | Quality control, reference versions, filtering thresholds |
| Statistics | Normalization, model choice, covariates, multiple-testing approach |
| Validation | Sensitivity analysis, external support, or orthogonal evidence |
| Reproducibility | Software versions, code or workflow trace, figure provenance |

![{meta['figs'][2]}. This figure is an illustrative formatted example and does not represent a new study dataset.](figures/fig3_projection.png){{ width=82% }}

![{meta['figs'][3]}. This figure is a discipline-specific publication-style summary schematic.](figures/fig4_strategy.png){{ width=78% }}

## Declarations

### Author contributions
{AUTHOR['name']} conceived the tutorial review, prepared the manuscript, and approved the final version.

### Funding
No external funding was declared for preparation of this manuscript.

### Competing interests
The author declares no competing interests.

### Ethics approval and consent to participate
Not applicable. This tutorial review does not report a new human-participant or animal experiment.

### Consent for publication
Not applicable.

### Availability of data and materials
No new dataset was generated or analyzed for this tutorial review. Figures are educational schematics and illustrative formatted examples created for explanatory purposes.

### Author information
{AUTHOR['name']}, {AUTHOR['aff']}. ORCID: {AUTHOR['orcid']}.

## References
{refs}
""")

    approx_words = word_count(manuscript)

    title = dedent(f"""# Title Page

**Title:** {meta['title']}

**Article Type:** Tutorial Review

**Author:** {AUTHOR['name']}

**Affiliation:** {AUTHOR['aff']}

**Corresponding Author:**  
{AUTHOR['name']}  
{AUTHOR['aff']}  
Email: {AUTHOR['email']}  
Phone: {AUTHOR['phone']}  
ORCID: {AUTHOR['orcid']}

**Keywords:** {meta['keywords']}

**Running Title:** {meta['run']}

**Word Count:** Approximately {approx_words:,} words excluding title page and references

**Figures:** 4

**Tables:** 2
""")

    cover = dedent(f"""{AUTHOR['name']}  
{AUTHOR['aff']}  
Email: {AUTHOR['email']}  
Phone: {AUTHOR['phone']}  
ORCID: {AUTHOR['orcid']}  

1 April 2026

Editor-in-Chief  
Briefings in Bioinformatics  
Oxford University Press  

Subject: Submission of tutorial review manuscript

Dear Editor,

Please consider the enclosed manuscript, **"{meta['title']},"** for publication as a tutorial review in *Briefings in Bioinformatics*.

This manuscript was prepared as part of a structured computational omics review series and has been expanded into a full-length review with stronger section-specific framing, richer references, and publication-style figures. It is intended as an educational and methodological synthesis rather than a report of a new experimental dataset.

The submission is original, has not been published previously, and is not under consideration elsewhere. I am the sole author, have approved the submitted version, and declare no competing interests.

Sincerely,

{AUTHOR['name']}  
{AUTHOR['aff']}
""")

    readme = dedent("""# Submission Package Notes

## Contents
1. `Main_Manuscript.md` and `Main_Manuscript_Reviewed_Final.docx`
2. `Complete_Manuscript.docx`
3. `Title_Page.md` and `Title_Page.docx`
4. `Cover_Letter.md` and `Cover_Letter.docx`
5. `figures/`
6. `generate_figures.py`
""")

    (pkg / "Main_Manuscript.md").write_text(manuscript, encoding="utf-8")
    (pkg / "Title_Page.md").write_text(title, encoding="utf-8")
    (pkg / "Cover_Letter.md").write_text(cover, encoding="utf-8")
    (pkg / "ReadMe_Submission_Guidelines.md").write_text(readme, encoding="utf-8")
    (pkg / "generate_figures.py").write_text(FIG_SCRIPT.format(root=str(pkg), titles=repr(meta["figs"])), encoding="utf-8")

    is_windows = sys.platform == "win32"
    sep = ";" if is_windows else ":"

    run(["python", "generate_figures.py"], pkg)
    run(["pandoc", "Title_Page.md", "-o", "Title_Page.docx"], pkg)
    run(["pandoc", "Cover_Letter.md", "-o", "Cover_Letter.docx"], pkg)
    run(["pandoc", "Main_Manuscript.md", "-o", "Main_Manuscript_Reviewed_Final.docx", f"--resource-path=.{sep}figures"], pkg)
    run(["pandoc", "Title_Page.md", "Main_Manuscript.md", "-o", "Complete_Manuscript.docx", f"--resource-path=.{sep}figures"], pkg)


if __name__ == "__main__":
    main()
