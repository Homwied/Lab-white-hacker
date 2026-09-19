#!/usr/bin/env python3
"""Council War Room v2 - REAL correlation engine (bukan dummy)."""
import re, json, glob
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from colorama import Fore, Style, init
init(autoreset=True)

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "09-audit-log"
REPORT_DIR = ROOT / "06-report"
REPORT_DIR.mkdir(exist_ok=True)

# MITRE ATT&CK mapping
MITRE_MAP = {
    r"failed password|auth fail":      ("T1110", "Brute Force", 7),
    r"invalid user":                   ("T1078", "Valid Accounts", 8),
    r"sqlmap|nikto|nmap|masscan":      ("T1595", "Active Scanning", 3),
    r"sql injection|union select":     ("T1190", "Exploit Public-Facing", 9),
    r"base64|obfuscat":                ("T1027", "Obfuscated Files", 5),
    r"persist|cron|systemd|rc\.local": ("T1053", "Scheduled Task", 8),
    r"exfil|upload.*c2":               ("T1041", "Exfiltration C2", 9),
    # r"ransom|encrypt.*file|locked":    ("T1486", "Data Encrypted", 10),   # disabled - false positive
}

def scan_logs():
    text, sources = "", []
    patterns = ["events.log"]
    for pat in patterns:
        for f in glob.glob(str(LOG_DIR / "**" / pat), recursive=True):
            try:
                with open(f, errors="ignore") as fp:
                    c = fp.read(); text += c + "\n"; sources.append((f, len(c)))
            except Exception: pass
    return text, sources

def correlate(text):
    hits = []
    for pattern, (tid, name, sev) in MITRE_MAP.items():
        m = re.findall(pattern, text, re.IGNORECASE)
        if m:
            hits.append({"technique": tid, "name": name, "count": len(m), "severity": sev})
    return hits

def risk_score(hits):
    if not hits: return 0, "CLEAN"
    score = sum(h["severity"] * (1 + h["count"]**0.5) for h in hits)
    score = min(int(score), 100)
    if score >= 70: v = "CRITICAL"
    elif score >= 40: v = "HIGH"
    elif score >= 15: v = "MEDIUM"
    elif score > 0: v = "LOW"
    else: v = "CLEAN"
    return score, v

def main():
    print(Fore.CYAN + "🏛️  COUNCIL WAR ROOM v2 - REAL ENGINE")
    print("=" * 55)

    text, sources = scan_logs()
    print(f"📂 Sources: {len(sources)} files")
    for f, size in sources[:5]:
        print(f"   - {Path(f).name} ({size} bytes)")

    if not text.strip():
        print(Fore.YELLOW + "⚠️  Tidak ada log. Jalankan modul red/blue dulu.")
        return

    hits = correlate(text)
    score, verdict = risk_score(hits)

    print(f"\n🎯 MITRE Matches: {len(hits)}")
    print("-" * 55)
    for h in sorted(hits, key=lambda x: -x["severity"]):
        print(f"  [{h['technique']}] {h['name']:<35} x{h['count']} (sev={h['severity']})")

    color = Fore.RED if verdict in ("CRITICAL","HIGH") else Fore.YELLOW if verdict == "MEDIUM" else Fore.GREEN
    print("\n" + "=" * 55)
    print(color + f"📊 RISK: {score}/100  →  VERDICT: {verdict}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = REPORT_DIR / f"council-{ts}.json"
    out.write_text(json.dumps({
        "timestamp": ts, "score": score, "verdict": verdict,
        "hits": hits, "sources": [s[0] for s in sources]
    }, indent=2))
    print(Fore.GREEN + f"💾 Report: {out}")

if __name__ == "__main__":
    main()
