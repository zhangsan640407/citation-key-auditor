import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from citation_key_auditor.cli import main


class CliTests(unittest.TestCase):
    def test_check_returns_success_when_all_citations_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manuscript = tmp_path / "paper.md"
            bibtex = tmp_path / "references.bib"
            manuscript.write_text("A supported claim [@smith2024].", encoding="utf-8")
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = main(["check", str(manuscript), str(bibtex)])

            self.assertEqual(exit_code, 0)

    def test_check_returns_failure_for_missing_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manuscript = tmp_path / "paper.md"
            bibtex = tmp_path / "references.bib"
            manuscript.write_text(
                "A supported claim [@smith2024].\n"
                "A missing claim [@missing2024].\n",
                encoding="utf-8",
            )
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(["check", str(manuscript), str(bibtex)])

            self.assertEqual(exit_code, 1)
            self.assertIn("- missing2024 (line 2)", stdout.getvalue())

    def test_json_output_is_machine_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manuscript = tmp_path / "paper.md"
            bibtex = tmp_path / "references.bib"
            manuscript.write_text("A supported claim [@smith2024].", encoding="utf-8")
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(["check", str(manuscript), str(bibtex), "--json"])

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["missing_keys"], [])
            self.assertEqual(payload["citation_locations"], {"smith2024": [1]})
            self.assertEqual(payload["missing_key_locations"], {})
            self.assertEqual(
                payload["citation_sources"],
                {"smith2024": [{"file": str(manuscript), "line": 1}]},
            )
            self.assertEqual(payload["missing_key_sources"], {})

    def test_json_output_includes_missing_key_locations(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manuscript = tmp_path / "paper.md"
            bibtex = tmp_path / "references.bib"
            manuscript.write_text(
                "First paragraph [@missing2024].\n"
                "Second paragraph.\n"
                "Another citation [@missing2024].\n",
                encoding="utf-8",
            )
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(["check", str(manuscript), str(bibtex), "--json"])

            self.assertEqual(exit_code, 1)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["missing_keys"], ["missing2024"])
            self.assertEqual(payload["missing_key_locations"], {"missing2024": [1, 3]})
            self.assertEqual(
                payload["missing_key_sources"],
                {
                    "missing2024": [
                        {"file": str(manuscript), "line": 1},
                        {"file": str(manuscript), "line": 3},
                    ]
                },
            )

    def test_check_accepts_multiple_manuscript_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            intro = tmp_path / "intro.md"
            results = tmp_path / "results.md"
            bibtex = tmp_path / "references.bib"
            intro.write_text(
                "A supported claim [@smith2024].\n"
                "A missing claim [@missing2024].\n",
                encoding="utf-8",
            )
            results.write_text(
                "A LaTeX missing claim " + r"\cite{missing2024}." + "\n",
                encoding="utf-8",
            )
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(["check", str(intro), str(results), str(bibtex)])

            self.assertEqual(exit_code, 1)
            output = stdout.getvalue()
            self.assertIn("Missing keys: 1", output)
            self.assertIn("missing2024", output)
            self.assertIn(f"{intro}:2", output)
            self.assertIn(f"{results}:1", output)

    def test_json_output_includes_multiple_manuscript_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            intro = tmp_path / "intro.md"
            results = tmp_path / "results.md"
            bibtex = tmp_path / "references.bib"
            intro.write_text("A missing claim [@missing2024].\n", encoding="utf-8")
            results.write_text(
                "A supported claim [@smith2024].\n"
                "Another missing claim [@missing2024].\n",
                encoding="utf-8",
            )
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(
                    ["check", str(intro), str(results), str(bibtex), "--json"]
                )

            self.assertEqual(exit_code, 1)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["missing_keys"], ["missing2024"])
            self.assertEqual(
                payload["missing_key_sources"],
                {
                    "missing2024": [
                        {"file": str(intro), "line": 1},
                        {"file": str(results), "line": 2},
                    ]
                },
            )


if __name__ == "__main__":
    unittest.main()
