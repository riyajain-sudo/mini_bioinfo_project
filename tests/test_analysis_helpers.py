import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from analysis.sequence_analysis import load_validated_fasta
from analysis.homology_analysis import comparative_hits
from analysis.functional_annotation import render_report

class ProteinValidationTests(unittest.TestCase):
    def test_real_fasta(self):
        rec, seq = load_validated_fasta()
        self.assertEqual(len(seq), 393)
        self.assertEqual(sum(__import__('collections').Counter(seq).values()), len(seq))
    def test_rejects_ambiguous_and_multiple_records_before_metrics(self):
        for content, message in ((">p\n" + "A"*99 + "X", "Unsupported residue"), (">p\n"+"A"*100+"\n>second\n"+"A"*100, "exactly one")):
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/"x.fa"; p.write_text(content)
                with self.assertRaisesRegex(ValueError, message): load_validated_fasta(p)
    def test_filters_self_duplicates_and_calculates_identity_coverage(self):
        def hit(acc,title,identity,alen=100,start=1,end=100):
            return SimpleNamespace(accession=acc,title=title,hsps=[SimpleNamespace(identities=identity,align_length=alen,query_start=start,query_end=end,expect=1e-20,score=80)])
        record=SimpleNamespace(query_length=200,alignments=[hit("P04637","self",100,100,1,100),hit("same","exact full",200,200,1,200),hit("X1","species 1",50,100,1,100),hit("X1","duplicate",40),hit("X2","species 2",60,100,51,150)])
        rows=comparative_hits(record)
        self.assertEqual([r["accession"] for r in rows],["X1","X2"]); self.assertAlmostEqual(rows[0]["identity"],.5); self.assertAlmostEqual(rows[0]["query_coverage"],.5)
    def test_annotation_identifies_direct_curated_source(self):
        report=render_report({"proteinDescription":{"recommendedName":{"fullName":{"value":"p53"}}},"organism":{"scientificName":"Homo sapiens"},"genes":[{"geneName":{"value":"TP53"}}],"comments":[{"commentType":"FUNCTION","texts":[{"value":"Function text"}]}]},"2026-01-01T00:00:00+00:00")
        self.assertIn("not homology inference",report); self.assertIn("Function text",report)

if __name__ == "__main__": unittest.main()
