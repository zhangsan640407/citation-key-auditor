# Quarto Usage

Quarto manuscripts use Pandoc-style citations, so Citation Key Auditor can check
the citation keys in a `.qmd` file as plain text.

## Minimal workflow

Install the project from a local checkout:

```powershell
python -m pip install -e .
```

Check a Quarto manuscript against a BibTeX file:

```powershell
citation-key-audit check paper.qmd references.bib
```

Run the included example:

```powershell
citation-key-audit check examples\quarto-paper.qmd examples\references.bib
```

## Example Quarto manuscript

A Quarto file can declare the bibliography in YAML:

```yaml
---
title: "Example Quarto manuscript"
format: html
bibliography: references.bib
---
```

The body can then use Pandoc-style citations:

```markdown
Research-writing workflows benefit from local reference checks [@smith2024].
Grouped citations are also supported [@lee2023; @garcia2022].
```

Citation Key Auditor reads the `.qmd` file and reports whether `smith2024`,
`lee2023`, and `garcia2022` exist in the BibTeX file passed to the command.

## Current limitations

- The tool does not render Quarto documents.
- The tool does not automatically read the `bibliography` field from YAML.
- Pass the `.qmd` file and `.bib` file explicitly.
- Multi-file manuscript projects are not supported yet.
- Multiple BibTeX files are not supported yet.
- Diagnostics do not include line numbers yet.

These limitations are tracked in open issues so they can be improved without
changing the current command behavior unexpectedly.
