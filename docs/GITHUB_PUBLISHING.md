# GitHub Publishing

This machine has `git`, but the GitHub CLI was not available when this project
was created. Use the GitHub website or install `gh` before publishing.

## Option A: GitHub website

1. Create a new public repository named `citation-key-auditor`.
2. Do not initialize it with a README, license, or `.gitignore`.
3. From this local repository, run:

```powershell
git remote add origin https://github.com/zhangsan640407/citation-key-auditor.git
git push -u origin main
```

4. Confirm the project URLs in `pyproject.toml` match the remote repository.

## Option B: GitHub CLI

If `gh` is installed and authenticated:

```powershell
gh repo create citation-key-auditor --public --source . --remote origin --push
```

Then verify:

```powershell
git remote -v
git status
```

## First GitHub tasks

- Enable Issues.
- Confirm the CI workflow runs on the first push.
- Create starter issues from `docs/OPEN_SOURCE_MAINTAINER_PLAN.md`.
- Add repository topics such as `bibtex`, `citations`, `markdown`, `latex`,
  `research-tools`, and `python`.
- Create the first release after CI passes.
