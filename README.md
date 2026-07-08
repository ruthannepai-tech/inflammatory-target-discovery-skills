# Inflammatory-Disease Target-Discovery Skills

A reusable, disease-agnostic methodology stack for **computational target discovery and antigen-specific therapeutic design** in inflammatory and immune-mediated disorders — eosinophilic GI diseases (EoE and other EGIDs), celiac disease, IBD, and autoimmune disease broadly.

These three skills were developed during a target-discovery effort for **eosinophilic esophagitis (EoE)** and generalized so the disease, the case/control contrast, the antigen set, and the HLA panel are all parameters. Swap them and the same pipelines run for a new disorder.

## The stack

| Skill | What it does |
|---|---|
| [`omics-target-mining`](skills/omics-target-mining/) | Mine public omics (GEO, ArrayExpress, PRIDE, CELLxGENE) → reproducible cross-study differential-expression meta-signature → single-cell validation → Open Targets druggability-ranked target shortlist. |
| [`antigen-epitope-pipeline`](skills/antigen-epitope-pipeline/) | Antigen set → UniProt sequences → peptide windows → MHC-II/I binding prediction → per-HLA epitope burden → personalized pMHC panel. |
| [`systematic-review-orchestration`](skills/systematic-review-orchestration/) | Taxonomy → multi-database retrieval (PubMed + OpenAlex + citation-graph) → DOI dedup → LLM relevance screen → Tier-1/2/3 evidence rubric → evidence-map figure. |

They compose: mine targets → ground the rationale in a tiered literature base → map candidate antigens to HLA-resolved epitopes for antigen-specific diagnostics/therapeutics.

## Design principles baked into the skills

- **Presentation ≠ pathology.** MHC-binding/epitope predictions are *priors*, never a diagnosis. The specificity-defining evidence is always a functional T-cell readout. HLA findings are reported as risk/capacity, never as disease.
- **Every cited claim carries a verified DOI.** No citation from memory; DOIs are checked against Crossref / the reference library.
- **Evidence tiering with a topical-specificity guardrail.** High citation count alone never earns Tier-1 — a reference must also be on-topic, so generic high-citation reviews don't pollute the landmark tier.
- **Honest ceilings.** Computational work is labeled established vs emerging vs hypothesis-level; open-API literature synthesis is not claimed as a full-text-read-of-every-paper review.
- **Inclusive by design.** Antigen-specific platforms use HLA-agnostic eligibility and per-patient panels; predicted burden is a mechanistic covariate, never an enrollment gate.

## Format

Each skill is an [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills): a `SKILL.md` (name + description front-matter, then the workflow) and an optional `kernel.py` of pure-compute helper functions that load into the analysis kernel. They run on the Claude Science platform but the `SKILL.md` workflows and `kernel.py` helpers are readable and adaptable independently.

## Status

Research methodology from a hackathon target-discovery project. Not clinical software; nothing here is validated for clinical use. See each skill's honesty/provenance section for scope and limits.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — skill anatomy, `kernel.py` constraints, the non-negotiable scientific conventions, and how to adapt a skill to a new disease.

## License

MIT — see [LICENSE](LICENSE).
