# Design Document: Repository Review Guardrails

## 1. Objective

Reduce review churn and process noise in `test_repo` by formalizing lightweight repository guardrails for:
- PR readiness
- review handoff quality
- documentation hygiene
- post-merge issue closure

The goal is to address the concrete failure cases seen in the last delivery cycle without broadening into general team-process tooling.

## 2. Engineering Interpretation Of The Request

The retrospective surfaced repeated operational failures:
- tasks moved to `in_review` before a real PR existed
- documentation PRs contained malformed Markdown or corrupted characters
- one PR mixed scope across tickets
- one CI PR had incorrect trigger/path assumptions
- issue closure after merge was not enforced consistently

The narrowest safe interpretation is:
- document the repository-level rules contributors must follow
- standardize the PR handoff format and checklist
- add minimal repository checks that catch the specific recurring failures
- avoid changing product behavior or adding heavy process infrastructure

## 3. Scope

### In Scope
- contributor-process documentation in the repository
- a standard PR template/checklist
- explicit rules for task state transitions into review
- minimal automation for documentation and process hygiene
- codifying post-merge issue closure expectations

### Out Of Scope
- changing the task-tracker product behavior
- branch protection or GitHub repository settings that require admin-only configuration
- adding external services
- broad workflow automation outside the specific failure cases above
- replacing human review with automated policy enforcement

## 4. Proposed Deliverables

### Contributor Guidance
- add `CONTRIBUTING.md` with repository workflow expectations:
  - stay within assigned scope
  - create a PR before moving a task to `in_review`
  - include issue/design links and validation notes
  - render-check docs before review
  - close the corresponding GitHub issue after merge

### PR Template
- add `.github/PULL_REQUEST_TEMPLATE.md`
- require fields for:
  - linked issue
  - objective
  - scope / out of scope
  - validation performed
  - docs/CI impact
  - merge follow-up confirmation

### Lightweight Hygiene Check
- add a small repository-owned validation script for docs/process hygiene
- initial checks should cover:
  - ASCII-only enforcement for repository docs where that is now the team standard
  - obvious malformed fenced-code-block structure
  - presence of required PR closeout guidance in contributor docs/templates

### CI Follow-Up
- extend the existing GitHub Actions workflow to run the new lightweight hygiene check in addition to the unit tests

## 5. Review And Handoff Rules To Codify

The repository artifacts should make the following operational rules explicit:

### Review Gate
A task is not ready for `in_review` until:
- the PR exists
- the PR link is posted in the task thread
- the PR is scoped to the assigned issue
- validation evidence is included

### Documentation Gate
If a PR changes Markdown or text docs, the author must:
- verify the rendered Markdown is clean
- confirm code fences are balanced
- confirm text is ASCII-only where required by repository convention

### CI Gate
If a PR changes workflow files or CI docs, the author must:
- confirm triggers match the intended protected branch workflow
- confirm paths/commands match the current repository layout
- document what the workflow runs and when it runs

### Merge Follow-Up
After merge:
- the corresponding GitHub issue must be closed
- the task thread handoff should clearly indicate whether closure was automatic or manual

## 6. Implementation Approach

### Documentation-First
- implement guidance in `CONTRIBUTING.md` and the PR template before adding stricter automation
- this keeps expectations reviewable and auditable

### Minimal Automation
- use a small Python standard-library script instead of adding third-party tooling first
- keep checks intentionally narrow to the failures already observed

### CI Integration
- integrate the docs/process hygiene script into the existing CI workflow
- keep CI readable and minimal; do not create a large matrix or additional services

## 7. Validation Strategy

Implementation work from this design should be validated by:
- confirming `CONTRIBUTING.md` and the PR template reflect the agreed repository rules
- running the hygiene script locally against the repository
- confirming CI runs both:
  - `python -m unittest discover -s tests -p "test*.py" -v`
  - the new docs/process hygiene check
- manually verifying a sample PR body can be completed using the template without ambiguity

