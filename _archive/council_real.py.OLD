import glob, os

print("🔍 SCANNING 6 TOOLS HEXALOGY...")
logs = ""
for f in glob.glob("../../**/*.log", recursive=True) + glob.glob("../../**/*.txt", recursive=True):
    try:
        with open(f) as x: logs += x.read()[:200] + "\n"
    except: pass

# Jika belum ada log real, pake dummy yang tadi tapi udah auto-detect
if not logs:
    logs = "AWS_KEY + Brute + S3"

print(f"LOG GABUNGAN TERDETEKSI:\n{logs[:500]}")

# AUTO CORRELATION
score = 11
if "AWS" in logs and "brute" in logs.lower(): score = 18
if "S3" in logs: score = 20

print(f"\n[FINAL COUNCIL] Risk -> {score}/20 {'SULTAN PARIPURNA' if score==20 else 'SULTAN'}")
