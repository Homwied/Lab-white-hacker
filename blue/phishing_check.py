#!/usr/bin/env python3
"""Phishing email header analyzer."""
import sys, re
from colorama import Fore, init
init(autoreset=True)

SUSPICIOUS_TLDS = (".xyz",".top",".tk",".ml",".ga",".cf",".gq",".zip",".mov")

def extract(h, field):
    m = re.search(rf"^{field}:\s*(.+)$", h, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None

def analyze(h):
    lo = h.lower(); alerts, info = [], []
    for tag in ["spf=fail","spf=softfail","dkim=fail","dmarc=fail","dmarc=none"]:
        if tag in lo: alerts.append(f"Auth FAIL: {tag.upper()}")
    for tag in ["spf=pass","dkim=pass","dmarc=pass"]:
        if tag in lo: info.append(f"Auth OK: {tag.upper()}")
    frm = extract(h, "From") or ""; rp = extract(h, "Return-Path") or ""
    fd = re.search(r"@([\w\.-]+)", frm); rd = re.search(r"@([\w\.-]+)", rp)
    if fd and rd and fd.group(1) != rd.group(1):
        alerts.append(f"From ({fd.group(1)}) != Return-Path ({rd.group(1)})")
    for tld in SUSPICIOUS_TLDS:
        if tld in lo: alerts.append(f"TLD suspicious: {tld}")
    return alerts, info

def main():
    print(Fore.CYAN + "=== PHISHING HEADER ANALYZER ===")
    print("Paste header, Ctrl+D untuk selesai:\n")
    h = sys.stdin.read()
    if not h.strip(): print(Fore.YELLOW + "[!] Kosong."); return
    alerts, info = analyze(h)
    print(Fore.GREEN + "\n--- OK ---")
    for i in info or ["(none)"]: print(f"  ✓ {i}")
    print(Fore.RED + "\n--- ALERT ---")
    if alerts:
        for a in alerts: print(f"  ✗ {a}")
        print(Fore.RED + f"\n[!] {len(alerts)} indikator phishing.")
    else:
        print("  (none)")

if __name__ == "__main__":
    main()
