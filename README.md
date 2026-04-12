# Personal Task Tracker (v1)

A small, local-only CLI for managing a simple personal task list from the terminal.

- Single-user, runs entirely on your machine
- JSON file persistence in the current working directory
- Commands: add, list, complete, delete

## Prerequisites
- Python 3.9+ installed and on PATH
- Windows, macOS, or Linux terminal

## Setup
Clone the repository:
```sh
git clone https://github.com/ktlichkid/test_repo.git
cd test_repo
```
(Optional) Create a virtual environment:
```sh
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux bash
source .venv/bin/activate
```

## Usage
Run the CLI via Python:
```sh
python task.py add "Buy milk"
python task.py list
python task.py complete 1
python task.py delete 1
```
Notes:
- Data is stored in `.tasks.json` in the current working directory
- Status markers in `list`: `[ ]` pending, `[x]` completed
- Invalid or nonexistent IDs return a clear error without crashing

## Running Tests
```sh
python -m unittest discover -s tests -p "test*.py" -v
```

## Scope
This v1 is intentionally minimal and local-only. For detailed setup and dependency notes, see `docs/setup.md`.
