import re


def clean_heading(heading):
    return re.sub(r"^\d+\.\s*", "", heading).strip()


def infer_profile(article_title):
    title = article_title.lower()
    if "from genomics to spatiotemporal omics" in title:
        return "umbrella"
    if "emerging omics" in title:
        return "emerging"
    if "human genomics and transcriptomics" in title:
        return "genotx"
    if "multiomics integration" in title:
        return "multiomics"
    if "single-cell and spatial omics" in title:
        return "scspatial"
    if "spatiotemporal omics" in title:
        return "spatiotemporal"
    return "generic"


def classify_section(label):
    key = label.lower()
    if "introduction" in key:
        return "intro"
    if "design" in key or "assay" in key or "technology choice" in key or "fit-for-purpose" in key:
        return "design"
    if "preprocessing" in key or "workflow" in key or "processing" in key or "alignment" in key or "annotation" in key:
        return "processing"
    if "integration" in key or "model" in key or "networks" in key or "traject" in key or "interactions" in key:
        return "analysis"
    if "application" in key or "translational" in key or "outlook" in key or "future" in key:
        return "translation"
    if "risk" in key or "failure" in key or "pitfall" in key or "overclaim" in key or "error" in key:
        return "cautions"
    if "conclusion" in key:
        return "conclusion"
    return "general"


def generic_reporting_paragraph(label):
    section_type = classify_section(label)
    label = label.lower()
    mapping = {
        "intro": f"For manuscript preparation, the opening discussion of {label} should define scope, audience, and the main analytical question so later methodological choices feel necessary rather than decorative.",
        "design": f"For manuscript preparation, the section on {label} should make the study logic explicit: what question is being prioritized, why that assay or cohort structure was chosen, and which design constraints limit the strength of the eventual claim.",
        "processing": f"For manuscript preparation, the section on {label} should document references, thresholds, and quality filters in enough detail that the preprocessing logic can be reconstructed without guessing.",
        "analysis": f"For manuscript preparation, the discussion of {label} should separate exploratory outputs from inferential results and state what assumptions make the analytical model interpretable.",
        "translation": f"For manuscript preparation, the section on {label} should connect analytical findings back to intended use, making clear whether the work supports hypothesis generation, biological explanation, prediction, or near-clinical interpretation.",
        "cautions": f"For manuscript preparation, the section on {label} should identify the failure modes most likely to mislead readers and explain how those risks can be detected before they become part of the final narrative.",
        "conclusion": f"For manuscript preparation, the conclusion on {label} should synthesize the main lessons of the review and restate the practical standards that distinguish a defensible workflow from a merely complicated one.",
        "general": f"For manuscript preparation, the section on {label} should name the decision points, reference resources, and sensitivity checks that control interpretive risk.",
    }
    return mapping[section_type]


def generic_validation_paragraph(label):
    section_type = classify_section(label)
    label = label.lower()
    mapping = {
        "intro": f"It also helps to signal early what kinds of validation or external evidence will matter later, so readers understand from the outset which claims in {label} are meant to be descriptive and which are expected to support stronger inference.",
        "design": f"Validation expectations should be tied directly to {label}, because cohort structure, reference choice, and assay pairing determine whether replication, orthogonal assays, or sensitivity analysis will be the decisive credibility check.",
        "processing": f"Robustness in {label} is best demonstrated through explicit quality metrics, versioned resources, and sensitivity to reasonable threshold changes rather than by asserting that standard pipelines were followed.",
        "analysis": f"Results from {label} should therefore be accompanied by stability checks, alternative parameterizations, or orthogonal evidence whenever the output is being used to support mechanism, subtype definition, or clinical relevance.",
        "translation": f"The evidentiary bar in {label} should rise with the ambition of the claim: exploratory biological framing may tolerate internal consistency, whereas biomarker or clinical language requires external validation and much tighter calibration.",
        "cautions": f"A useful review does not only list problems in {label}; it also shows what checks, controls, or external comparisons would reveal that those problems are distorting the result.",
        "conclusion": f"A strong closing section should also remind readers that validation is not interchangeable across studies: the right confirmatory step depends on whether the manuscript’s main claim is descriptive, predictive, mechanistic, or translational.",
        "general": f"A strong section on {label} should also link method choice to downstream validation and reporting, stating which results are primarily descriptive and what additional evidence would be required for stronger claims.",
    }
    return mapping[section_type]


def generic_takeaway_paragraph(label):
    section_type = classify_section(label)
    label = label.lower()
    mapping = {
        "intro": f"The practical takeaway from {label} is that readers should finish the first section knowing exactly what problem the manuscript will solve and what kinds of conclusions it will deliberately avoid.",
        "design": f"The practical takeaway from {label} is to choose the minimum analytical complexity that truly serves the biological question, then document the tradeoffs before downstream results make those compromises harder to see.",
        "processing": f"The practical takeaway from {label} is that reproducibility usually fails at the level of quiet preprocessing decisions, so explicit thresholds and references are more valuable than long software lists.",
        "analysis": f"The practical takeaway from {label} is to treat elegant models as aids to reasoning rather than substitutes for evidence, especially when interpretation begins to outrun what the data directly support.",
        "translation": f"The practical takeaway from {label} is to match the language of impact to the strength of evidence, resisting clinical or mechanistic overstatement when the workflow is still best viewed as discovery-oriented.",
        "cautions": f"The practical takeaway from {label} is to treat these errors as expected analytical hazards, not as rare exceptions, and to build manuscript structure around showing they were checked.",
        "conclusion": f"The practical takeaway from {label} is that a good manuscript leaves the reader with a usable decision framework, not just an impression that the field is complex.",
        "general": f"The practical takeaway from {label} is to state what should be done by default, what should be justified explicitly, and which shortcuts most often weaken the final claim.",
    }
    return mapping[section_type]


