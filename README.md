# Citation Key Auditor

Citation Key Auditor is a small command-line tool that checks whether citation
keys used in Markdown or LaTeX manuscripts exist in a BibTeX file.

It is designed for researchers, graduate students, maintainers of academic
templates, and documentation teams that want a fast pre-submit check before a
paper, thesis chapter, or technical report is shared.

## Why this exists

Citation mistakes are easy to miss during manuscript editing:

- a cited key is absent from `references.bib`
- a reference is present in the BibTeX file but never cited
- a key is renamed in one file but not the other

This tool catches those mismatches early and returns a clear exit code for CI.

## Features

- Detects Pandoc-style Markdown citations such as `[@smith2024]`.
- Detects grouped Markdown citations such as `[@smith2024; @lee2023]`.
- Detects common LaTeX citation commands such as `\cite{smith2024}`.
- Reads BibTeX keys from `.bib` files.
- Reports missing and unused citation keys.
- Supports text and JSON output.
- Has no runtime dependencies.

## Install

From a local checkout:

```powershell
python -m pip install -e .
```

## Usage

Check a manuscript against a BibTeX file:

```powershell
citation-key-audit check manuscript.md references.bib
```

Try the included example:

```powershell
citation-key-audit check examples\manuscript.md examples\references.bib
```

Check a Quarto manuscript in the same way:

```powershell
citation-key-audit check examples\quarto-paper.qmd examples\references.bib
```

For Quarto-specific notes, see [docs/QUARTO.md](docs/QUARTO.md).

Return JSON:

```powershell
citation-key-audit check manuscript.md references.bib --json
```

Fail the command when unused BibTeX entries are found:

```powershell
citation-key-audit check manuscript.md references.bib --fail-on-unused
```

## Example

```markdown
Recent work has improved thermal-process monitoring [@wang2024; @lee2023].
```

```bibtex
@article{wang2024,
  title = {Example paper},
  author = {Wang, A.},
  year = {2024}
}
```

The auditor reports `lee2023` as missing.

## Development

Run the test suite:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests
```

## Project status

This repository is intentionally small and practical. The first public milestone
is a stable citation-key checker for Markdown and LaTeX workflows. See
[ROADMAP.md](ROADMAP.md) for planned work.

For a realistic open-source maintenance plan, see
[docs/OPEN_SOURCE_MAINTAINER_PLAN.md](docs/OPEN_SOURCE_MAINTAINER_PLAN.md).

## License

MIT. See [LICENSE](LICENSE).
