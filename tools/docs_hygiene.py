#!/usr/bin/env python3
# Recreate hygiene script
from __future__ import annotations
import argparse, sys
from pathlib import Path
DEFAULT_PATHS=[Path("ARCHITECTURE.md"),Path("CI.md"),Path("CONTRIBUTING.md"),Path(".github/pull_request_template.md")]
HOOK_PATTERNS=["close the corresponding github issue","pr link","tag a specific"]

def is_ascii_only(t:str)->bool:
    try: t.encode('ascii'); return True
    except UnicodeEncodeError: return False

def check_fences(t:str)->bool:
    return t.count("```")%2==0

def has_hooks(t:str)->bool:
    l=t.lower(); return all(p in l for p in HOOK_PATTERNS)

def main(argv:list[str])->int:
    ap=argparse.ArgumentParser(); ap.add_argument('paths',nargs='*'); a=ap.parse_args(argv)
    targets=[]
    if a.paths:
        for p in a.paths: targets.extend(Path().glob(p))
    else:
        targets=[p for p in DEFAULT_PATHS if p.exists()]
    if not targets:
        print('No target docs found; nothing to check.'); return 0
    failed=False
    for path in targets:
        try: txt=path.read_text(encoding='utf-8')
        except Exception as e:
            print(f'ERROR {path}: could not read file: {e}'); failed=True; continue
        if not is_ascii_only(txt):
            print(f'FAIL {path}: non-ASCII characters detected'); failed=True
        else:
            print(f'OK   {path}: ASCII-only')
        if not check_fences(txt):
            print(f'FAIL {path}: unmatched or malformed fenced code blocks (```)'); failed=True
        else:
            print(f'OK   {path}: fenced code blocks balanced')
        pn=path.name.lower()
        if pn in {'contributing.md','pull_request_template.md'} or str(path).lower().endswith('/.github/pull_request_template.md'):
            if not has_hooks(txt):
                print('FAIL {path}: missing expected guardrail hooks (close-issue, PR link, reviewer tagging)'); failed=True
            else:
                print(f'OK   {path}: guardrail hooks present')
    return 1 if failed else 0

if __name__=='__main__':
    raise SystemExit(main(sys.argv[1:]))
