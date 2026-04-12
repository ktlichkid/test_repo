# Continuous Integration (CI)

This repository uses GitHub Actions to run the Python unit test suite on:
- pull requests to `main`
- direct pushes to `main`

Workflow file: `.github/workflows/ci.yml`

What runs
- Environment: `ubuntu-latest` with Python 3.11
- Command: `python -m unittest discover -s tests -p "test*.py" -v`

Purpose
- Provide fast feedback that the current v1 CLI passes the existing tests before merge and on changes to `main`.

Scope
- Minimal CI only; no release automation or deployment in this workflow.