## 8. Risks And Constraints

### Risks
- over-automating docs hygiene could create noisy false positives
- under-specifying the contributor guidance would not prevent repeat review churn
- repository-wide ASCII enforcement must stay limited to agreed documentation files so it does not accidentally block legitimate future Unicode use cases

### Constraints
- keep the guardrails lightweight
- prefer repository-local logic over external dependencies
- do not assume admin access for branch-protection settings

## 9. Dependency Management

### Proposed Dependencies
- no new runtime dependencies
- no new third-party test dependencies in the initial implementation
- if automation is added, prefer a small Python standard-library script committed in-repo

### Installation Impact
- no additional installation steps should be required beyond the current Python setup
- contributors should be able to run the new hygiene check with the same local Python environment used for the test suite

## 10. Documentation Plan

### New Or Updated Docs Needed
- `CONTRIBUTING.md`
  - repository workflow rules
  - `in_review` gate
  - merge/issue-close expectations
- `.github/PULL_REQUEST_TEMPLATE.md`
  - standardized review handoff/checklist
- `CI.md`
  - update if needed to mention the added hygiene check

### Existing Docs Status
The following documentation already exists on `main` and should not be re-opened unless the implementation requires a narrow update:
- `README.md`
- `docs/setup.md`
- `ARCHITECTURE.md`

## 11. CI/CD Plan

### CI
- keep GitHub Actions as the only CI mechanism
- continue running the unit tests on:
  - pull requests to `main`
  - pushes to `main`
- add one lightweight job or step for docs/process hygiene

### CD
- no deployment changes are needed
- CD remains limited to keeping `main` reviewable and green

### CI/CD Documentation Needed
- `CI.md` should explicitly state that CI now checks:
  - unit tests
  - repository docs/process hygiene

## 12. Proposed Task Breakdown

If this design is approved, create the following follow-up tasks:

### Task A: Contributor Workflow Documentation
- objective: add `CONTRIBUTING.md` with repository workflow rules and review/merge hygiene
- scope:
  - document PR readiness rules
  - document `in_review` gate
  - document issue-close-after-merge rule
- out of scope:
  - product docs rewrite
  - CI implementation

### Task B: Pull Request Template
- objective: add a repository PR template that standardizes review handoff fields
- scope:
  - add `.github/PULL_REQUEST_TEMPLATE.md`
  - require issue link, scope, validation, docs/CI impact, and closeout reminder
- out of scope:
  - GitHub org/repo setting changes outside the tracked file

### Task C: Docs/Process Hygiene Check
- objective: add a lightweight repository-owned script that catches the recurring docs/process defects
- scope:
  - check selected docs for ASCII-only content
  - detect obvious malformed fenced code blocks
  - verify required workflow documentation hooks
- out of scope:
  - full Markdown lint ecosystem
  - unrelated style enforcement

### Task D: CI Update For Guardrails
- objective: extend CI to run the new hygiene check along with the current test suite
- scope:
  - update `.github/workflows/ci.yml`
  - update `CI.md` if workflow behavior changes
- out of scope:
  - release automation
  - deployment

## 13. Assignment Intent

If approved, the implementation should be distributed to minimize overlap:
- `@SWE_01`
  - Task A: Contributor Workflow Documentation
  - Task B: Pull Request Template
- `@SWE_02`
  - Task C: Docs/Process Hygiene Check
  - Task D: CI Update For Guardrails

This split keeps documentation/process artifacts on one side and automation/CI changes on the other.

## 14. Open Decisions For Review

Please confirm these decisions before implementation tickets are created:
- repository docs/process hygiene should stay stdlib-only initially instead of adding third-party lint dependencies
- ASCII-only enforcement should apply to the repository documentation/process files covered by this follow-up
- CI should add only one lightweight docs/process hygiene step, not a broader quality pipeline
- the existing product docs (`README.md`, `docs/setup.md`, `ARCHITECTURE.md`) should remain out of scope unless a narrow update is required by the new guardrail implementation
