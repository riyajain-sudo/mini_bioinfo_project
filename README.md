# In silico characterization of human p53 (P04637)

This small example validates the bundled human TP53 protein FASTA, computes sequence-derived physicochemical summaries, parses a **frozen, pre-existing BLAST XML snapshot**, and can optionally retrieve the direct UniProt record. It does not retrieve the FASTA from UniProt and the BLAST parser does not run BLAST. The saved search date/parameters are not established here. The UniProt script reports curated database annotation, **not a homology-based prediction**. These outputs are educational snapshots, not clinical interpretation or independent proof of broad evolutionary conservation.

## Setup

Python 3.10+ is recommended. From the repository root: `python -m venv .venv`, activate it, then `python -m pip install -r requirements.txt`. All data/results paths are anchored to the repository, so the commands below also work if invoked from another current directory using an absolute script path.

## Offline steps

```sh
python analysis/sequence_analysis.py
python analysis/homology_analysis.py
python -m unittest discover -s tests -v
```

Sequence metrics require exactly one FASTA record, at least 100 residues, and only the 20 standard amino-acid symbols; X, B, Z, U, O, stop markers and punctuation are rejected with positions before any metric is computed. The checked-in sequence has 393 residues. The BLAST summary excludes P04637 and full-query exact sequence matches and duplicate accessions, reports accession/title, percent identity, query coverage, E-value and score, and labels the results as a frozen snapshot. Archived XML metadata does not establish a reproducible database date or search parameters.

## Optional live UniProt retrieval

`python analysis/functional_annotation.py` makes an explicit network request to `https://rest.uniprot.org/uniprotkb/P04637.json` with a timeout and HTTP/schema checks. On failure, the previous report remains untouched. On success it atomically replaces `results/functional_annotation.txt` and records retrieval time. This online step is not needed for offline analysis/tests. No live BLAST/UniProt call is performed by the offline commands.
