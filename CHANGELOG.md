# Changelog

## Unreleased

- Added support for checking multiple manuscript files in one command.
- Added file-aware citation source metadata for JSON output.
- Added file-aware missing-key diagnostics for multi-file text output.

## 0.2.0

- Added Quarto usage documentation and a runnable `.qmd` example.
- Added GitHub Actions documentation for using the tool in manuscript repositories.
- Added citation line-number diagnostics for Markdown and LaTeX citations.
- Added JSON metadata fields for `citation_locations` and `missing_key_locations`.
- Updated tests for Markdown, LaTeX, text output, and JSON output.

## 0.1.0

- Initial CLI for auditing citation keys.
- Markdown, LaTeX, and BibTeX key extraction.
- Text and JSON output.
- Unit tests and GitHub Actions workflow.
