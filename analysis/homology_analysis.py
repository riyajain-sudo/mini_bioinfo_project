"""Summarize the checked-in BLAST XML snapshot; no request is made here."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
XML = ROOT / "results/blast_results.xml"
OUTPUT = ROOT / "results/blast_results.txt"
FASTA = ROOT / "data/p53.fasta"
QUERY_ACCESSION = "P04637"

def accession_for(alignment):
    return (getattr(alignment, "accession", "") or "").strip()

def comparative_hits(blast_record, query_accession=QUERY_ACCESSION, limit=5):
    """Return top HSP per unique non-self accession; exact full self hits are omitted."""
    query_len = int(blast_record.query_length)
    seen, result = set(), []
    for alignment in blast_record.alignments:
        accession = accession_for(alignment)
        hsp = next(iter(alignment.hsps), None)
        if hsp is None:
            continue
        title = alignment.title
        if accession == query_accession or re.search(rf"\b{re.escape(query_accession)}\b", title):
            continue
        if accession and accession in seen:
            continue
        identity = hsp.identities / hsp.align_length if hsp.align_length else 0.0
        qstart, qend = getattr(hsp, "query_start", 0), getattr(hsp, "query_end", 0)
        coverage = (abs(qend - qstart) + 1) / query_len if qstart and qend and query_len else hsp.align_length / query_len if query_len else 0.0
        # A 100%-identical, full-query alignment is the same protein sequence even under another ID.
        if identity >= 1.0 and coverage >= 0.999:
            continue
        if accession:
            seen.add(accession)
        result.append({"accession": accession or "unknown", "title": title, "identity": identity,
                       "query_coverage": min(coverage, 1.0), "evalue": hsp.expect, "score": hsp.score})
        if len(result) >= limit:
            break
    return result

def main():
    if not XML.is_file():
        raise SystemExit(f"Frozen BLAST XML not found: {XML}. This script does not submit a live BLAST request.")
    try:
        from .sequence_analysis import load_validated_fasta
    except ImportError:
        from sequence_analysis import load_validated_fasta
    from Bio.Blast import NCBIXML
    record, sequence = load_validated_fasta()
    try:
        with XML.open(encoding="utf-8") as handle:
            blast = NCBIXML.read(handle)
    except Exception as exc:
        raise SystemExit(f"Could not parse BLAST XML {XML}: {exc}") from exc
    hits = comparative_hits(blast)
    with OUTPUT.open("w", encoding="utf-8") as out:
        out.write("Comparative BLAST hits (filtered frozen XML snapshot)\n")
        out.write(f"Query: {record.id}; length={len(sequence)}; XML query length={blast.query_length}\n")
        out.write(f"Database: {blast.database}; search date/parameters: not established by this repository\n")
        out.write("The saved XML is an archived search; this parser makes no current BLAST request. Self-accession and exact full-length sequence matches are omitted; these remaining hits alone do not demonstrate broad conservation.\n\n")
        for hit in hits:
            out.write(f"Accession: {hit['accession']}\nTitle/taxon: {hit['title']}\nPercent identity: {100*hit['identity']:.2f}%\nQuery coverage: {100*hit['query_coverage']:.2f}%\nE-value: {hit['evalue']}\nScore: {hit['score']}\n{'-'*50}\n")
    print(f"Wrote {len(hits)} filtered comparative hit(s) to {OUTPUT}")

if __name__ == "__main__": main()
