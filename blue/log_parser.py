#!/usr/bin/env python3
"""Log Parser multi-format: auth, apache, nginx, syslog, JSON lines."""
import sys, re, json, argparse
from collections import Counter
from colorama import Fore, Style, init
init(autoreset=True)

PATTERNS = {
    "sshd_fail": re.compile(r"Failed password for (?:invalid user )?(\S+) from ([\d\.]+)"),
    "sshd_ok":   re.compile(r"Accepted \S+ for (\S+) from ([\d\.]+)"),
    "sudo":      re.compile(r"sudo:\s+(\S+) : .*COMMAND=(.+)"),
    "http":      re.compile(r'^([\d\.]+) - - \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d+)'),
}
SUSPICIOUS_UA = ["sqlmap","nikto","nmap","masscan","dirbuster","gobuster","hydra"]
SUSPICIOUS_PATH = ["/admin","/.env","/wp-login","/phpmyadmin","/etc/passwd","/.git"]

def parse_file(path):
    f = {"failed_logins": [], "success_logins": [], "sudo_cmds": [],
         "http_requests": [], "suspicious_ua": [], "suspicious_path": [], "unparsed": 0}
    with open(path, errors="ignore") as fh:
        for line in fh:
            m = PATTERNS["sshd_fail"].search(line)
            if m: f["failed_logins"].append((m.group(2), m.group(1))); continue
            m = PATTERNS["sshd_ok"].search(line)
            if m: f["success_logins"].append((m.group(2), m.group(1))); continue
            m = PATTERNS["sudo"].search(line)
            if m: f["sudo_cmds"].append((m.group(1), m.group(2).strip())); continue
            m = PATTERNS["http"].search(line)
            if m:
                ip, ts, method, url, code = m.groups()
                f["http_requests"].append((ip, method, url, code))
                ua_low = line.lower()
                for ua in SUSPICIOUS_UA:
                    if ua in ua_low: f["suspicious_ua"].append((ip, ua, url))
                for p in SUSPICIOUS_PATH:
                    if p in url.lower(): f["suspicious_path"].append((ip, url, code))
                continue
            f["unparsed"] += 1
    return f

def report(f):
    print(Fore.CYAN + "\n============== LOG ANALYSIS ==============\n")
    print(Fore.BLUE + "--- Failed Logins (top IP) ---")
    ip_count = Counter(ip for ip, _ in f["failed_logins"])
    for ip, c in ip_count.most_common(10):
        flag = Fore.RED + " [BRUTE FORCE?]" if c >= 5 else ""
        print(f"  {ip:<20} {c:>4}{flag}")
    print(Fore.BLUE + "\n--- Successful Logins ---")
    for ip, u in f["success_logins"][:20]: print(f"  {ip} -> {u}")
    print(Fore.BLUE + "\n--- Sudo ---")
    for u, c in f["sudo_cmds"][:20]: print(f"  {u}: {c}")
    print(Fore.RED + "\n--- Suspicious UA ---")
    for ip, ua, url in f["suspicious_ua"][:20]: print(f"  {ip} UA={ua} -> {url}")
    print(Fore.RED + "\n--- Suspicious Path ---")
    for ip, url, code in f["suspicious_path"][:20]: print(f"  {ip} {code} {url}")
    print(Fore.YELLOW + f"\n--- Unparsed: {f['unparsed']} lines ---\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    f = parse_file(args.logfile)
    report(f)
    if args.output:
        with open(args.output, "w") as fp:
            json.dump(f, fp, indent=2, default=str)
        print(Fore.GREEN + f"[+] Report: {args.output}")

if __name__ == "__main__":
    main()
