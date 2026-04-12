Adds stdlib-only `tools/docs_hygiene.py` that checks:
- ASCII-only content for selected docs/process files
- balanced fenced code blocks (``` fences)
- presence of required guardrail hooks in contributor/process docs

No third-party dependencies. Output is CI-friendly.

Run: `python tools/docs_hygiene.py`
