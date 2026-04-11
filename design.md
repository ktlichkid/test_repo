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

## 10. Ticketing Plan After Approval

After design approval, break work into self-contained tickets with corresponding GitHub issues. Likely ticket boundaries:
- CLI skeleton and command routing
- task storage and repository behavior
- add/list operations
- complete/delete operations
- validation and persistence tests

Final ticket boundaries should be assigned only after review of this design.

## 11. Open Decisions For Approval

Please confirm these design decisions before implementation tickets are created:
- completed tasks remain visible by default
- duplicate descriptions are allowed
- deletion does not require confirmation
- tasks are displayed in creation order
- JSON file storage is acceptable for v1
- storage path should be the project-local data file unless another location is preferred
