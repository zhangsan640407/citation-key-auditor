# Open Source Maintainer Plan

This document describes how to grow Citation Key Auditor as a legitimate
open-source project. It is not a shortcut to any grant, credit, or subscription
program. Claims about maintainership, usage, downloads, stars, or users should
only describe evidence that really exists.

## First public release

- Publish the repository publicly on GitHub.
- Keep the MIT license, README, contribution guide, security policy, tests, and
  GitHub Actions workflow visible.
- Create a `v0.1.0` release after CI passes.
- Open a small set of real starter issues:
  - add line-number reporting
  - support multiple manuscript files
  - support multiple BibTeX files
  - add Quarto examples
  - document GitHub Actions usage

## First month

- Use the tool on real Markdown or LaTeX manuscripts.
- Record false positives and false negatives as public issues.
- Add tests before changing parser behavior.
- Invite a few researchers or template maintainers to try it.
- Reply to issues with reproducible examples and concrete decisions.

## Evidence worth tracking

- merged pull requests
- closed issues with tests
- releases and changelog entries
- external projects or templates that use the tool
- package downloads, if it is later published
- user reports with reproducible citation examples

## What not to do

- Do not invent users, stars, downloads, or institutional adoption.
- Do not create fake issues or fake pull requests.
- Do not claim to be the maintainer of a project you do not maintain.
- Do not apply to programs with placeholder links or unverified impact claims.

## Honest application positioning

If this project later has real users and maintenance activity, describe it as:

> Citation Key Auditor is a small open-source CLI that helps researchers catch
> missing and unused BibTeX citation keys in Markdown and LaTeX manuscripts. I
> maintain the project, review user-reported citation syntax edge cases, add
> parser tests, and keep CI passing across supported Python versions.
