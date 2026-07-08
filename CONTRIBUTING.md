# Contributing

Thanks for your interest in extending this methodology stack. These skills were
built for target discovery in inflammatory/immune disorders and are meant to be
adapted to new diseases. This guide covers how the skills are structured, the
platform they run on, and the scientific conventions any contribution must
uphold.

## What these skills are

Each skill is an [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills):

```
skills/<skill-name>/
  SKILL.md      # YAML front-matter (name + description) then the workflow prose
  kernel.py     # optional: pure-compute helper functions loaded into the kernel
```

- **`SKILL.md`** is the workflow: when to use the skill, the ordered steps, the
  gotchas, and the honesty rules. It is read by an agent, so it is written as
  instructions, not as library docs.
- **`kernel.py`** ships only *pure-compute* helpers (sequence windowing, DOI
  dedup, tiering, burden aggregation). Retrieval and any connector/MCP calls
  (PubMed, OpenAlex, ClinicalTrials.gov, Open Targets) live in `SKILL.md`, not
  in `kernel.py`, because those run in a different execution context on the host
  platform.

### Platform context (important)

These skills are authored for the **Claude Science** platform: `kernel.py`
auto-loads into the analysis kernel when the skill is loaded, and the workflows
call platform connectors. They are **readable and adaptable as reference
methodology anywhere**, but they are not drop-in standalone scripts for a plain
Python environment. If you are porting a workflow to run outside the platform,
treat the `SKILL.md` as the spec and the `kernel.py` as the reusable core.

## kernel.py constraints

The kernel sidecar is validated before loading — only **definitions** may run at
import time. At the top level you may use:

- `def` / `async def` (no decorators; default arguments must be literals — use
  an `if x is None:` guard inside the body for computed defaults)
- `import` / `from … import name` (no `*`); defer third-party imports to inside
  function bodies so a fresh kernel doesn't fail to load the skill
- assignment of a **literal** constant to a plain name

Anything else at the top level (classes, calls, loops, non-literal assignments)
is rejected. Names starting with `_` are reserved. Function *bodies* have no
restrictions.

## Non-negotiable scientific conventions

Any change — new skill, new step, new disease adaptation — must preserve these.
They are the reason the stack is trustworthy, and they were each learned the
hard way:

1. **Presentation ≠ pathology.** MHC-binding / epitope predictions are *priors*,
   never a diagnosis. The specificity-defining evidence is always a functional
   T-cell readout. Report HLA findings as risk/capacity, never as disease. Do
   not add a step that names a trigger or asserts pathogenicity from binding
   prediction alone.
2. **Every cited claim carries a verified DOI.** No citation from memory; verify
   against Crossref or the reference library before a DOI goes into prose.
3. **Evidence tiering keeps the topical-specificity guardrail.** Citation count
   alone never promotes a reference to the landmark tier — it must also be
   on-topic. Do not weaken this; it is what keeps generic high-citation reviews
   out of Tier-1.
4. **State the honest ceiling.** Label evidence established vs emerging vs
   hypothesis-level. Do not describe an open-API, abstract-level synthesis as a
   full-text-read-of-every-paper review.
5. **Inclusive by design.** Antigen-specific platforms use HLA-agnostic
   eligibility and per-patient panels; predicted burden is a mechanistic
   covariate, never an enrollment gate.
6. **Prior-art / patents.** For any translation-bound claim, do a
   named-investigator prior-art search (not just a keyword sweep) and flag
   relevant patents.

## Adapting a skill to a new disease

The skills parameterize on the disease, the case/control contrast, the antigen
set, and the HLA panel. To retarget:

- **`omics-target-mining`** — swap the disease search terms, the Tier-1 dataset
  filter, and the canonical-marker panel.
- **`antigen-epitope-pipeline`** — swap the antigen UniProt accessions and the
  HLA allele panel (represent each antigen source by its full clinically
  relevant protein family, not a token protein).
- **`systematic-review-orchestration`** — swap the taxonomy (parts → subtopics →
  queries) and the `topic_terms` used by the tiering guardrail.

Prefer adding a worked example over hardcoding a new disease into the workflow.

## Proposing changes

1. Fork the repo and create a branch.
2. Keep each skill self-contained; don't create cross-skill imports in
   `kernel.py`.
3. If you change a `kernel.py` helper, note it in the skill's own workflow so
   `SKILL.md` and the sidecar stay in sync.
4. Open a pull request describing the change and which of the conventions above
   it touches (and confirming it preserves them).

## Scope

This is research methodology from a hackathon target-discovery project. It is
**not** clinical software and nothing here is validated for clinical use.
Contributions should keep that framing explicit.
