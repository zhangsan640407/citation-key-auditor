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
            manuscript.write_text("A missing claim [@missing2024].", encoding="utf-8")
            bibtex.write_text("@article{smith2024,title={Paper}}", encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = main(["check", str(manuscript), str(bibtex)])

            self.assertEqual(exit_code, 1)

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


if __name__ == "__main__":
    unittest.main()
