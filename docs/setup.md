# Setup and Dependencies

This project is a local-only CLI written in Python. v1 uses only Python standard library modules ¡ª there are no third?party runtime dependencies.

## Prerequisites
- Python 3.9+ installed and available on PATH
- Windows, macOS, or Linux terminal

## Local Setup
1. Clone the repository
   `sh
   git clone https://github.com/ktlichkid/test_repo.git
   cd test_repo
   `
2. (Optional) Create a virtual environment ¡ª no packages are required, but this keeps tooling isolated.
   `sh
   python -m venv .venv
   # activate: Windows PowerShell
   .venv\\Scripts\\Activate.ps1
   # activate: macOS/Linux bash
   source .venv/bin/activate
   `
3. Verify Python version
   `sh
   python -V
   `

## Running the CLI
The CLI entry is a Python module. For now, invoke via:
`sh
python task.py list
python task.py add "Buy milk"
`
Notes:
- Data persists to .tasks.json in the current working directory
- Commands available in v1: dd, list, complete, delete

## Running Tests
The test suite uses Python¡¯s built-in unittest.
`sh
python -m unittest discover -s tests -p "test*.py" -v
`

## Modules Used (stdlib)
- rgparse, json, pathlib, datetime, dataclasses, 	yping, unittest, 	empfile, shutil, io, os, contextlib

## Notes
- If your terminal on Windows shows garbled non?ASCII characters, enable UTF?8 mode or a UTF?8 compatible font. This does not affect JSON persistence, which is UTF?8.
- Packaging/installer and a dedicated 	ask entrypoint may be added in a future ticket.