SPECIFIC_EXPANSIONS = {
    "multiomics": {
        "introduction": [
            "{seed_text} In practice, the attraction of multiomics is that no single molecular layer fully captures disease biology, treatment response, or host-environment interaction. Genomic variation may define predisposition, transcription may reflect active programs, methylation may encode regulatory state, and proteomic or metabolomic measurements may track nearer-term physiology. The promise of integration is therefore real, but it only materializes when these layers are measured on a coherent study backbone.",
            "The main practical difficulty is that different assays do not fail in the same way. RNA-seq data are count-based and sensitive to library composition, proteomics data often contain missing values linked to detection limits, methylation arrays or sequencing generate platform-specific biases, and metabolomics features may remain only partially annotated. A strong tutorial review must therefore show readers how to respect modality-specific data structure before attempting any integrative model.",
            "This review is most useful when it frames multiomics as a sequence of design and inference problems: selecting modalities, preserving biospecimen comparability, handling incomplete sample overlap, choosing an integration level, and deciding what kind of biological statement can be defended at the end. That framing is what separates a full-length manuscript from a catalog of integration software."
        ],
        "designing multiomics studies": [
            "{seed_text} The first decision is whether the study really requires multiple layers or whether one well-powered assay would answer the question more cleanly. In oncology, for example, combining DNA, RNA, methylation, and proteomics may clarify subtype structure or treatment resistance, but only if the same biological specimens or tightly matched aliquots are available. If sample provenance diverges across layers, integration becomes a technical exercise rather than a biological one.",
            "Design quality in multiomics depends heavily on synchrony. The interval between biopsy, preservation, extraction, and assay generation can introduce modal discordance that later appears as biology. Researchers therefore need explicit metadata on specimen handling, platform batches, repeated measures, and whether each modality was generated for all individuals or only a nested subset. Those choices determine if the analytic target is a fully paired cohort, a partially overlapping cohort, or a reference-plus-validation design.",
            "Power considerations are also different from single-modality studies. A cohort that is adequate for differential expression may be weak for latent-factor learning across five assays. Investigators should therefore define the primary integration objective in advance: supervised prediction, subtype discovery, cross-modal association, mechanistic hypothesis generation, or patient stratification. The answer drives sample size expectations and the degree of acceptable missingness."
        ],
        "modality-specific preprocessing": [
            "{seed_text} Good integration starts with disciplined preprocessing within each modality. Variant calls need reference-aware filtering and annotation; transcriptomic counts need normalization and low-count handling; proteomic intensities need missingness assessment, peptide-to-protein summarization, and batch correction; metabolomic features need peak alignment, drift correction, and annotation confidence tracking. Collapsing these steps into a generic 'preprocessed matrix' hides where the strongest biases arise.",
            "Identifier harmonization is another underappreciated step. Genes, proteins, pathways, CpG sites, metabolites, and microbial features occupy different abstraction levels, and mapping them too early can destroy useful structure. Many strong studies keep the original feature space long enough to perform modality-native quality checks, then connect layers through curated identifiers, pathway databases, networks, or latent variables instead of forcing one-to-one feature equivalence.",
            "The main reporting obligation here is to state exactly what was filtered, transformed, imputed, or batch-corrected in each assay. Without that clarity, downstream integration is difficult to interpret because observed concordance might reflect biology, common preprocessing artifacts, or information leakage from overly aggressive harmonization."
        ],
        "integration strategies": [
            "{seed_text} Early integration by simple feature concatenation is tempting because it is easy to implement, but it usually works only when sample size is generous, feature selection is disciplined, and all layers are measured on the same individuals. Otherwise, high-dimensional noise from one modality can dominate the combined representation. This is why many multiomics studies now favor intermediate approaches that learn latent factors or shared embeddings while preserving modality-specific variance.",
            "Intermediate integration can be attractive when the goal is subtype discovery or shared biological programs. Methods such as matrix factorization, variational latent models, or graph-based manifold learning can reveal cross-modal structure, but only if investigators assess factor stability and biological interpretability. An unstable factor that changes with modest preprocessing adjustments should not be narrated as a disease mechanism.",
            "Late integration is often more defensible in translational settings. Separate models can be built within each layer and then combined at the prediction or evidence level, which makes performance attribution clearer and reduces pressure to force heterogeneous data into one space. The best choice therefore depends on whether the study emphasizes biological explanation, prediction, missing-data tolerance, or regulatory interpretability."
        ],
        "statistical learning and networks": [
            "{seed_text} Cross-modal correlation maps and network analyses are common starting points because they provide intuitive summaries of coordinated biology. However, correlation alone is vulnerable to confounding by cell composition, tumor purity, inflammation, treatment exposure, and hidden batch structure. Network edges should therefore be interpreted as statistical associations unless supported by perturbational or orthogonal evidence.",
            "More formal learning methods such as canonical correlation analysis, partial least squares, Bayesian integration, graph neural models, or multimodal classifiers can capture higher-order structure, but they substantially raise the bar for validation. Investigators need to show that performance or discovered factors persist across resampling, external cohorts, or modality dropout experiments. Otherwise, the model may be learning platform-specific artifacts rather than cross-modal biology.",
            "Interpretability matters especially when the output is meant to guide clinical or mechanistic conclusions. Factor loadings, pathway enrichments, and feature-importance summaries should be linked back to recognizable biology, not treated as self-validating because the mathematics is sophisticated. A technically complex model that cannot support a transparent biological explanation often adds less value than a simpler integrative analysis."
        ],
        "missing data and confounding": [
            "{seed_text} Multiomics cohorts almost never have complete data for every participant and every assay. Tissue may be exhausted, some analytes may fail quality control, and certain modalities may be generated only for a nested discovery set. Analysts should therefore define the anchoring cohort explicitly and distinguish complete-case analyses from analyses that tolerate partial overlap.",
            "Imputation can be useful, but its meaning differs across layers. In proteomics, missingness may reflect abundance below detection; in methylation or transcriptomics, missingness may arise from technical failure or low-quality samples; in clinical metadata, absence may reflect workflow limitations. Treating all missing values as exchangeable can distort downstream integration. Sensitivity analyses that compare complete-case, imputed, and reduced-modality models are often more informative than a single optimized pipeline.",
            "Confounding is equally important. Age, sex, ancestry, medication, sampling site, storage batch, and tissue composition can induce coordinated changes across modalities that look like elegant integrative biology. Publication-ready manuscripts therefore need to show how these variables were measured, where they entered the design or model, and whether the main conclusions remain after adjustment."
        ],
        "translational applications": [
            "{seed_text} In oncology, integration of DNA, RNA, methylation, proteomics, and immune features can refine subtype definitions and identify resistance mechanisms that are invisible within one assay alone. In immunology, combined transcriptomic, epigenomic, and proteomic readouts can distinguish activation state from lineage commitment. In cardiometabolic or inflammatory disease, integrative models may connect inherited risk with dynamic physiology and treatment response.",
            "The key translational question is what the integrated analysis adds. A manuscript is stronger when it can show that multi-layer evidence changes classification confidence, narrows a candidate mechanism, or improves predictive performance in a way that is clinically meaningful. Simply demonstrating that several assays correlate with the same phenotype is not enough to justify the additional complexity and cost.",
            "Clinical ambition should also determine evidentiary standards. If the study aims at biomarker development, external validation and calibration are essential. If the study aims at mechanistic interpretation, targeted experiments or independent cohorts are more important than marginal improvements in internal model fit."
        ],
        "common overclaims": [
            "{seed_text} A common overclaim is to present concordant signals across assays as proof of causal mechanism. In reality, several layers can move together because of a shared confounder such as cell composition or treatment exposure. Another recurrent problem is narrating unstable clusters or factors as novel subtypes without showing reproducibility across preprocessing choices or cohorts.",
            "Small-sample machine learning is another major source of inflated claims. Multiomics datasets are high dimensional, and aggressive feature selection performed before cross-validation can create misleadingly strong performance. Manuscripts should clarify where feature selection occurred, how leakage was prevented, and whether class imbalance or nested resampling was handled correctly.",
            "Review articles in this field should also caution against novelty bias. A multiomics analysis is not automatically better because it is technologically ambitious. The decisive question is whether integration materially improves explanation, prediction, or intervention design beyond what the strongest single-modality analysis already achieved."
        ],
        "conclusion": [
            "{seed_text} The main practical lesson from multiomics is that integration is a design problem before it is a machine-learning problem. Studies succeed when specimen matching, assay quality, missing-data logic, and inferential goals are coherent before modeling begins. Without that foundation, even elegant latent-factor methods produce fragile stories.",
            "A strong conclusion should also leave the reader with a realistic standard for success. The goal is not to use every available assay, but to combine the minimum set of modalities that answer the biological question more convincingly than any single layer could. That is the threshold that makes integration defensible in publication and practice.",
            "For future work, the most credible direction is not maximal complexity but better calibration: benchmark datasets with partial overlap, transparent reporting of preprocessing decisions, and clearer links between integrated signals and actionable biology. Those elements will matter more than any single new integration algorithm."
        ],
    },
    "genotx": {
        "introduction": [
            "{seed_text} Human sequencing studies are often described as mature, yet the path from FASTQ files to clinically credible interpretation remains full of judgment calls. Read mapping, variant calling, transcript quantification, annotation, phenotype linkage, and disease-specific evidence synthesis each introduce assumptions that can alter the final conclusion. A review in this domain therefore needs to connect laboratory output to clinical reasoning, not just describe software.",
            "The genomics-transcriptomics combination is especially powerful because it links inherited or acquired sequence change with functional consequence. A rare coding variant may gain plausibility when expression or splicing is abnormal in a relevant tissue, while an RNA-seq outlier may become interpretable when anchored to a structural variant or copy-number event. The computational challenge is to integrate these lines of evidence without overstating causality.",
            "This manuscript is strongest when it treats clinical interpretation as an endpoint of disciplined evidence handling. That means tracking reference genome choice, transcript models, ancestry-aware population frequency resources, somatic versus germline context, and the difference between research-grade prioritization and formal clinical classification."
        ],
        "study design and assay selection": [
            "{seed_text} Assay choice should follow the disease model and the expected class of genomic variation. Whole-genome sequencing is more appropriate when structural variants, noncoding regulation, repeat expansions, or complex rearrangements matter; exome sequencing remains efficient for coding rare disease studies; targeted panels may be sufficient for defined hereditary syndromes or hotspot-driven cancers. Bulk RNA-seq or total RNA-seq becomes most valuable when splicing, fusion detection, or expression outliers are central to the question.",
            "Clinical context changes design requirements. Germline studies benefit from trios, extended pedigrees, or ancestry-matched controls because segregation and allele-frequency interpretation are central. Tumor studies introduce purity, ploidy, copy-number background, subclonality, and the availability of matched normal tissue. These design features should be explicit because they determine what classes of calls are interpretable later.",
            "The study should also define whether the primary endpoint is diagnosis, gene discovery, biomarker development, therapeutic stratification, or mechanistic follow-up. That choice affects acceptable false-positive rates, the depth of validation needed, and whether the analysis prioritizes sensitivity, specificity, or interpretability."
        ],
        "core genomic preprocessing": [
            "{seed_text} The foundation of genomic analysis is still careful handling of raw reads, reference alignment, duplicate marking where appropriate, base-quality recalibration or analogous correction, and calibrated variant calling. Yet high-quality pipelines also need to state which reference build, decoy or alt-aware resources, and transcript annotations were used, because these choices affect comparability and downstream annotation.",
            "In cancer sequencing, preprocessing must separate distinct signal types rather than collapsing everything into a single variant list. Single-nucleotide variants and indels are only one layer; copy-number alterations, structural variants, mutational signatures, and fusion events often drive the clinically relevant biology. A full-length review should therefore explain why these classes require different callers, quality filters, and evidentiary standards.",
            "Quality control is not a clerical step. Coverage uniformity, contamination estimates, insert-size behavior, strand bias, mapping quality, and sample identity checks determine whether negative results are meaningful and whether apparent rare variants are believable. Publication-ready methods sections should state these metrics, not merely claim that standard QC was performed."
        ],
        "variant annotation and prioritization": [
            "{seed_text} Annotation pipelines assign predicted consequence, gene context, transcript context, and population frequency, but interpretation begins only after those labels are connected to phenotype and disease mechanism. In rare disease, prioritization often depends on inheritance model, gene-disease validity, tissue relevance, and whether the candidate transcript is actually expressed in the affected organ. In oncology, therapeutic and prognostic interpretation depends on tumor type, clonality, co-mutation context, and evidence tiering.",
            "Population resources such as gnomAD are powerful, but they are not neutral filters. Frequency thresholds must be calibrated to disease prevalence, penetrance, ancestry composition, and the expected inheritance model. Overly simple frequency cutoffs can eliminate real candidates in underrepresented populations or retain implausible variants when ancestry is mismatched.",
            "Predictive scores and in silico tools should be presented as supporting evidence rather than adjudicators of truth. SIFT, PolyPhen, SpliceAI, CADD, conservation measures, and similar tools can help prioritize, but they are not substitutes for segregation, orthogonal assays, transcript evidence, or curated clinical databases."
        ],
        "transcriptomic quantification and differential expression": [
            "{seed_text} RNA-seq analysis begins with read quality control, alignment or pseudoalignment strategy, transcriptome reference choice, and expression summarization, but the inferential quality of the study depends on normalization and design specification. Low-count filtering, batch effects, tissue heterogeneity, repeated measures, and unwanted variation can all dominate the signal if ignored.",
            "Differential expression tables are often overinterpreted because they are visually persuasive. A publication-quality manuscript should therefore pair statistical significance with effect size, mean expression context, and pathway-level synthesis. For clinically oriented studies, it is also important to distinguish broad expression shifts from interpretable outliers, aberrant splicing, fusion-driven signals, or allele-specific effects that directly inform mechanism.",
            "RNA-seq contributes most when it is treated as evidence with structure, not as a generic list of upregulated and downregulated genes. Pathway analysis, gene-set enrichment, and network context can be useful, but they should be anchored to the study design and phenotype rather than used as after-the-fact narrative decoration."
        ],
        "integrative interpretation": [
            "{seed_text} Joint interpretation becomes powerful when different data types address different uncertainty. A putative pathogenic splice-site variant gains credibility if RNA-seq shows aberrant exon usage; a somatic amplification becomes more compelling when linked to increased transcript abundance; a candidate fusion is strengthened by matching structural and expression evidence. These are the kinds of cross-modal links that make genomics and transcriptomics complementary rather than redundant.",
            "Even so, corroboration is not causation. Expression change may reflect treatment, inflammation, cell-type mixture, or a broad stress program rather than direct consequence of a specific variant. Analysts should therefore differentiate between evidence that supports plausibility, evidence that narrows alternatives, and evidence that functionally validates a mechanism.",
            "The most defensible integrative studies are explicit about biological context. Tissue relevance, developmental timing, tumor purity, and the availability of matched controls all influence whether DNA-RNA concordance can be interpreted strongly. That context should be part of the main narrative, not hidden in supplementary material."
        ],
        "common analytical failures": [
            "{seed_text} One recurrent failure is reference drift: using outdated genome builds, transcript models, or annotation databases that materially affect variant consequence and gene prioritization. Another is overreliance on generic pathogenicity scores without matching them to phenotype, inheritance model, or transcript relevance. These shortcuts often produce long candidate lists with weak clinical value.",
            "In transcriptomics, a common failure is volcano-plot storytelling, where the visual prominence of a gene outruns the evidentiary basis for its interpretation. Hidden batch effects, sample swaps, tissue heterogeneity, and low replicate counts can all create persuasive but fragile findings. Studies should show how these risks were checked before major claims are made.",
            "Clinical overreach remains the most important caution. Variants of uncertain significance, borderline expression signatures, and exploratory pathway enrichments should not be narrated as actionable findings without appropriate evidence tiers and validation. Review articles should be firm on that point because translational credibility depends on it."
        ],
        "translational applications": [
            "{seed_text} In rare disease, combined sequencing and transcript analysis can support molecular diagnosis, resolve variants that alter splicing, and reduce the search space when phenotype alone is nonspecific. In oncology, integrated DNA and RNA profiling can refine tumor classification, identify actionable fusions, characterize pathway activation, and inform resistance mechanisms. In pharmacogenomics and hereditary risk assessment, the value lies in connecting sequence findings to clinically interpretable evidence.",
            "The strongest translational manuscripts do not stop at reporting hits. They show how computational outputs affect classification confidence, management decisions, or biological understanding relative to standard practice. Even when the work remains research-oriented, there should be a clear line between exploratory findings and those with near-term clinical implications.",
            "Validation strategy should match the claim. Orthogonal sequencing, targeted assays, pathology correlation, family segregation, functional experiments, or external cohorts each serve different purposes. The manuscript should specify which type of validation is relevant rather than invoking validation as a generic aspiration."
        ],
        "conclusion": [
            "{seed_text} The most useful takeaway is that sequence analysis becomes clinically persuasive only when the computational chain is transparent from raw data to final interpretation. Reference choice, filtering, annotation, statistical modeling, and phenotype linkage are not background details; they are the basis of credibility.",
            "A strong genomics-transcriptomics workflow also resists false certainty. Many findings will remain suggestive rather than definitive, and that is acceptable if the evidentiary status is stated clearly. Readers benefit more from a review that distinguishes plausible, likely, and clinically actionable findings than from one that implies all integrated signals are equally informative.",
            "Future improvements in this area will come from better harmonized annotation resources, broader ancestry representation, richer transcript-level interpretation, and cleaner integration between research pipelines and clinical reporting frameworks. Those advances will matter more than small gains from swapping one caller or differential expression package for another."
        ],
    },
    "emerging": {
        "introduction": [
            "{seed_text} What unifies these newer domains is not a common assay chemistry but a shared problem: each promises access to biology that was previously hard to observe, yet each arrives before standards, benchmarks, and mature computational pipelines are fully settled. That makes emerging omics especially attractive and especially vulnerable to overinterpretation.",
            "Spatial proteomics, perturb-omics, epitranscriptomics, exposomics, and liquid biopsy multiomics generate very different data objects, but they all strain conventional workflows. Analysts must manage unusual measurement error, sparse or ambiguous annotations, evolving reference resources, and an evidence base that may still be uneven across diseases and specimen types.",
            "A useful review in this space therefore needs to be explicitly practical. It should ask which technologies are analytically mature enough for publication-grade inference, which are best used for hypothesis generation, and what extra safeguards are needed before novelty is translated into biomedical claims."
        ],
        "spatial proteomics": [
            "{seed_text} Spatial proteomics is powerful because proteins sit closer to phenotype than transcripts and because tissue architecture often determines biological interpretation. Imaging mass cytometry, multiplexed immunofluorescence, CODEX-like platforms, and related methods can identify cell states, tissue neighborhoods, and immune organization, but only after careful segmentation, channel normalization, spillover control, and marker-panel harmonization.",
            "Unlike bulk proteomics, the signal here is inseparable from image quality and morphology. Poor segmentation can create false cell types, signal bleed can simulate marker co-expression, and tissue damage or fixation artifacts can distort neighborhood analysis. Review articles should therefore explain that image-processing decisions are part of the core analytical pipeline, not a cosmetic prelude to downstream statistics.",
            "The strongest studies combine protein-level spatial signals with pathology review, orthogonal staining, or matched transcriptomic information. That triangulation is important because biological narratives about immune niches, tumor borders, or stromal programs are easy to overstate when derived from one imaging panel alone."
        ],
        "perturb-omics": [
            "{seed_text} Perturb-omics is attractive because it moves beyond passive observation and links molecular readout to experimentally imposed change. CRISPR screens coupled to single-cell transcriptomics, chromatin accessibility, or multimodal profiling can reveal regulatory programs and genetic dependencies at high resolution, but they also introduce specific technical risks.",
            "Guide assignment, multiplicity of infection, editing efficiency, cell-state selection effects, and indirect downstream responses all complicate interpretation. A differential expression signature after perturbation does not automatically identify the direct target pathway, particularly when knockout efficiency varies or when the perturbation alters cell viability. These issues should be central in any computational roadmap for the field.",
            "Strong analyses therefore model guide-level variability, include appropriate controls, and distinguish reproducible perturbation effects from assay noise or clonal bottlenecks. The value of perturb-omics lies in causal leverage, but that leverage depends on careful experimental accounting and conservative downstream inference."
        ],
        "epitranscriptomics": [
            "{seed_text} Epitranscriptomic assays attempt to measure RNA modifications such as m6A, m5C, pseudouridine, and related marks, often with antibody-based enrichment, direct RNA sequencing, or specialized chemical approaches. The computational challenge is to separate genuine modification signatures from changes caused by transcript abundance, isoform structure, sequence context, or platform bias.",
            "This field is especially sensitive to reference annotation quality because modifications are often interpreted relative to transcript position, isoform usage, and motif context. Peak calling, site resolution, replicate handling, and normalization across transcripts with very different expression levels can all alter the apparent biology. A review in this area should make clear that many pipelines still infer more than they directly observe.",
            "Interpretation is strongest when modification evidence is integrated with independent expression, splicing, ribosome profiling, or perturbation data. Without that context, it is easy to narrate broad RNA modification maps as regulatory mechanisms even when the assay mainly captures correlated transcript abundance patterns."
        ],
        "exposomics": [
            "{seed_text} Exposomics aims to characterize the environmental, dietary, occupational, and chemical exposures that shape disease risk across the life course. Computationally, it resembles a difficult mixture of untargeted metabolomics, biomarker discovery, longitudinal epidemiology, and annotation science. Large numbers of features may be detected, while only a fraction can be identified with high confidence.",
            "Batch effects, instrument drift, seasonality, biospecimen timing, and co-exposure structure complicate nearly every analysis. Association testing is therefore only one part of the problem; feature filtering, annotation confidence, adduct handling, and replication are equally important. Reviews should be explicit that the exposure signal can be technically unstable even before phenotype modeling begins.",
            "Because exposomics sits close to public health interpretation, confounding control matters enormously. Diet, geography, occupation, medication, and socioeconomic structure can all create broad correlations. The best studies align exposure feature processing with rigorous epidemiologic design rather than treating high-dimensional feature tables as self-explanatory."
        ],
        "liquid biopsy multiomics": [
            "{seed_text} Liquid biopsy multiomics combines cell-free DNA, methylation patterns, fragmentomics, cell-free RNA, circulating proteins, and other analytes from blood or related minimally invasive samples. The attraction is obvious: repeated sampling, lower procedural burden, and potential early detection or response monitoring. The computational burden is equally obvious because the signal fraction is often small and analytes behave very differently.",
            "Low tumor fraction, clonal hematopoiesis, preanalytical handling differences, and platform-specific background noise can all erode specificity. Analysts need to model signal detection limits, error suppression, and modality agreement carefully. A positive result in one analyte layer does not automatically validate another, particularly when each has different sensitivity to tumor burden or inflammatory context.",
            "The best liquid biopsy studies are careful about intended use. Early detection, minimal residual disease monitoring, and therapy-response tracking impose different tolerances for false positives and false negatives. Manuscripts should show how that intended use shaped the choice of analytes, thresholds, and validation cohort design."
        ],
        "readiness and fit-for-purpose": [
            "{seed_text} A central practical question is not whether a technology is exciting, but whether it is mature enough for the specific biomedical claim being made. Some platforms are already reliable for exploratory profiling or tissue mapping, whereas others remain best suited for focused hypothesis generation or benchmark development. Review articles should help readers make that distinction instead of treating all emerging assays as equally deployable.",
            "Fit-for-purpose evaluation should include reproducibility across sites, availability of reference datasets, annotation maturity, throughput, cost, and the existence of software that can be defended in a publication setting. A method with impressive biological resolution may still be a weak choice for a clinical or population-scale study if the preprocessing pipeline is unstable or the evidence base is thin.",
            "This is also where novelty bias should be addressed directly. A newer assay is not automatically the right assay. In many projects, the best computational decision is to pair one emerging modality with a well-established companion assay rather than relying entirely on an immature platform."
        ],
        "common computational risks": [
            "{seed_text} Benchmark weakness is one of the defining risks in emerging omics. Many methods are first evaluated on highly curated showcase datasets, leaving uncertain how they behave across laboratories, tissue types, disease contexts, and sample quality gradients. As a result, published performance claims may be more optimistic than real-world use warrants.",
            "Annotation immaturity is another recurring problem. Proteomic markers may lack harmonized panels, exposomic features may remain putative, RNA modification sites may depend on evolving transcript models, and liquid biopsy signatures may be trained on narrow cohorts. Reviews should therefore encourage authors to communicate uncertainty in labels and feature identities rather than presenting every detected signal as settled biology.",
            "Translational overstatement is the final major risk. Emerging assays often enter the literature with language of precision medicine or early diagnosis before the computational robustness is proven. Full-length manuscripts in this area should insist on external validation, realistic intended-use framing, and explicit discussion of failure modes."
        ],
        "conclusion": [
            "{seed_text} The common lesson across emerging omics is that novelty increases both opportunity and interpretive risk. New assays can open biologically important windows, but they require unusually careful attention to preprocessing, reference resources, benchmarking, and claim calibration.",
            "A strong conclusion should leave readers with a fit-for-purpose mindset. The right question is not whether an assay is fashionable, but whether its data structure, analytical maturity, and validation ecosystem are adequate for the study objective. That principle is what turns a fast-moving technology review into a useful computational guide.",
            "As these fields mature, the most valuable advances will likely be shared standards, open benchmark datasets, clearer annotation confidence frameworks, and better integration with established modalities. Those infrastructure gains will determine whether emerging omics becomes routine science or remains a collection of impressive but fragile demonstrations."
        ],
    },
    "scspatial": {
        "introduction": [
            "{seed_text} These technologies matter because tissue biology is organized at the level of cells, neighborhoods, and anatomical context, not only at the level of averaged molecular profiles. Single-cell assays resolve heterogeneity, while spatial assays preserve location and morphology. Together they allow investigators to ask which cells are present, where they sit, and how local environment reshapes state.",
            "The computational difficulty is that cellular resolution does not guarantee interpretive clarity. Dissociation bias, ambient RNA, doublets, segmentation errors, sparse counts, and uncertain annotation all influence the final map. Attractive UMAPs or tissue overlays can conceal these issues unless the workflow is described with enough discipline.",
            "A full-length review in this area should therefore connect wet-lab constraints, matrix-level preprocessing, image-aware spatial analysis, and the biological limits of inferred trajectories or communication networks. That integration is what readers need when moving from atlas generation to defensible inference."
        ],
        "technology choice and study design": [
            "{seed_text} Technology selection starts with the biological question and the specimen. Some studies need dissociated single cells to resolve immune or stromal diversity, others benefit from nuclei because frozen tissues or fragile cell types are involved, and others require intact sections because architecture itself is the primary signal. Throughput, panel size, transcriptome breadth, imaging compatibility, and tissue availability all influence the right choice.",
            "Sample handling is particularly important. Dissociation can deplete fragile populations and induce stress-response transcription, while fixation and embedding strategies affect spatial signal preservation. If paired single-cell and spatial assays are planned, investigators should decide early whether one modality will serve as the reference and the other as the localization layer, because that choice shapes both sampling and downstream integration.",
            "Study design should also specify whether the aim is discovery atlas building, group comparison, intervention response, developmental mapping, or pathology-linked interpretation. These goals impose different expectations for replicate structure, covariate modeling, and how much annotation uncertainty is acceptable."
        ],
        "single-cell workflow": [
            "{seed_text} The main single-cell pipeline begins with count matrix generation and proceeds through cell-level quality filtering, empty-droplet handling where relevant, doublet detection, normalization, variable feature selection, dimensionality reduction, graph construction, clustering, and marker-based annotation. Each of these steps is familiar, but each can materially change downstream biological labels.",
            "Quality thresholds deserve explicit justification because they are tissue and platform dependent. Mitochondrial content, total counts, detected features, and ribosomal fraction can reflect true biology as well as poor-quality cells. Overly rigid filtering may remove activated or metabolically extreme states, whereas lax filtering can produce artifactual clusters driven by damaged cells or ambient RNA contamination.",
            "Annotation is the most interpretively sensitive step. Marker panels, reference mapping, hierarchical labels, and manual curation should be aligned with tissue context and not treated as interchangeable. A publication-ready review should emphasize that cell types, cell states, and transient programs require different evidentiary standards."
        ],
        "spatial workflow": [
            "{seed_text} Spatial analysis adds a second layer of complexity because expression must be interpreted together with coordinates, histology, and in many platforms imperfect spatial resolution. Depending on the technology, the analytical unit may be a segmented cell, a multi-cell spot, or a multiplexed imaging pixel neighborhood. Those units are not interchangeable and should be described explicitly.",
            "Image preprocessing and segmentation are central. Tissue folds, staining variability, autofluorescence, nuclei segmentation errors, and misregistration between imaging channels can all produce false spatial patterns. Analysts should therefore document image QC, segmentation strategy, and any manual correction steps before presenting neighborhood maps or spatially variable features.",
            "Statistical interpretation also needs restraint. Spatial autocorrelation, uneven tissue composition, and region-size imbalance can create convincing visual gradients that are not specific biological programs. Robust studies combine formal spatial testing with pathology-aware interpretation and sensitivity to segmentation or spot-resolution assumptions."
        ],
        "integration of single-cell and spatial data": [
            "{seed_text} Integration typically treats single-cell profiles as the high-resolution reference and spatial data as the anatomical scaffold. Deconvolution, label transfer, and probabilistic mapping can estimate which cell states occupy each region, but the answer depends heavily on annotation quality, platform compatibility, and whether the reference captures all relevant states present in the tissue.",
            "This becomes especially important in diseased tissues where dissociation bias may remove fragile populations or where treatment alters states not present in a healthy reference atlas. Analysts should therefore test alternative annotation granularities and, where possible, compare mapping results across methods rather than presenting one transferred label set as definitive.",
            "The most convincing integrative studies use mapping to support focused biological questions, such as localizing an inflammatory program, explaining a tumor border niche, or relating neuronal states to cortical layers. Broad claims about complete tissue organization are much harder to support and require more extensive validation."
        ],
        "trajectories and interactions": [
            "{seed_text} Trajectory inference can be useful for developmental systems, regeneration, immune activation, or treatment response, but it often reconstructs plausible order rather than directly observed lineage history. Pseudotime should therefore be described as a computational ordering unless true temporal labels or lineage tracing are available.",
            "Cell-cell communication analyses face similar limits. Ligand-receptor frameworks can highlight candidate interactions between neighboring or co-occurring states, yet transcript presence alone does not prove secretion, receptor occupancy, or functional signaling. Spatial context can narrow the hypothesis, but it does not automatically validate it.",
            "The best manuscripts use trajectories and interaction analyses to generate mechanistic leads that are then compared with orthogonal data, perturbation experiments, or established biology. That stance is more credible than treating inferred arrows or communication networks as direct observations."
        ],
        "common pitfalls": [
            "{seed_text} Overclustering is one of the most common errors because it converts gradual variation, cell cycle effects, or technical artifacts into apparently novel states. Another is assigning labels from a small number of familiar markers without considering alternative lineages, tissue context, or transitional programs.",
            "Visual embeddings create additional traps. UMAP proximity is not a formal metric of lineage distance, and a visually distinct island may reflect parameter choice more than biology. In spatial datasets, low-quality spots or segmentation artifacts can likewise masquerade as microenvironments if image QC is weak.",
            "Review articles should also warn about dissociation artifacts, batch-driven clusters, and the temptation to equate atlas scale with analytical quality. Bigger cell counts do not compensate for unclear design or unstable annotation."
        ],
        "translational applications": [
            "{seed_text} In cancer, these methods can delineate tumor-immune neighborhoods, treatment-resistant compartments, and stromal programs that are invisible in bulk assays. In immunology and infection, they can map local activation states and tissue-specific immune organization. In neuroscience and developmental biology, they can relate molecular programs to anatomical layers and temporal progression.",
            "Their translational value comes from contextual interpretation. A biomarker defined by a cell state may behave differently depending on spatial niche, surrounding immune composition, or tissue architecture. That is why these assays can be more informative than bulk profiles for pathology-linked questions, provided the study remains focused.",
            "Still, translational use demands conservative claims. Small tissue cohorts, limited pathology diversity, and uncertain spatial label transfer can easily produce elegant but non-generalizable narratives. External cohorts, orthogonal staining, and pathology review remain critical."
        ],
        "conclusion": [
            "{seed_text} The practical strength of single-cell and spatial omics is not resolution for its own sake, but the ability to connect molecular state, cellular identity, and tissue organization within the same study. That advantage becomes real only when preprocessing, annotation, and spatial interpretation are handled with unusual care.",
            "A strong closing message is that these assays are most convincing when applied to focused tissue questions with replicate-aware design and pathology-grounded interpretation. They are least convincing when used only to produce large atlases with minimal control over uncertainty.",
            "Future progress will depend on better benchmark tissues, improved segmentation and mapping standards, stronger integration with histopathology, and clearer reporting of annotation confidence. Those developments will make the field more useful than simply adding more cells or more colorful embeddings."
        ],
    },
    "spatiotemporal": {
        "introduction": [
            "{seed_text} The key difference from static spatial biology is that this field tries to represent processes rather than snapshots. Developmental progression, regeneration, treatment response, and disease evolution all require claims about order, timing, and movement across tissue context. That makes the computational problem fundamentally harder than describing a single well-annotated section.",
            "Spatiotemporal studies combine at least three sources of complexity: spatial registration, temporal alignment, and molecular interpretation. Each can fail independently. A false correspondence between sections can create an apparent trajectory, and a strong pseudotime model can still be misleading if the spatial alignment or sampling scheme is weak.",
            "A practical review must therefore emphasize what kind of time is actually available in the data. Some studies observe time directly through serial sampling, some reconstruct it from developmental stage collections, and others infer it computationally from state similarity. Those are not equivalent evidentiary situations."
        ],
        "study design for dynamic tissues": [
            "{seed_text} Study design begins by defining whether temporal information is experimentally observed or computationally reconstructed. Repeated sampling from the same organism, aligned serial sections, synchronized perturbation experiments, and cross-sectional cohorts arranged by stage all support different kinds of claims. The manuscript should make that distinction explicit because it determines how strongly progression can be interpreted.",
            "Sampling interval is also central. Fast processes such as immune infiltration after therapy or wound healing may require dense timepoints, whereas developmental atlases may tolerate broader staging if morphology is stable and stage assignment is reliable. Sparse sampling can still be valuable, but only if the analysis avoids implying fine-grained kinetics that the data cannot actually resolve.",
            "Metadata matters here more than in static studies. Intervention timing, tissue orientation, section depth, anatomical landmarks, and specimen-level covariates all influence alignment and interpretation. Without them, differences across timepoints can reflect collection artifacts rather than biology."
        ],
        "registration and temporal alignment": [
            "{seed_text} Accurate registration is the technical backbone of spatiotemporal inference. Whether alignment is performed through image landmarks, morphology-informed warping, atlas-based coordinates, or molecular similarity, the chosen reference frame controls every later claim about movement, persistence, or regional transition.",
            "Registration error is not merely a nuisance variable. Small misalignments can create artificial gradients, suggest migration that did not occur, or obscure true boundaries between compartments. Review articles should therefore discuss quality metrics for alignment, uncertainty visualization, and how conclusions change when the reference frame is perturbed.",
            "Temporal alignment has its own hazards. When timepoints are unequally sampled or pooled across individuals, computational smoothing may imply continuity that is not directly observed. Analysts should clarify where interpolation was used and where the results remain anchored only to discrete observations."
        ],
        "dynamic modeling strategies": [
            "{seed_text} Dynamic modeling in this field ranges from simple stage-wise comparisons to pseudotime reconstruction, graph diffusion, optimal transport, tensor decomposition, and mechanistic dynamical systems. The correct choice depends on whether the goal is descriptive ordering, transition probability estimation, lineage coupling, or explicit state dynamics.",
            "Pseudotime is useful when direct temporal labels are incomplete, but it should not be narrated as measured time. Likewise, optimal transport or graph-based trajectory models can reveal plausible flows between states, yet they depend strongly on neighborhood construction, regularization, and how the state space was defined. These assumptions deserve main-text discussion because they shape the biological narrative.",
            "Model outputs should also be linked back to tissue structure. A compelling dynamic result is one that explains where transitions occur, which compartments are stable, and how state change relates to morphology or intervention timing. Models that remain only in latent space are harder to interpret biologically."
        ],
        "integration with references": [
            "{seed_text} Reference datasets are often used to label states, constrain trajectories, or compare observed tissue programs with better-characterized single-cell atlases. This can substantially improve interpretability, especially when the spatiotemporal assay has limited feature depth. But references also import assumptions about annotation, stage definition, and the completeness of known cell states.",
            "A strong analysis therefore tests whether conclusions persist under alternative references or coarser annotation schemes. This matters especially in regeneration and disease settings, where transitional or treatment-induced states may not exist in the canonical atlas. Overconfident label transfer can erase exactly the novel biology the study hopes to capture.",
            "Reference integration works best when it is used to bound uncertainty rather than to eliminate it. The manuscript should describe how much of the signal is directly observed in the target data and how much is inferred by borrowing structure from external resources."
        ],
        "common inferential errors": [
            "{seed_text} Treating pseudotime as literal time is the most frequent conceptual error, but it is not the only one. Another is failing to distinguish changes in abundance from changes in location. A cell type may appear to move across tissue simply because one region expands or contracts, not because individual cells migrate.",
            "Section effects are another major risk. Differences in section thickness, orientation, staining, or imaging quality can create temporal-looking patterns that disappear once alignment uncertainty is considered. Analysts should show that major trends are not driven by one problematic slice or one poorly matched timepoint.",
            "Overinterpretation of gradients is also common. Spatially smooth trends can be visually compelling, yet they may reflect averaging, tissue composition, or registration artifacts. Review articles should encourage formal checks before assigning developmental or disease-progression meaning to these patterns."
        ],
        "biological applications": [
            "{seed_text} Developmental systems are an obvious application because cell-state transitions unfold in defined anatomical space. Embryology, organogenesis, and neural patterning all benefit from models that link lineage progression to tissue compartments. Regeneration and wound healing pose similar questions, but with intervention timing and inflammatory context layered on top.",
            "In cancer and chronic disease, spatiotemporal approaches can illuminate clonal expansion, immune remodeling, stromal adaptation, and therapy response. These settings are especially challenging because repeated sampling may be sparse and treatment itself changes tissue architecture, making alignment and interpretation more difficult than in developmental atlases.",
            "The most compelling application papers answer focused questions about when and where key transitions occur. Broad claims about total tissue dynamics are harder to defend unless the sampling design, alignment quality, and validation burden are exceptionally strong."
        ],
        "reporting standards": [
            "{seed_text} Reporting needs to be more explicit here than in static spatial studies because the reader must understand both the coordinate system and the temporal logic. Manuscripts should specify how time was observed or inferred, what anatomical reference was used, how sections were registered, and how uncertainty was represented.",
            "It is also important to state which parts of the workflow are descriptive and which are model-based. Interpolated maps, smoothed trajectories, and borrowed annotations can be highly informative, but they should be labeled as such. Without that transparency, readers may mistake inferred continuity for direct observation.",
            "Sensitivity analysis should be treated as standard rather than optional. Alternative alignments, trajectory parameters, stage definitions, or reference atlases can materially change conclusions. A publication-ready spatiotemporal paper should show at least the main robustness checks in the core manuscript."
        ],
        "conclusion": [
            "{seed_text} Spatiotemporal omics is valuable because it lets investigators ask dynamic questions in their anatomical setting, but that advantage comes with a much higher inferential burden than static atlas work. Claims about progression, movement, or response are only as strong as the registration, sampling design, and uncertainty handling that support them.",
            "The strongest closing message is therefore one of disciplined ambition. These methods are worth using when the biological question genuinely concerns change over time in tissue context, not merely because four-dimensional plots look modern or comprehensive.",
            "As the field matures, better alignment benchmarks, standardized uncertainty reporting, and richer multimodal reference atlases will likely matter more than incremental increases in modeling complexity. Those advances will make dynamic tissue biology more reproducible and more clinically credible."
        ],
    },
    "umbrella": {
        "introduction": [
            "{seed_text} The practical challenge for modern investigators is no longer access to one omics workflow, but deciding how far along the resolution ladder a given question needs to go. Sequence variation, expression, multimodal coupling, single-cell heterogeneity, spatial structure, and time-resolved tissue dynamics all offer different kinds of evidence. More resolution can reveal more biology, but it also increases preprocessing burden, model complexity, and failure modes.",
            "An umbrella review is useful only if it clarifies what each layer contributes and where the additional complexity becomes justified. That means comparing modalities not as a prestige hierarchy, but as a set of tools with different inferential targets. Readers should come away knowing when a bulk RNA-seq study is enough, when a multiomics design adds decisive value, and when single-cell or spatial resolution changes the biological answer.",
            "The article is strongest when it treats modern omics as a continuum of decisions rather than a menu of technologies. Assay choice, preprocessing transparency, interpretation limits, and translational caution recur across all domains even though the data objects differ."
        ],
        "the resolution hierarchy": [
            "{seed_text} Genomics provides the most stable view of inherited or acquired sequence change, transcriptomics adds dynamic regulation, multiomics links layers, single-cell assays resolve cellular heterogeneity, spatial methods preserve tissue architecture, and spatiotemporal approaches attempt to model change within that architecture. Each step upward adds biological specificity, but also new uncertainty and greater dependence on preprocessing choices.",
            "This hierarchy is useful because it exposes the tradeoff between breadth and interpretability. Bulk assays often support larger cohorts and cleaner statistical models, whereas high-resolution assays produce richer local insight but usually on smaller and more technically complex datasets. A strong umbrella review should make that tradeoff explicit rather than implying that later technologies automatically supersede earlier ones.",
            "The hierarchy also helps separate inferential targets. Variant classification, differential expression, latent-factor discovery, cell-state annotation, neighborhood analysis, and dynamic trajectory modeling are fundamentally different outputs. Confusing them leads to overclaiming, especially when visually rich downstream methods are treated as stronger evidence than simpler upstream assays."
        ],
        "shared design principles": [
            "{seed_text} Across all omics domains, the first principle is to define the biological question before choosing the assay. The second is to preserve the metadata needed to support that question: cohort structure, covariates, specimen handling, timing, anatomical context, and batch variables. The third is to define the inferential target clearly so that preprocessing and modeling decisions remain aligned with the objective.",
            "These principles sound obvious, but they are where many studies fail. Investigators often inherit data generated for one purpose and then impose a more ambitious analytical story later. When design and question are mismatched, the resulting workflow may be technically sophisticated yet conceptually weak. That is true whether the assay is whole-genome sequencing or spatial transcriptomics.",
            "An umbrella review should therefore emphasize decision discipline over tool novelty. Readers need to understand how to choose the minimum complexity necessary for the question, because unnecessary assay escalation usually increases uncertainty faster than it improves insight."
        ],
        "data processing across modalities": [
            "{seed_text} Although each modality has its own specialized pipeline, they all depend on the same foundational tasks: quality control, reference management, filtering, normalization or transformation, and careful joining with metadata. What differs is the object being processed, whether it is reads, variant calls, count matrices, protein intensities, segmented cells, or aligned tissue sections.",
            "This cross-domain view is valuable because it shows where failures recur under different names. A bad genome build, an outdated transcript annotation, an unstable integration reference, poor segmentation, or weak registration all play the same role: they distort the data before the interpretive step begins. Review articles should highlight those parallels because they help readers transfer good habits across domains.",
            "The most publication-relevant message is that preprocessing choices deserve main-text visibility. In nearly every omics field, the dominant analytical errors arise before formal statistics. Hiding those decisions in supplementary methods weakens both reproducibility and trust."
        ],
        "interpretation and integration": [
            "{seed_text} Modern omics studies increasingly combine outputs from different levels of resolution, but interpretation depends on knowing what each output actually represents. A variant call reflects sequence evidence, a differential expression list reflects modeled abundance change, a latent factor reflects shared statistical structure, and a spatial neighborhood reflects coordinate-informed association. These are not interchangeable kinds of biological proof.",
            "Integration is most useful when it narrows uncertainty by combining complementary evidence. For example, genomics and transcriptomics may connect variant effect to expression or splicing, while single-cell and spatial data may connect state to anatomical niche. Problems arise when integration is used rhetorically, with each additional layer treated as automatic validation regardless of its own uncertainty.",
            "A good umbrella review should therefore teach interpretive hierarchy. Some outputs are descriptive, some are inferential, and some are mechanistic only when supported by orthogonal validation. That distinction matters more than any specific software brand."
        ],
        "common cross-domain failures": [
            "{seed_text} Weak design, underreported filtering, unresolved batch effects, and association-mechanism confusion are not isolated problems of one field; they recur across nearly every omics domain. The forms differ, but the logic is the same: visually impressive outputs can outrun the quality of the underlying data and study design.",
            "Another recurring failure is assay overreach. Investigators sometimes use a high-resolution modality simply because it is available, then make claims that the cohort size, annotation confidence, or preprocessing stability cannot sustain. In other cases, simpler assays are treated as inherently inferior even when they would have supported stronger statistical inference.",
            "An umbrella review is useful when it names these patterns explicitly. Doing so helps readers recognize that many failures are structural rather than modality-specific, and that good analytical habits can transfer across very different datasets."
        ],
        "clinical and translational outlook": [
            "{seed_text} Clinical translation is now a realistic goal across multiple omics domains, but the route to translation differs by assay. Genomics already supports diagnosis and therapeutic stratification in defined settings, transcriptomics contributes molecular classification and pathway interpretation, and higher-resolution modalities promise better tissue-contextualized biomarkers. The more complex the modality, the more rigorous the validation burden becomes.",
            "This section should therefore compare not only technical capability but readiness for use. Some assays are already embedded in clinical workflows, while others remain strongest as discovery tools or trial-enrichment strategies. Translational writing is most persuasive when it separates those categories clearly instead of implying that all omics outputs are equally close to implementation.",
            "Clinical ambition also sharpens the need for conservative interpretation. A finding that is acceptable as a hypothesis in exploratory biology may be inappropriate as a biomarker claim. That distinction should anchor any roadmap that spans multiple omics technologies."
        ],
        "future directions": [
            "{seed_text} The field is moving toward multimodal, image-linked, and longitudinal designs in which previously separate assays are measured or modeled together. This trend is scientifically productive because biological systems are layered, contextual, and dynamic. It is also analytically demanding because each new layer adds preprocessing complexity and widens the space of plausible overclaims.",
            "The most important future advances may therefore be infrastructural rather than glamorous: benchmark datasets spanning modalities, better shared ontologies, interoperable file formats, stronger provenance tracking, and clearer uncertainty reporting. These elements make it possible to compare methods and carry results across studies.",
            "An umbrella review should also caution that the future is not automatically more complex. In many settings, smarter assay selection and better study design will yield more robust science than maximal multimodal measurement. Progress depends on choosing complexity where it is justified."
        ],
        "conclusion": [
            "{seed_text} The central lesson across omics domains is that added analytical resolution is worthwhile only when it sharpens the answer to a real biological or clinical question. More layers, more cells, more spatial detail, or more timepoints are not goals in themselves; they are tools with specific evidentiary strengths and limits.",
            "A useful integrated roadmap therefore teaches readers how to choose among modalities, how to recognize shared failure modes, and how to communicate uncertainty honestly. That perspective is more durable than any single pipeline because technologies will keep changing while the underlying logic of defensible analysis remains stable.",
            "For future work, the best outcome is a field that becomes both more integrated and more disciplined. Better benchmarks, clearer reporting, and fit-for-purpose assay selection will make modern omics more reproducible and more useful than simply layering on additional technical complexity."
        ],
    },
}


def expand_section(article_title, heading, seed_text, position, total):
    label = clean_heading(heading)
    key = label.lower()
    profile = infer_profile(article_title)
    paragraphs = SPECIFIC_EXPANSIONS.get(profile, {}).get(key)

    if paragraphs is None:
        paragraphs = [
            f"{seed_text} This section should explain why the analytical choice matters for downstream interpretation and which errors it is designed to prevent.",
            f"In practical studies, choices around {label.lower()} depend on cohort structure, assay behavior, metadata quality, and the precise inferential target rather than software availability alone.",
            generic_reporting_paragraph(label),
            generic_validation_paragraph(label),
            generic_takeaway_paragraph(label),
        ]
    else:
        paragraphs = list(paragraphs) + [generic_validation_paragraph(label), generic_takeaway_paragraph(label)]

    return "\n\n".join(
        p.format(seed_text=seed_text, article_title=article_title, position=position, total=total)
        for p in paragraphs
    )
