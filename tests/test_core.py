import unittest

from citation_key_auditor.core import (
    audit_citations,
    extract_bibtex_keys,
    extract_citation_keys,
    extract_citation_locations,
)


class CitationExtractionTests(unittest.TestCase):
    def test_extracts_pandoc_markdown_keys(self):
        text = "Prior work shows this [@smith2024; @lee-2023, pp. 10-12]."

        self.assertEqual(extract_citation_keys(text), {"smith2024", "lee-2023"})

    def test_extracts_latex_cite_keys(self):
        text = r"These results follow \citep[see][12]{smith2024, lee2023}."

        self.assertEqual(extract_citation_keys(text), {"smith2024", "lee2023"})

    def test_extracts_markdown_key_locations(self):
        text = "\n".join(
            [
                "Opening paragraph.",
                "Prior work shows this [@smith2024; @lee-2023].",
                "The same source appears again [@smith2024].",
            ]
        )

        self.assertEqual(
            extract_citation_locations(text),
            {"lee-2023": (2,), "smith2024": (2, 3)},
        )

    def test_extracts_latex_key_locations(self):
        text = "\n".join(
            [
                r"These results follow \citep[see][12]{smith2024, lee2023}.",
                "A plain sentence.",
                r"A second command uses \cite{smith2024}.",
            ]
        )

        self.assertEqual(
            extract_citation_locations(text),
            {"lee2023": (1,), "smith2024": (1, 3)},
        )

    def test_extracts_bibtex_keys(self):
        bibtex = """
        @article{smith2024,
          title = {A paper}
        }
        @inproceedings(lee2023,
          title = {A conference paper}
        )
        """

        self.assertEqual(extract_bibtex_keys(bibtex), {"smith2024", "lee2023"})


class AuditTests(unittest.TestCase):
    def test_reports_missing_and_unused_keys(self):
        manuscript = "Known claim [@smith2024; @missing2025]."
        bibtex = """
        @article{smith2024,
          title = {Known paper}
        }
        @article{unused2022,
          title = {Unused paper}
        }
        """

        result = audit_citations(manuscript, bibtex)

        self.assertEqual(result.missing_keys, {"missing2025"})
        self.assertEqual(result.unused_keys, {"unused2022"})
        self.assertEqual(result.citation_locations["missing2025"], (1,))


if __name__ == "__main__":
    unittest.main()
