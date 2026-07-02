# Validation Record

This page records privacy-preserving checks performed with real academic data.
It does not publish manuscript text, reference titles, citation keys, or local
file paths.

## 2026-07-02: thesis Markdown and Zotero BibTeX

Citation Key Auditor was run against a temporary, private copy of a real thesis
Markdown draft. A short validation citation block was added to the temporary
copy using keys from three real journal records in the maintainer's local
Zotero library. Each record was exported to a separate BibTeX file to exercise
the multi-BibTeX command.

Command shape:

```powershell
citation-key-audit check private-thesis-copy.md `
  --bibtex project-paper.bib `
  --bibtex background-paper.bib `
  --bibtex recent-paper.bib `
  --json
```

Anonymized result:

| Metric | Result |
| --- | ---: |
| Manuscript files | 1 |
| BibTeX files | 3 |
| Cited keys | 3 |
| BibTeX keys | 3 |
| Missing keys | 0 |
| Unused keys | 0 |
| Duplicate BibTeX keys | 0 |
| Exit code | 0 |

The source files and complete JSON output remained local. This small validation
confirmed the expected success path for real UTF-8 academic text and multiple
BibTeX exports. It does not claim broad parser coverage or external adoption.
