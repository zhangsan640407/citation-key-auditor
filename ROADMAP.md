# Roadmap

## 0.1

- Extract citation keys from Pandoc Markdown.
- Extract citation keys from common LaTeX commands.
- Compare cited keys with BibTeX entries.
- Provide text and JSON CLI output.
- Add CI and baseline tests.

## 0.2

- Support Quarto examples in documentation.
- Add better diagnostics with citation line numbers.
- Add `--ignore-unused` and config-file support.
- Add more tests for natbib and biblatex commands.

## 0.3

- Support multiple manuscript files.
- Support multiple BibTeX files.

## 0.4

- Add `--ignore-unused` and config-file support.
- Add more tests for natbib and biblatex commands.
- Publish package metadata for PyPI.

## Open questions

- Whether CSL JSON should be supported directly.
- Whether unused-key checks should default to warnings forever.
- Whether future file-aware diagnostics should use a parser or a lightweight scanner.
