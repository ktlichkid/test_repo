# Design: Repository Review Guardrails

## Objective

Reduce repeat review churn in `test_repo` by adding a small set of repository guardrails around PR readiness, docs hygiene, and post-merge cleanup.

## Problem Statement

Recent failures were operational, not product-related:
- tasks moved to `in_review` before a real PR existed
- docs PRs had malformed Markdown or corrupted characters
- one PR mixed scope across tickets
- one CI PR had wrong trigger/path assumptions
- merged work did not always close the corresponding GitHub issue

## Proposed Changes

### 1. Contributor Workflow Rules
Add `CONTRIBUTING.md` with the minimum required rules:
- do not move a task to `in_review` until a PR exists and the PR link is posted
- keep each PR scoped to its assigned issue
- include validation notes in the PR
- close the corresponding GitHub issue after merge

### 2. Pull Request Template
Add `.github/PULL_REQUEST_TEMPLATE.md` with required fields:
- linked issue
- objective
- scope / out of scope
- validation performed
- docs/CI impact
- merge follow-up reminder

### 3. Lightweight Docs/Process Check
Add one repository-owned Python check for the specific recurring failures:
- ASCII-only enforcement for the repository docs/process files covered by this follow-up
- obvious malformed fenced code blocks
- required contributor/PR-template closeout guidance present

### 4. CI Follow-Up
Extend the existing GitHub Actions workflow so CI runs:
- the current unit tests
- the new docs/process hygiene check

## Dependency Management

- no new runtime dependencies
- no new third-party tooling in the first pass
- use a small Python standard-library script if automation is added

## Documentation Plan

New or updated docs in this follow-up:
- `CONTRIBUTING.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `CI.md` if the CI behavior description needs to mention the new hygiene check

Existing product docs (`README.md`, `docs/setup.md`, `ARCHITECTURE.md`) stay out of scope unless a narrow update is required by implementation.

## CI/CD Plan

- keep GitHub Actions as the only CI mechanism
- continue running on pull requests to `main` and pushes to `main`
- add only one lightweight docs/process hygiene step
- no deployment changes

## Task Breakdown

If approved, create these implementation tickets:

### Task A
- objective: add `CONTRIBUTING.md`
- assignee: `@SWE_01`

### Task B
- objective: add `.github/PULL_REQUEST_TEMPLATE.md`
- assignee: `@SWE_01`

### Task C
- objective: add the docs/process hygiene check
- assignee: `@SWE_02`

### Task D
- objective: update CI to run the new check
- assignee: `@SWE_02`

## Open Decisions

Please confirm before implementation:
- stdlib-only automation is preferred over adding third-party lint tooling
- ASCII-only enforcement should apply to the documentation/process files covered by this follow-up
- CI should stay minimal and limited to one added hygiene check
