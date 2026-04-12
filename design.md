# Design Document: Personal Task Tracker v1

## 1. Objective

Deliver a small, local-only command-line task tracker for a single user that supports:
- adding a task
- listing tasks
- marking a task as completed
- deleting a task
- persisting tasks between runs

The design intentionally keeps v1 minimal and avoids broader productivity features.

## 2. Engineering Interpretation Of Requirements

This version will be implemented as a local CLI application with a file-backed data store.

The product behavior is defined as follows:
- The application runs entirely on a local machine.
- A task contains:
  - `id`: integer identifier unique within the current task list
  - `description`: short user-provided text
  - `completed`: boolean state
  - `created_at`: timestamp for stable ordering and auditability
  - `completed_at`: optional timestamp set when a task is completed
- Tasks are shown in creation order.
- Completed tasks remain visible by default so the user can distinguish pending from completed items.
- Duplicate task descriptions are allowed. Task identity is based on `id`, not description text.
- Delete does not require confirmation in v1 to preserve a fast CLI workflow.

These choices resolve the requirement document's open questions into explicit behavior and should be confirmed before implementation begins.

## 3. Scope

### In Scope
- Local CLI entry point
- Add command for creating a task
- List command for showing tasks
- Complete command for marking a task completed
- Delete command for removing a task
- Persistent local storage across runs
- Clear empty-state messaging
- Clear invalid-id error handling

### Out Of Scope
- Multi-user behavior
- Authentication, network, sync, or remote storage
- Tags, priorities, subtasks, reminders, recurring tasks
- GUI, web, or mobile interface
- Search, filtering, sorting beyond creation order
- Bulk operations
- Undo or delete confirmation flow

## 4. Proposed User Interface

### Commands
- `task add "<description>"`
- `task list`
- `task complete <id>`
- `task delete <id>`

### Command Behavior

#### Add
Input:
- required description string

Output:
- success message including the new task id

Failure cases:
- empty or whitespace-only description

#### List
Output:
- ordered list of all tasks
- each row includes id, status marker, and description
- if no tasks exist, print a clear empty-state message

Status markers:
- `[ ]` pending
- `[x]` completed

#### Complete
Input:
- required integer task id

Output:
- success message identifying the completed task

Failure cases:
- id does not exist
- id is malformed
- task is already completed

#### Delete
Input:
- required integer task id

Output:
- success message identifying the deleted task

Failure cases:
- id does not exist
- id is malformed

## 5. Storage Design

### Storage Mechanism
- Use a single local JSON file for persistence.
- Default storage path should live in the current working directory or another explicitly defined local path chosen during implementation.

### File Format
```json
{
  "next_id": 4,
  "tasks": [
    {
      "id": 1,
      "description": "Buy milk",
      "completed": false,
      "created_at": "2026-04-12T03:00:00Z",
      "completed_at": null
    }
  ]
}
```

### Storage Rules
- `next_id` guarantees stable unique ids even after deletions.
- Reads and writes operate on the full document because v1 data volume is small.
- If the storage file does not exist, the app initializes an empty task store.
- Writes should replace the full file atomically where practical to reduce corruption risk.

## 6. Logical Components

The implementation should be separated into small components with clear responsibilities:

### CLI Layer
- Parses commands and arguments
- Validates command shape
- Maps user requests to task operations
- Formats user-facing output

### Service Layer
- Applies task business rules
- Generates ids
- Prevents invalid state transitions

### Repository Layer
- Loads task data from disk
- Saves task data back to disk
- Owns storage-path handling and initialization

### Domain Model
- Defines task record structure and related state transitions

This separation keeps future changes reviewable and testable without introducing unnecessary complexity.

## 7. Error Handling

The application should fail clearly, not silently.

Expected user-facing errors:
- unknown command
- missing required argument
- invalid task id format
- task id not found
- completing an already completed task
- storage read/write failure

Error messages should:
- state what failed
- identify the relevant id when applicable
- avoid stack traces for normal user mistakes

## 8. Validation Strategy

Implementation should be validated with focused checks that map directly to the requirements.

### Minimum Automated Coverage
- add persists a new task
- list shows pending and completed states correctly
- complete updates a pending task and rejects invalid ids
- delete removes the correct task and rejects invalid ids
- empty-state output is clear
- data survives process restart

### Manual Verification
- CLI commands match documented usage
- output remains readable with multiple tasks
- storage file initializes correctly from empty state

## 9. Risks And Constraints

### Risks
- Ambiguity about storage location can create surprising behavior
- Non-atomic writes could risk data loss if interrupted during save
- Over-engineering the CLI would violate the product goal

### Constraints
- Keep implementation local-only
- Keep dependency footprint minimal
- Keep code structure simple enough for safe review

## 10. Dependency Management

### Current Dependencies
- Runtime: Python 3.9+
- Standard library modules only for the current implementation:
  - `argparse`
  - `dataclasses`
  - `datetime`
  - `json`
  - `pathlib`
  - `typing`
- Test-only standard library modules:
  - `unittest`
  - `tempfile`
  - `shutil`
  - `io`
  - `os`
  - `contextlib`

### Installation Approach
- No third-party package installation is currently required.
- Local setup should be:
  - install Python 3.9 or newer
  - clone the repository
  - run the CLI with `python task.py ...`
  - run tests with `python -m unittest discover -s tests -p "test*.py" -v`

### Dependency Documentation Needed
- `README.md` with runtime and test prerequisites
- a short dependency note stating that the project currently relies only on the Python standard library

## 11. Documentation Plan

The project now needs explicit documentation work beyond the design doc itself.

### Required Docs
- `README.md`
  - project purpose
  - Python version requirement
  - installation/setup steps
  - command usage examples
  - test command
- dependency documentation
  - current dependency list
  - installation/setup expectations
  - note that there are no third-party packages today
- architecture documentation
  - high-level component overview
  - storage model and file location behavior
  - CLI/service/repository responsibilities

### Documentation Scope Notes
- Documentation should match the implementation already merged to `main`.
- Documentation should avoid promising future features outside v1.

## 12. CI/CD Plan

The project currently has no repository automation and needs a minimal CI baseline.

### Recommended Initial CI
- Trigger on:
  - pushes to `main`
  - pull requests targeting `main`
- Environment:
  - GitHub Actions
  - Python 3.9 and one newer supported Python version if desired later
- Required steps:
  - checkout repository
  - set up Python
  - run `python -m unittest discover -s tests -p "test*.py" -v`

### Initial CD Position
- No deployment pipeline is needed because the product is local-only.
- For v1, "CD" should be limited to keeping `main` green and mergeable.

### CI/CD Documentation Needed
- workflow file comments or accompanying documentation explaining:
  - what the workflow runs
  - when it runs
  - how failures should be interpreted

## 13. Remaining Task Breakdown

The core v1 implementation is already delivered on `main`. Remaining work is documentation and project automation.

### Remaining Workstreams
- Dependency documentation
- Project usage documentation, including `README.md`
- Architecture documentation
- CI/CD setup

### Sequencing
- Documentation tasks can start immediately from the current `main`.
- CI/CD setup can also start now because the test command and project structure are already stable enough for a minimal workflow.
- Architecture documentation should reflect the code already merged in PRs #7 and #8.

## 14. Open Decisions For Approval

Please confirm these design decisions before implementation tickets are created:
- completed tasks remain visible by default
- duplicate descriptions are allowed
- deletion does not require confirmation
- tasks are displayed in creation order
- JSON file storage is acceptable for v1
- storage path should be the project-local data file unless another location is preferred
