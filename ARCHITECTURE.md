# Architecture Overview

This document summarizes the Task Tracker CLI architecture for quick onboarding and review. It aligns with the approved design and current code in 	ask_tracker/.

## Components
- CLI (	ask_tracker/cli.py): parses commands, validates args, maps requests to service, formats user output.
- Service (	ask_tracker/service.py): business rules and state transitions (id generation, validation, invariants).
- Repository (	ask_tracker/repo.py): JSON persistence, storage-path handling, initialization.
- Domain (	ask_tracker/domain.py): task record model and helpers.

## Data Model
Task fields:
- id: int ¡ª stable, unique, 1..N
- description: str
- completed: bool
- created_at: ISO8601 str
- completed_at: Optional[ISO8601 str]

## Storage
- Local JSON file (default per test usage: .tasks.json within working directory or provided path).
- Full-document reads/writes; writes are replace-in-full to reduce corruption risk.

## Command Flows
- dd <desc>: CLI ¡ú Service.add ¡ú Repo.save ¡ú prints new id
- list: CLI ¡ú Service.list ¡ú Repo.load ¡ú prints tasks grouped by state
- complete <id>: CLI validates id ¡ú Service.complete (rejects invalid/duplicate) ¡ú Repo.save ¡ú prints updated task
- delete <id>: CLI validates id ¡ú Service.delete (rejects invalid) ¡ú Repo.save ¡ú prints removed task

## Validation & Errors
- Clear user-facing errors for: unknown command, missing arg, malformed id, id not found, completing already-completed task.
- Normal user mistakes do not print stack traces.

## Module Boundaries
- CLI: I/O and UX only; no persistence logic.
- Service: business rules; no disk I/O.
- Repository: persistence; no UX.
- Domain: pure data structures and conversions.

## Testing Strategy
- Unit tests cover add/list/complete/delete and id validation (python -m unittest -v).
- Temp directories ensure persistence behavior is validated without polluting workspace.

## CI
- GitHub Actions runs unit tests on PRs and pushes to main (see .github/workflows/ci.yml).

## Future Extensions (Non-binding)
- Optional: configurable storage path via env/flag.
- Optional: richer list formatting and filters.
- Optional: atomic file write helper.

