from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML

# # Read FASTA sequence
# record = SeqIO.read("../data/p53.fasta", "fasta")

# print("Running BLAST search...")

# # Run BLASTP
# result_handle = NCBIWWW.qblast(
#     program="blastp",
#     database="nr",               #non-redundant protein database
#     sequence=record.seq
# )

# # Save BLAST results
# with open("../results/blast_results.xml", "w") as out_file:
#     out_file.write(result_handle.read())

# print("BLAST search completed.")
# print("Results saved in blast_results.xml")

# Parse BLAST XML results
result_handle = open("../results/blast_results.xml")

blast_record = NCBIXML.read(result_handle)

# Save interpreted BLAST results
with open("../results/blast_results.txt", "w") as output_file:

    output_file.write("Top BLAST Hits\n\n")

    for alignment in blast_record.alignments[:5]:

        output_file.write(f"Hit: {alignment.title}\n")

        for hsp in alignment.hsps[:1]:

            output_file.write(f"E-value: {hsp.expect}\n")
            output_file.write(f"Identity: {hsp.identities}\n")
            output_file.write(f"Alignment Length: {hsp.align_length}\n")

        output_file.write("-" * 50 + "\n")

print("\nParsed BLAST results saved in blast_results.txt")