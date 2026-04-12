# Setup and Dependencies

This project is a local-only CLI written in Python. v1 uses only Python standard library modules ¡ª there are no third-party runtime dependencies.

## Prerequisites
- Python 3.9+ installed and available on PATH
- Windows, macOS, or Linux terminal

## Local Setup
1. Clone the repository
`sh
git clone https://github.com/ktlichkid/test_repo.git
cd test_repo
`
2. (Optional) Create a virtual environment (no packages are required; this just isolates tooling)
`sh
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux bash
source .venv/bin/activate
`
3. Verify Python version
`sh
python -V
`

## Running the CLI
Run via Python:
`sh
python task.py add "Buy milk"
python task.py list
python task.py complete 1
python task.py delete 1
`
Notes:
- Data persists to .tasks.json in the current working directory
- Status markers in list: [ ] pending, [x] completed

## Running Tests
Uses Python's built-in unittest:
`sh
python -m unittest discover -s tests -p "test*.py" -v
`

## Modules Used (stdlib)
- argparse, json, pathlib, datetime, dataclasses, typing, unittest, tempfile, shutil, io, os, contextlib

## Notes
- If your Windows console shows garbled non-ASCII text, enable UTF-8 mode or use a UTF-8 compatible font. JSON persistence is UTF-8 and not affected.
- Packaging and a dedicated 	ask entrypoint may be added in a future ticket.
