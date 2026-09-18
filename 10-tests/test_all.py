#!/usr/bin/env python3
import sys, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("red/scan.sh", "executable"),
    ("blue/log_parser.py", "file"),
    ("blue/timeline_builder.py", "file"),
    ("blue/triage.py", "file"),
    ("blue/phishing_check.py", "file"),
    ("purple/council_real.py", "file"),
    ("purple.sh", "executable"),
    ("main_v12.py", "file"),
    ("00-config/targets_allow", "file"),
    ("00-config/policy.conf", "file"),
    ("09-audit-log/events.log", "file"),
]

def check(rel, kind):
    p = ROOT / rel
    if not p.exists(): return f"❌ MISSING: {rel}"
    if kind == "executable" and not os.access(p, os.X_OK):
        return f"⚠️  NOT EXEC: {rel}"
    return f"✅ OK: {rel}"

ok = 0; fail = 0
print("=" * 50)
for rel, kind in CHECKS:
    r = check(rel, kind)
    print(r)
    if r.startswith("✅"): ok += 1
    else: fail += 1
print("=" * 50)
print(f"Passed: {ok} | Issues: {fail}")
sys.exit(0 if fail == 0 else 1)
