from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(r"D:\Computational Metagenomics\Manuscript_Package")
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
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    }
)


def savefig(path: Path):
    plt.savefig(path, facecolor="white")
    plt.close()


def workflow_figure():
    fig, ax = plt.subplots(figsize=(13.5, 6.8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    colors = {
        "design": "#274c77",
        "amplicon": "#2a9d8f",
        "shotgun": "#e76f51",
        "stats": "#6d597a",
        "report": "#7f5539",
    }

    boxes = [
        (0.8, 6.6, 2.6, 1.4, "Study design\nmetadata, controls", colors["design"]),
        (4.0, 7.7, 3.1, 1.4, "16S workflow\nQC -> ASVs -> taxonomy", colors["amplicon"]),
        (4.0, 4.7, 3.1, 1.4, "Shotgun workflow\nQC -> profiling or assembly", colors["shotgun"]),
        (8.3, 6.2, 3.0, 1.8, "Statistical layer\nfiltering, diversity,\ndifferential abundance", colors["stats"]),
        (12.1, 6.2, 2.8, 1.8, "Transparent reporting\nfigures, tables,\ndeclarations", colors["report"]),
    ]

    for x, y, w, h, text, color in boxes:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            linewidth=1.8,
            edgecolor=color,
            facecolor=color,
            alpha=0.92,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", weight="bold")

    arrows = [
        ((3.45, 7.3), (3.95, 8.35)),
        ((3.45, 7.3), (3.95, 5.35)),
        ((7.15, 8.35), (8.2, 7.35)),
        ((7.15, 5.35), (8.2, 6.85)),
        ((11.35, 7.1), (12.0, 7.1)),
    ]

    for start, end in arrows:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.0,
                color="#3a3a3a",
            )
        )

    ax.text(
        8.0,
        1.15,
        "Decision principle: choose assay and analysis depth according to the biological question,\n"
        "then apply compositional-aware statistics and transparent reporting.",
        ha="center",
        va="center",
        fontsize=11,
        color="#333333",
    )

    ax.set_title("Computational Metagenomics Tutorial Framework", weight="bold", pad=14)
    savefig(FIG_DIR / "fig1_workflow_overview.png")


def alpha_diversity():
    rng = np.random.default_rng(42)
    data = pd.DataFrame(
        {
            "Shannon diversity": np.concatenate(
                [
                    rng.normal(4.4, 0.35, 28),
                    rng.normal(3.55, 0.45, 28),
                ]
            ),
            "Group": ["Reference cohort"] * 28 + ["Clinical cohort"] * 28,
        }
    )

    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    palette = ["#2a9d8f", "#e76f51"]
    sns.boxplot(
        data=data,
        x="Group",
        y="Shannon diversity",
        hue="Group",
        palette=palette,
        width=0.55,
        dodge=False,
        legend=False,
        ax=ax,
    )
    sns.stripplot(data=data, x="Group", y="Shannon diversity", color="#333333", alpha=0.55, size=4, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Shannon index")
    ax.set_title("Illustrative Alpha-Diversity Comparison", weight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    savefig(FIG_DIR / "fig2_alpha_diversity.png")


def beta_diversity():
    rng = np.random.default_rng(123)
    healthy_x = rng.normal(-0.22, 0.11, 26)
    healthy_y = rng.normal(0.15, 0.10, 26)
    disease_x = rng.normal(0.21, 0.12, 26)
    disease_y = rng.normal(-0.12, 0.11, 26)

    data = pd.DataFrame(
        {
            "PCoA1 (31.8%)": np.concatenate([healthy_x, disease_x]),
            "PCoA2 (14.6%)": np.concatenate([healthy_y, disease_y]),
            "Group": ["Reference cohort"] * 26 + ["Clinical cohort"] * 26,
        }
    )

    fig, ax = plt.subplots(figsize=(8.0, 6.1))
    sns.scatterplot(
        data=data,
        x="PCoA1 (31.8%)",
        y="PCoA2 (14.6%)",
        hue="Group",
        palette=["#2a9d8f", "#e76f51"],
        s=90,
        linewidth=0.7,
        edgecolor="black",
        ax=ax,
    )
    ax.axhline(0, color="#8a8a8a", linestyle="--", linewidth=0.9)
    ax.axvline(0, color="#8a8a8a", linestyle="--", linewidth=0.9)
    ax.set_title("Illustrative Beta-Diversity Ordination", weight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    savefig(FIG_DIR / "fig3_beta_diversity.png")


def volcano_plot():
    rng = np.random.default_rng(2026)
    n = 450
    log2fc = rng.normal(0, 1.15, n)
    pvals = rng.uniform(0.001, 1.0, n)
    idx = rng.choice(n, 34, replace=False)
    log2fc[idx] = rng.choice([-1, 1], size=34) * rng.uniform(1.5, 4.8, size=34)
    pvals[idx] = rng.uniform(1e-6, 0.01, size=34)

    df = pd.DataFrame(
        {
            "log2FC": log2fc,
            "minus_log10_p": -np.log10(pvals),
            "status": "Not significant",
        }
    )
    df.loc[(pvals < 0.05) & (log2fc >= 1), "status"] = "Higher in clinical cohort"
    df.loc[(pvals < 0.05) & (log2fc <= -1), "status"] = "Lower in clinical cohort"

    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    sns.scatterplot(
        data=df,
        x="log2FC",
        y="minus_log10_p",
        hue="status",
        palette={
            "Not significant": "#b8b8b8",
            "Higher in clinical cohort": "#e76f51",
            "Lower in clinical cohort": "#2a9d8f",
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
    ax.set_title("Illustrative Differential-Abundance Volcano Plot", weight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    savefig(FIG_DIR / "fig4_volcano_plot.png")


if __name__ == "__main__":
    workflow_figure()
    alpha_diversity()
    beta_diversity()
    volcano_plot()
    print("Figures generated successfully.")
