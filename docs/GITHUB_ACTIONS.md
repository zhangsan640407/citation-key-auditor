# GitHub Actions Usage

Citation Key Auditor can run as a quality gate in a manuscript repository. This
is useful when a paper, report, thesis chapter, or Quarto project is edited by
more than one person.

The project is not published to PyPI yet, so install it from a GitHub release
tag.

## Minimal workflow

Create `.github/workflows/citation-keys.yml` in the manuscript repository:

```yaml
name: Citation keys

on:
  pull_request:
  push:
    branches: [main]

jobs:
  citation-keys:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --upgrade pip
      - run: python -m pip install "git+https://github.com/zhangsan640407/citation-key-auditor.git@v0.3.0"
      - run: citation-key-audit check manuscript.md references.bib
```

The final step returns a non-zero exit code when cited keys are missing from the
BibTeX file, so the GitHub Actions job fails. Missing-key diagnostics include
the manuscript line numbers where the keys were cited.

Pass each manuscript file before the BibTeX file. Multi-file diagnostics include
both file names and line numbers:

```yaml
- run: citation-key-audit check intro.md methods.md results.md references.bib
```

Starting with `v0.3.0`, repeat `--bibtex` to merge references from multiple
BibTeX files:

```yaml
- run: >-
    citation-key-audit check intro.md methods.md results.md
    --bibtex primary.bib
    --bibtex software.bib
```

Duplicate keys across BibTeX files are reported with their source file names.
They are warnings and do not fail the job.

## Quarto example

For a Quarto manuscript, pass the `.qmd` file explicitly:

```yaml
- run: citation-key-audit check paper.qmd references.bib
```

For a split Quarto project, pass each checked source file before the BibTeX file:

```yaml
- run: citation-key-audit check index.qmd methods.qmd results.qmd references.bib
```

The tool reads citation syntax from the `.qmd` source file. It does not render
the Quarto project or read the `bibliography` field from YAML yet.

## JSON output

Text output is usually enough for CI logs. Use `--json` when another script
needs to consume the result:

```yaml
- run: citation-key-audit check manuscript.md references.bib --json
```

The command still fails when missing keys are found.

## Optional unused-reference gate

By default, unused BibTeX entries are reported but do not fail CI. To make unused
entries fail the job, add `--fail-on-unused`:

```yaml
- run: citation-key-audit check manuscript.md references.bib --fail-on-unused
```

Use this stricter mode only when the repository expects every BibTeX entry to be
cited by the checked manuscript.

## Current limitations

- Pass manuscript paths and the BibTeX path explicitly.
- Quarto bibliography paths are not read automatically from YAML metadata.

These limitations are tracked in open issues and should improve in later
releases.
