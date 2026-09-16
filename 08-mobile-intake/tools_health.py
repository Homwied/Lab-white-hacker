#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import json
import platform
import shutil

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "06-report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TOOLS = [
    "python",
    "git",
    "curl",
    "jq",
    "openssl",
    "dig",
    "sha256sum",
    "find",
]

results = {}
ready = True

print("\n=== COUNCIL V12: KESEHATAN TOOLS ===")

for tool in TOOLS:
    location = shutil.which(tool)
    status = "OK" if location else "BELUM"
    results[tool] = {
        "status": status,
        "location": location,
    }

    if not location:
        ready = False

    print(f"{status:<6} : {tool}")

timestamp = datetime.now()
report = {
    "lab_version": 12,
    "check_time": timestamp.isoformat(timespec="seconds"),
    "device_system": platform.system(),
    "device_machine": platform.machine(),
    "overall_status": "READY" if ready else "INCOMPLETE",
    "tools": results,
}

report_file = REPORT_DIR / (
    "TOOLS-HEALTH-" + timestamp.strftime("%Y%m%d-%H%M%S") + ".json"
)

report_file.write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("\nSTATUS AKHIR :", report["overall_status"])
print("LAPORAN      :", report_file)
