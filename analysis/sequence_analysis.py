"""Validate the bundled single-record protein FASTA before computing properties."""
from collections import namedtuple
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
FASTA = ROOT / "data/p53.fasta"
VALID = set("ACDEFGHIKLMNPQRSTVWY")
MINIMUM_LENGTH = 100
Record = namedtuple("Record", "id description seq")

def load_validated_fasta(path=FASTA):
    records=[]; header=None; chunks=[]
    try: lines=Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc: raise ValueError(f"Cannot read FASTA {path}: {exc}") from exc
    for line in lines:
        line=line.strip()
        if not line: continue
        if line.startswith(">"):
            if header is not None: records.append((header,"".join(chunks)))
            header=line[1:].strip(); chunks=[]
        elif header is None: raise ValueError("FASTA sequence data appears before its header")
        else: chunks.append("".join(line.split()))
    if header is not None: records.append((header,"".join(chunks)))
    if len(records) != 1: raise ValueError(f"Expected exactly one FASTA record; found {len(records)}")
    description, sequence=records[0]; sequence=sequence.upper()
    if not sequence: raise ValueError("Protein sequence is empty")
    invalid=[(i,aa) for i,aa in enumerate(sequence,1) if aa not in VALID]
    if invalid:
        details=", ".join(f"{aa!r} at {i}" for i,aa in invalid[:20])
        raise ValueError(f"Unsupported residue(s) (only the 20 standard amino acids are accepted): {details}")
    if len(sequence)<MINIMUM_LENGTH: raise ValueError(f"Protein sequence is too short: {len(sequence)} residues; minimum is {MINIMUM_LENGTH}")
    record_id=description.split()[0] if description else "unnamed"
    return Record(record_id, description, sequence), sequence

def main():
    record, sequence=load_validated_fasta()
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    analysis=ProteinAnalysis(sequence)
    print(f"Protein ID: {record.id}\nDescription: {record.description}")
    print(f"Sequence length: {len(sequence)}; SHA-256: {hashlib.sha256(sequence.encode()).hexdigest()}")
    print("Amino acid composition:")
    for amino_acid,count in analysis.count_amino_acids().items(): print(f"{amino_acid}: {count}")
    print(f"Molecular weight (Da): {analysis.molecular_weight():.3f}")
    print(f"Aromaticity: {analysis.aromaticity():.4f}")
    print(f"Instability index: {analysis.instability_index():.3f}")
    print(f"Isoelectric point (pI): {analysis.isoelectric_point():.3f}")

if __name__ == "__main__": main()
