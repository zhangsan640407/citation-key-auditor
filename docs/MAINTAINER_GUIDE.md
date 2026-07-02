# Maintainer Guide

This project is intended to be maintained in the open.

## Release routine

1. Review open issues tagged `bug`.
2. Run the full test suite.
3. Update `CHANGELOG.md`.
4. Bump the version in `pyproject.toml` and `src/citation_key_auditor/__init__.py`.
5. Create a GitHub release with a concise changelog.

## Issue triage

Useful issue labels:

- `bug`
- `citation-syntax`
- `bibtex`
- `documentation`
- `good first issue`
- `help wanted`

## Project principles

- Prefer deterministic local checks over network-backed behavior.
- Keep the CLI stable and easy to automate.
- Add tests for each citation syntax before expanding support.
- Keep documentation honest about what is and is not parsed.
