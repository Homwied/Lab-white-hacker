#!/usr/bin/env python3
"""IP/Domain Triage: VT + AbuseIPDB + OTX."""
import os, sys, json, requests
from colorama import Fore, Style, init
init(autoreset=True)

VT_KEY = os.getenv("VT_API_KEY", "")
ABUSE_KEY = os.getenv("ABUSEIPDB_KEY", "")
OTX_KEY = os.getenv("OTX_API_KEY", "")

def vt_ip(ip):
    if not VT_KEY: return {"error": "VT_API_KEY kosong"}
    r = requests.get(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
                     headers={"x-apikey": VT_KEY}, timeout=15)
    if r.status_code != 200: return {"error": f"HTTP {r.status_code}"}
    a = r.json()["data"]["attributes"]
    return {"stats": a.get("last_analysis_stats"), "country": a.get("country"),
            "asn": a.get("asn"), "as_owner": a.get("as_owner")}

def abuse_ip(ip):
    if not ABUSE_KEY: return {"error": "ABUSEIPDB_KEY kosong"}
    r = requests.get("https://api.abuseipdb.com/api/v2/check",
                     headers={"Key": ABUSE_KEY, "Accept": "application/json"},
                     params={"ipAddress": ip, "maxAgeInDays": 90}, timeout=15)
    if r.status_code != 200: return {"error": f"HTTP {r.status_code}"}
    d = r.json()["data"]
    return {"abuse_score": d.get("abuseConfidenceScore"), "country": d.get("countryCode"),
            "isp": d.get("isp"), "total_reports": d.get("totalReports")}

def otx_ip(ip):
    if not OTX_KEY: return {"error": "OTX_API_KEY kosong"}
    r = requests.get(f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
                     headers={"X-OTX-API-KEY": OTX_KEY}, timeout=15)
    if r.status_code != 200: return {"error": f"HTTP {r.status_code}"}
    return {"pulse_count": r.json().get("pulse_info", {}).get("count", 0)}

def verdict(results):
    score = 0
    vt = results.get("virustotal", {})
    if isinstance(vt, dict) and "stats" in vt:
        score += vt["stats"].get("malicious", 0) * 10
    ab = results.get("abuseipdb", {})
    if isinstance(ab, dict) and "abuse_score" in ab:
        score += ab["abuse_score"] // 5
    ot = results.get("otx", {})
    if isinstance(ot, dict) and ot.get("pulse_count", 0) > 0:
        score += ot["pulse_count"] * 5
    if score >= 50: return "MALICIOUS", Fore.RED
    if score >= 10: return "SUSPICIOUS", Fore.YELLOW
    return "CLEAN", Fore.GREEN

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else input("IP/Domain: ").strip()
    print(Fore.CYAN + f"\n=== TRIAGE: {target} ===\n")
    results = {}
    if target.replace(".", "").isdigit():
        results["virustotal"] = vt_ip(target)
        results["abuseipdb"] = abuse_ip(target)
        results["otx"] = otx_ip(target)
    else:
        results["virustotal"] = {"note": "Domain lookup belum diimplementasi di v1.0"}
    for src, data in results.items():
        color = Fore.YELLOW if isinstance(data, dict) and "error" in data else Fore.WHITE
        print(f"{color}[{src}]{Style.RESET_ALL}")
        print(json.dumps(data, indent=2, default=str)); print()
    v, c = verdict(results)
    print(c + f">>> VERDICT: {v}\n")

if __name__ == "__main__":
    main()
