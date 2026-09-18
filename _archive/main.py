import os, subprocess, sys
BASE = os.path.dirname(os.path.abspath(__file__))
print("\n=== LAB HACKER PUTIH - SULTAN EDITION @homwied ===\n")
order = [
    ("01-log-analyzer", ["analyzer.py"]),
    ("02-phishing-checker", ["checker.py"]),
    ("03-secret-scanner", ["scanner.py"]),
    ("04-cloud-pwn-hunter", ["hunter.py"]),
    ("05-ransomware-lab", ["simulator.py", "ransom.py", "lab.py"]),
    ("06-mini-siem", ["siem.py"]),
]
for folder, candidates in order:
    folder_path = os.path.join(BASE, folder)
    if not os.path.exists(folder_path): continue
    for fname in candidates:
        fpath = os.path.join(folder_path, fname)
        if os.path.exists(fpath):
            print(f"\n>>> [{folder}] RUNNING {fname}...")
            subprocess.run([sys.executable, fname], cwd=folder_path)
            break
print("\n=== DONE - LAB EFEKTIF - PALEMBANG SULTAN via HP - 0 RUPIAH ===")
