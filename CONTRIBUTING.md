# Contributing

Thanks for considering a contribution.

## Useful contributions

- Add citation syntax examples from real Markdown, LaTeX, or Quarto projects.
- Improve BibTeX parsing around edge cases.
- Add tests for citation commands used by specific journals or templates.
- Improve documentation for CI integration.
- Report false positives or false negatives with a minimal example.

## Development setup

```powershell
python -m pip install -e .
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests
```

## Pull request checklist

- Add or update tests for behavior changes.
- Keep runtime dependencies at zero unless there is a strong reason.
- Update README or docs when user-facing behavior changes.
- Keep changes focused on one problem.

## Maintainer notes

The project should stay small, predictable, and easy to run in CI. Larger
features should start as issues so users can discuss the expected behavior.
