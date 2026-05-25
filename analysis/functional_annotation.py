import requests
import json

# UniProt accession ID
accession_id = "P04637"

# UniProt API URL
url = f"https://rest.uniprot.org/uniprotkb/{accession_id}.json"

# Send request to UniProt
response = requests.get(url)

# Convert response to JSON
data = response.json()
# print(data.keys())
# print("*"*50)
# print(data["proteinDescription"])
# print("*"*50)
# print(data["organism"])
# print("*"*50)
# print(data["genes"])

#Extract important information

protein_name = data["proteinDescription"]["recommendedName"]["fullName"]["value"]

organism = data["organism"]["scientificName"]

gene_name = data["genes"][0]["geneName"]["value"]

#Extract function comment
function_text = "Function annotation not found."

for comment in data["comments"]:
    if comment["commentType"] == "FUNCTION":
        function_text = comment["texts"][0]["value"]
        break

# Create annotation report

annotation_report = f"""
Functional Annotation Report
============================

Protein Name:
{protein_name}

Gene Name:
{gene_name}

Organism:
{organism}

UniProt Accession:
{accession_id}

Predicted Function:
{function_text}
"""

# Save annotation report

with open("../results/functional_annotation.txt", "w", encoding="utf-8") as file:
    file.write(annotation_report)

print("Functional annotation retrieved successfully.")
print("Annotation saved in functional_annotation.txt")













# #Functional Annotation

# # Functional annotation text
# annotation = """
# Functional Annotation of p53 Protein
# ====================================

# Protein Name:
# Cellular tumor antigen p53

# Organism:
# Homo sapiens (Human)

# UniProt Accession:
# P04637

# Predicted Function:
# p53 is a tumor suppressor protein involved in the regulation
# of the cell cycle, DNA repair, apoptosis, and genomic stability.

# Biological Role:
# The protein helps prevent uncontrolled cell division and
# plays a critical role in protecting cells from cancer development.

# Homology-Based Evidence:
# BLAST analysis showed strong similarity with p53 proteins
# from multiple mammalian species, indicating evolutionary conservation.

# Conserved Features:
# The protein contains conserved DNA-binding regions important
# for transcription regulation and tumor suppression.

# Organism Relevance:
# In humans, p53 is one of the most important proteins involved
# in cancer prevention and cellular stress response.
# """

# # Save annotation
# with open("../results/functional_annotation.txt", "w") as output_file:
#     output_file.write(annotation)

# print("Functional annotation saved in functional_annotation.txt")