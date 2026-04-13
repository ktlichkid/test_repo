# Contributing Guide (Workflow)

This repository follows a concise contributor workflow focused on review readiness and clean handoffs.

## PR Readiness Rules
- One ticket/issue per PR; no cross-ticket scope
- PR body includes: objective, acceptance-criteria mapping, and links (issue/design)
- Include validation notes (commands/tests, brief evidence)
- Tag a specific reviewer (e.g., @Architect)
- Use `Closes #<issue>` to auto-close on merge

## In-Review Gate
A task may move to `in_review` only after a PR exists and its link is posted in the task thread.
- Post the PR link
- Ensure validation notes are present

## Post-Merge
After the PR is merged, close the linked GitHub issue.