#!/usr/bin/env python3
"""Timeline builder - gabung event dari multi-log."""
import sys, re, json, argparse
from datetime import datetime
from collections import Counter
from colorama import Fore, Style, init
init(autoreset=True)

TS_PATTERNS = [
    (re.compile(r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'), "%d/%b/%Y:%H:%M:%S"),
    (re.compile(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})'), None),
    (re.compile(r'^(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})'), "%b %d %H:%M:%S"),
    (re.compile(r'"timestamp"\s*:\s*(\d{10})'), "epoch"),
]

def parse_ts(line):
    for rx, fmt in TS_PATTERNS:
        m = rx.search(line)
        if m:
            try:
                raw = m.group(1)
                if fmt == "epoch": return datetime.fromtimestamp(int(raw))
                if fmt is None: return datetime.fromisoformat(raw.replace("Z",""))
                return datetime.strptime(raw, fmt)
            except Exception: continue
    return None

def classify(l):
    lo = l.lower()
    if "failed password" in lo: return "AUTH_FAIL"
    if "accepted" in lo: return "AUTH_OK"
    if "sudo:" in lo: return "SUDO"
    if "sqlmap" in lo or "nikto" in lo: return "SCAN"
    if "error" in lo: return "ERROR"
    return "INFO"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("-o", "--out", default="timeline")
    args = ap.parse_args()
    events = []
    for fp in args.logs:
        try:
            with open(fp, errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    ts = parse_ts(line)
                    if ts:
                        events.append({"timestamp": ts.isoformat(), "epoch": int(ts.timestamp()),
                                       "source": fp, "line_no": i, "type": classify(line),
                                       "raw": line.rstrip()})
        except FileNotFoundError:
            print(Fore.YELLOW + f"[!] Skip: {fp}")
    events.sort(key=lambda e: e["epoch"])
    if not events:
        print(Fore.RED + "[-] Tidak ada event ber-timestamp."); return
    with open(f"{args.out}.txt", "w") as f:
        for e in events:
            f.write(f"[{e['timestamp']}] [{e['type']:<10}] ({e['source']}:{e['line_no']}) {e['raw']}\n")
    with open(f"{args.out}.json", "w") as f:
        json.dump(events, f, indent=2)
    counts = Counter(e["type"] for e in events)
    print(Fore.CYAN + f"\n=== TIMELINE: {len(events)} events ===\n")
    for t, c in counts.most_common():
        color = Fore.RED if t in ("AUTH_FAIL","ERROR") else Fore.GREEN
        print(f"  {color}{t:<12}{Style.RESET_ALL} {c}")
    print(Fore.GREEN + f"\n[+] {args.out}.txt & .json")

if __name__ == "__main__":
    main()
