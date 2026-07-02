import unittest

from citation_key_auditor.core import (
    audit_citations,
    audit_manuscripts,
    audit_project,
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

    def test_reports_sources_for_multiple_manuscripts(self):
        manuscripts = {
            "intro.md": "Known claim [@smith2024].\nMissing claim [@missing2025].",
            "results.md": r"Repeated missing claim \cite{missing2025}.",
        }
        bibtex = """
        @article{smith2024,
          title = {Known paper}
        }
        """

        result = audit_manuscripts(manuscripts, bibtex)

        self.assertEqual(result.missing_keys, {"missing2025"})
        self.assertEqual(
            [
                (source.path, source.line)
                for source in result.citation_sources["missing2025"]
            ],
            [("intro.md", 2), ("results.md", 1)],
        )

    def test_merges_multiple_bibtex_files_and_reports_duplicates(self):
        manuscripts = {
            "paper.qmd": "First [@primary2024]. Second [@software2023]."
        }
        bibtex_files = {
            "primary.bib": (
                "@article{primary2024,title={Primary}}\n"
                "@article{shared2022,title={Shared primary}}"
            ),
            "software.bib": (
                "@software{software2023,title={Software}}\n"
                "@article{shared2022,title={Shared software}}"
            ),
        }

        result = audit_project(manuscripts, bibtex_files)

        self.assertEqual(result.missing_keys, set())
        self.assertEqual(result.bibtex_keys, {"primary2024", "software2023", "shared2022"})
        self.assertEqual(result.duplicate_bibtex_keys, {"shared2022"})
        self.assertEqual(
            result.bibtex_sources["shared2022"],
            ("primary.bib", "software.bib"),
        )


if __name__ == "__main__":
    unittest.main()
