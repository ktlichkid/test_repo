#!/usr/bin/env python3
"""
Lightweight docs/process hygiene check (stdlib-only).
- ASCII-only enforcement for selected docs/process files
- Balanced fenced code blocks (```)
- Presence of guardrail hooks in contributor/process docs

Exit codes:
0 = all checks pass
1 = one or more checks failed

Usage:
  python tools/docs_hygiene.py [paths...]
If no paths are given, a default allowlist is used.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

DEFAULT_PATHS = [
    Path("ARCHITECTURE.md"),
    Path("CI.md"),
    Path("CONTRIBUTING.md"),
    Path(".github/pull_request_template.md"),
]

# Phrases required by guardrail docs/templates
HOOK_PATTERNS = [
    "close the corresponding github issue",  # post-merge closeout
    "pr link",                               # link PR when moving to in_review
    "tag a specific",                        # reviewer tagging guidance
]

def is_ascii_only(text: str) -> bool:
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False

def check_fences(text: str) -> bool:
    # Count occurrences of triple backticks; should be even
    count = text.count("```")
    return (count % 2) == 0

def has_hooks(text: str) -> bool:
    low = text.lower()
    return all(p in low for p in HOOK_PATTERNS)

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="Files or globs to check")
    args = ap.parse_args(argv)

    # Resolve target files
    targets: list[Path] = []
    if args.paths:
        for p in args.paths:
            targets.extend(Path().glob(p))
    else:
        targets = [p for p in DEFAULT_PATHS if p.exists()]

    if not targets:
        print("No target docs found; nothing to check.")
        return 0

    failed = False
    for path in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"ERROR {path}: could not read file: {e}")
            failed = True
            continue

        # ASCII-only (docs/process only)
        if not is_ascii_only(text):
            print(f"FAIL {path}: non-ASCII characters detected")
            failed = True
        else:
            print(f"OK   {path}: ASCII-only")

        # Fenced code blocks balanced
        if not check_fences(text):
            print(f"FAIL {path}: unmatched or malformed fenced code blocks (```)")
            failed = True
        else:
            print(f"OK   {path}: fenced code blocks balanced")

        # Guardrail hooks presence (only for process/contributor docs)
        if path.name.lower() in {"contributing.md", "pull_request_template.md"} or \
           str(path).lower().endswith("/.github/pull_request_template.md"):
            if not has_hooks(text):
                print(f"FAIL {path}: missing expected guardrail hooks (close-issue, PR link, reviewer tagging)")
                failed = True
            else:
                print(f"OK   {path}: guardrail hooks present")

    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
