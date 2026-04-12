# Architecture Overview

This document summarizes the Task Tracker CLI architecture for quick onboarding and review. It aligns with the approved design and the current code in `task_tracker/`.

## Components
- CLI (`task_tracker/cli.py`): parses commands, validates args, maps requests to the service, formats user output.
- Service (`task_tracker/service.py`): business rules and state transitions (id generation, validation, invariants).
- Repository (`task_tracker/repo.py`): JSON persistence, storage-path handling, initialization.
- Domain (`task_tracker/domain.py`): task record model and helpers.

## Data Model
Task fields:
- `id: int` ¡ª stable, unique, 1..N
- `description: str`
- `completed: bool`
- `created_at: ISO8601 str`
- `completed_at: Optional[ISO8601 str]`

## Storage
- Local JSON file (default per test usage: `.tasks.json` within the working directory or a provided path).
- Full-document reads/writes; writes replace the full file to reduce corruption risk.

## Command Flows
- `add <desc>`: CLI -> Service.add -> Repo.save -> prints new id
- `list`: CLI -> Service.list -> Repo.load -> prints tasks in creation order
- `complete <id>`: CLI validates id -> Service.complete (rejects invalid/duplicate) -> Repo.save -> prints updated task
- `delete <id>`: CLI validates id -> Service.delete (rejects invalid) -> Repo.save -> prints removed task

## Validation & Errors
- Clear user-facing errors for: unknown command, missing arg, malformed id, id not found, completing an already-completed task.
- Normal user mistakes do not print stack traces.

## Module Boundaries
- CLI: I/O and UX only; no persistence logic.
- Service: business rules; no disk I/O.
- Repository: persistence; no UX.
- Domain: pure data structures and conversions.

## Testing Strategy
- Unit tests cover add/list/complete/delete and id validation (`python -m unittest -v`).
- Temp directories ensure persistence behavior is validated without polluting the workspace.

## CI
- GitHub Actions runs unit tests on PRs to `main` and pushes to `main` (see `.github/workflows/ci.yml`).

## Future Extensions (non-binding)
- Optional: configurable storage path via env/flag.
- Optional: richer list formatting and filters.
- Optional: atomic file write helper.
