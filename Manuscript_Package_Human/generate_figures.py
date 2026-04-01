from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(r"D:\Computational Metagenomics\Manuscript_Package_Human")
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "figure.titlesize": 15,
        "figure.dpi": 220,
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
    }
)


def savefig(path: Path):
    plt.savefig(path, facecolor="white")
    plt.close()


def workflow_figure():
    fig, ax = plt.subplots(figsize=(13.6, 7.1))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 10)
    ax.axis("off")

    nodes = [
        (0.8, 6.7, 2.8, 1.35, "Clinical specimen\nand metadata", "#355070"),
        (4.0, 6.7, 2.9, 1.35, "QC and trimming", "#6d597a"),
        (7.2, 6.7, 3.2, 1.35, "Host-read removal\nprivacy-sensitive step", "#b56576"),
        (10.9, 7.5, 3.1, 1.35, "Taxonomy and function", "#2a9d8f"),
        (10.9, 5.6, 3.1, 1.35, "Assembly and MAGs", "#e76f51"),
        (14.3, 6.55, 2.2, 1.35, "Clinical\ninterpretation", "#7f5539"),
    ]

    for x, y, w, h, text, color in nodes:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            linewidth=1.8,
            edgecolor=color,
            facecolor=color,
            alpha=0.94,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, color="white", ha="center", va="center", weight="bold")

    arrows = [
        ((3.65, 7.35), (3.95, 7.35)),
        ((6.95, 7.35), (7.15, 7.35)),
        ((10.45, 7.35), (10.85, 8.15)),
        ((10.45, 7.2), (10.85, 6.25)),
        ((14.05, 8.15), (14.25, 7.35)),
        ((14.05, 6.25), (14.25, 7.0)),
    ]
    for start, end in arrows:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.0,
                color="#333333",
            )
        )

    ax.text(
        8.5,
        2.0,
        "Critical audit points: host-DNA proportion, low-biomass contamination, covariate structure,\n"
        "and ethics/privacy handling must be documented before biological claims are made.",
        ha="center",
        va="center",
        fontsize=11,
        color="#333333",
    )

    ax.set_title("Human Computational Metagenomics Workflow", weight="bold", pad=12)
    savefig(FIG_DIR / "fig1_human_workflow.png")


def beta_diversity():
    rng = np.random.default_rng(77)
    case_x = rng.normal(0.28, 0.14, 30)
    case_y = rng.normal(-0.06, 0.10, 30)
    control_x = rng.normal(-0.24, 0.12, 30)
    control_y = rng.normal(0.11, 0.09, 30)

    df = pd.DataFrame(
        {
            "PCoA1 (29.7%)": np.concatenate([control_x, case_x]),
            "PCoA2 (13.2%)": np.concatenate([control_y, case_y]),
            "Group": ["Control"] * 30 + ["Clinical case"] * 30,
        }
    )

    fig, ax = plt.subplots(figsize=(8.1, 6.2))
    sns.scatterplot(
        data=df,
        x="PCoA1 (29.7%)",
        y="PCoA2 (13.2%)",
        hue="Group",
        palette=["#2a9d8f", "#e76f51"],
        s=88,
        linewidth=0.7,
        edgecolor="black",
        ax=ax,
    )
    ax.axhline(0, color="#8d8d8d", linestyle="--", linewidth=0.9)
    ax.axvline(0, color="#8d8d8d", linestyle="--", linewidth=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Illustrative Beta-Diversity Pattern in a Human Cohort", weight="bold")
    savefig(FIG_DIR / "fig2_human_beta_diversity.png")


def volcano():
    rng = np.random.default_rng(2027)
    n = 420
    log2fc = rng.normal(0, 1.2, n)
    pvals = rng.uniform(0.001, 1.0, n)
    idx = rng.choice(n, 36, replace=False)
    log2fc[idx] = rng.choice([-1, 1], size=36) * rng.uniform(1.7, 4.5, size=36)
    pvals[idx] = rng.uniform(1e-6, 0.01, size=36)

    df = pd.DataFrame(
        {
            "log2FC": log2fc,
            "minus_log10_p": -np.log10(pvals),
            "status": "Not significant",
        }
    )
    df.loc[(pvals < 0.05) & (log2fc >= 1), "status"] = "Higher in cases"
    df.loc[(pvals < 0.05) & (log2fc <= -1), "status"] = "Higher in controls"

    fig, ax = plt.subplots(figsize=(8.5, 6.3))
    sns.scatterplot(
        data=df,
        x="log2FC",
        y="minus_log10_p",
        hue="status",
        palette={
            "Not significant": "#b9b9b9",
            "Higher in cases": "#e76f51",
            "Higher in controls": "#2a9d8f",
        },
        s=34,
        alpha=0.85,
        linewidth=0,
        ax=ax,
    )
    ax.axhline(-np.log10(0.05), color="black", linestyle="--", linewidth=1)
    ax.axvline(1, color="black", linestyle=":", linewidth=1)
    ax.axvline(-1, color="black", linestyle=":", linewidth=1)
    ax.set_xlabel("Log2 fold change")
    ax.set_ylabel("-log10 adjusted P value")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Illustrative Differential-Abundance Output for a Human Study", weight="bold")
    savefig(FIG_DIR / "fig3_human_volcano.png")


if __name__ == "__main__":
    workflow_figure()
    beta_diversity()
    volcano()
    print("Figures generated successfully.")
