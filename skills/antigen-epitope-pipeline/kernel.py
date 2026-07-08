"""Helpers for the antigen-epitope / pMHC pipeline skill.

Pure-compute utilities for the disease-agnostic epitope-mapping workflow:
antigen sequence -> peptide windows -> (external MHC prediction) -> per-HLA
burden. The MHC prediction step itself is env-specific (netMHCIIpan via IEDB,
or mhcnuggets in a TF env) and lives in SKILL.md, not here.
"""

STRONG_IC50_NM = 500.0        # class-II strong-binder threshold (nM)
DEFAULT_CLASSII_K = 15        # class-II core-containing peptide length
DEFAULT_CLASSI_K = 9          # class-I peptide length


def fetch_uniprot_fasta(accession, timeout=30):
    """Fetch a UniProt sequence by accession. Returns (header, sequence)."""
    import requests
    url = "https://rest.uniprot.org/uniprotkb/" + accession + ".fasta"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    lines = r.text.strip().splitlines()
    header = lines[0].lstrip(">") if lines else accession
    seq = "".join(l.strip() for l in lines[1:])
    return header, seq


def sliding_windows(seq, k=None, step=1):
    """All length-k peptide windows over a sequence.

    Returns list of (start_1based, peptide). k defaults to class-II 15-mer.
    """
    if k is None:
        k = DEFAULT_CLASSII_K
    seq = "".join(seq.split())
    out = []
    for i in range(0, len(seq) - k + 1, step):
        out.append((i + 1, seq[i:i + k]))
    return out


def summarize_binders(rows, allele_key="allele", antigen_key="antigen",
                      ic50_key="ic50", threshold=None):
    """Aggregate a flat list of prediction dicts into strong-binder counts.

    rows: iterable of dicts with allele/antigen/ic50 fields.
    Returns dict with per_allele, per_antigen, per_allele_antigen counts and
    the total number of strong binders (ic50 < threshold).
    """
    if threshold is None:
        threshold = STRONG_IC50_NM
    per_allele = {}
    per_antigen = {}
    per_pair = {}
    total = 0
    for row in rows:
        try:
            ic50 = float(row.get(ic50_key))
        except (TypeError, ValueError):
            continue
        if ic50 >= threshold:
            continue
        total += 1
        al = row.get(allele_key, "NA")
        ag = row.get(antigen_key, "NA")
        per_allele[al] = per_allele.get(al, 0) + 1
        per_antigen[ag] = per_antigen.get(ag, 0) + 1
        key = al + "|" + ag
        per_pair[key] = per_pair.get(key, 0) + 1
    return {"total_strong": total, "per_allele": per_allele,
            "per_antigen": per_antigen, "per_allele_antigen": per_pair,
            "threshold_nM": threshold}


def unique_core_count(rows, core_key="core", ic50_key="ic50", threshold=None):
    """Count distinct strong-binding cores (dedups shared cores across alleles).

    Guards against the common double-count bug where per-cell sums inflate the
    true number of unique binding cores.
    """
    if threshold is None:
        threshold = STRONG_IC50_NM
    cores = set()
    for row in rows:
        try:
            ic50 = float(row.get(ic50_key))
        except (TypeError, ValueError):
            continue
        if ic50 < threshold and row.get(core_key):
            cores.add(row[core_key])
    return len(cores)
