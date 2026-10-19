"""Retrieve a direct UniProt-curated record, not homology-derived annotation."""
from datetime import datetime, timezone
from pathlib import Path
import os
import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results/functional_annotation.txt"
ACCESSION = "P04637"
URL = f"https://rest.uniprot.org/uniprotkb/{ACCESSION}.json"

def render_report(data, retrieved_at):
    if not isinstance(data, dict) or not isinstance(data.get("proteinDescription"), dict) or not isinstance(data.get("organism"), dict):
        raise ValueError("UniProt response is missing required protein/organism fields")
    names = data["proteinDescription"].get("recommendedName", {}).get("fullName", {})
    name = names.get("value") if isinstance(names, dict) else None
    organism = data["organism"].get("scientificName")
    genes = data.get("genes", [])
    gene = next((entry.get("geneName", {}).get("value") for entry in genes if isinstance(entry, dict) and isinstance(entry.get("geneName"), dict)), None)
    if not name or not organism or not gene:
        raise ValueError("UniProt response lacks recommended name, organism, or gene name")
    function = None
    for comment in data.get("comments", []):
        if isinstance(comment, dict) and comment.get("commentType") == "FUNCTION":
            texts = comment.get("texts", [])
            if texts and isinstance(texts[0], dict): function = texts[0].get("value")
            if function: break
    if not function: function = "No FUNCTION comment was supplied in this response."
    return ("UniProt-curated functional annotation (direct record; not homology inference)\n"
            f"Accession: {ACCESSION}\nProtein: {name}\nGene: {gene}\nOrganism: {organism}\n"
            f"Source: {URL}\nRetrieved UTC: {retrieved_at}\n\nFunction comment:\n{function}\n")

def main():
    try:
        response = requests.get(URL, timeout=(5, 20), headers={"Accept":"application/json"})
        response.raise_for_status()
        data = response.json()
        report = render_report(data, datetime.now(timezone.utc).isoformat())
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        temp = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
        temp.write_text(report, encoding="utf-8")
        os.replace(temp, OUTPUT)
    except (requests.RequestException, ValueError, OSError) as exc:
        raise SystemExit(f"UniProt annotation failed; existing report was not replaced: {exc}") from exc
    print(f"UniProt-curated annotation saved to {OUTPUT}")

if __name__ == "__main__": main()
