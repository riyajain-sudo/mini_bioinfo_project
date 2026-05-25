from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Read the FASTA file
record = SeqIO.read("../data/p53.fasta", "fasta")

# Extract sequence
sequence = str(record.seq)

# Create ProteinAnalysis object
analysis = ProteinAnalysis(sequence)
 
# Print information
print("Protein ID:")
print(record.id)

print("\nDescription:")
print(record.description)

print("\nProtein Sequence:")
print(record.seq)

print("\nSequence Length:")
print(len(sequence))

# Amino Acid Composition
print("\nAmino Acid Composition:")

composition = analysis.count_amino_acids()

for amino_acid, count in composition.items():
    print(amino_acid, ":", count)

# Molecular Weight
print("\nMolecular Weight:")
print(analysis.molecular_weight())

# Aromaticity
print("\nAromaticity:")
print(analysis.aromaticity())

# Instability Index
print("\nInstability Index:")
print(analysis.instability_index())

# Isoelectric Point
print("\nIsoelectric Point (pI):")
print(analysis.isoelectric_point())


#Sequence Filtering & Validation

print("\nSequence Filtering & Validation")

# Filtering criteria
minimum_length = 100

# Standard amino acids
valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

# Find invalid residues
invalid_residues = []

for residue in sequence:
    if residue not in valid_amino_acids:
        invalid_residues.append(residue)

# Decision making

if len(sequence) < minimum_length:
    print("Sequence rejected: Protein sequence is too short.")

elif len(invalid_residues) > 0:
    print("Sequence rejected: Invalid amino acids detected.")
    print("Invalid residues:", set(invalid_residues))

else:
    print("Sequence passed filtering criteria.")
    print("Sequence is suitable for downstream analysis.")