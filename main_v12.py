#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import ipaddress
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
POLICY_FILE = ROOT / "00-config" / "policy.conf"
TARGET_FILE = ROOT / "00-config" / "targets.allow"
LOG_DIR = ROOT / "09-audit-log"
REPORT_DIR = ROOT / "06-report"

LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def read_policy():
    data = {}
    if POLICY_FILE.exists():
        for line in POLICY_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()
    return data


def read_targets():
    if not TARGET_FILE.exists():
        return []
    return [
        line.strip()
        for line in TARGET_FILE.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def audit(action, result, target="-"):
    timestamp = datetime.now().isoformat(timespec="seconds")
    with (LOG_DIR / "events.log").open("a", encoding="utf-8") as log:
        log.write(
            f"{timestamp} | {action} | {result} | target={target}\n"
        )


def target_type(target):
    try:
        ipaddress.ip_address(target)
        return "Alamat IP"
    except ValueError:
        if target == "localhost":
            return "Perangkat lokal"
        return "Nama domain/host"


def valid_target_format(target):
    return bool(re.fullmatch(r"[A-Za-z0-9._:-]+", target))


def show_status():
    policy = read_policy()

    print("\n=== STATUS LAB V12 ===")
    print("Versi       :", policy.get("LAB_VERSION", "belum diatur"))
    print("Mode        :", policy.get("DEFAULT_MODE", "belum diatur"))
    print("Allowlist   :", policy.get("REQUIRE_ALLOWLIST", "belum diatur"))
    print("Dry-run     :", policy.get("DRY_RUN_DEFAULT", "belum diatur"))
    print("Audit log   :", policy.get("AUDIT_LOG", "belum diatur"))
    print("Jumlah target:", len(read_targets()))
    audit("SHOW_STATUS", "OK")


def show_targets():
    targets = read_targets()

    print("\n=== TARGET DIIZINKAN ===")
    if not targets:
        print("Belum ada target.")
    else:
        for number, target in enumerate(targets, 1):
            print(f"{number}. {target} [{target_type(target)}]")

    audit("SHOW_TARGETS", "OK")


def add_target():
    target = input("\nTarget milik sendiri/berizin: ").strip().lower()

    if not target or not valid_target_format(target):
        print("Format target tidak valid.")
        audit("ADD_TARGET", "REJECTED_FORMAT", target or "-")
        return

    targets = read_targets()
    if target in targets:
        print("Target sudah terdaftar.")
        return

    confirmation = input(
        "Ketik SETUJU untuk mengonfirmasi kepemilikan/izin: "
    ).strip()

    if confirmation != "SETUJU":
        print("Dibatalkan karena izin belum dikonfirmasi.")
        audit("ADD_TARGET", "REJECTED_NO_CONFIRMATION", target)
        return

    with TARGET_FILE.open("a", encoding="utf-8") as file:
        file.write(target + "\n")

    print("Target berhasil didaftarkan.")
    audit("ADD_TARGET", "OK", target)


def initial_intake():
    target = input("\nMasukkan target terdaftar: ").strip().lower()

    if target not in read_targets():
        print("DITOLAK: target belum ada dalam allowlist.")
        audit("INITIAL_INTAKE", "BLOCKED_NOT_ALLOWLISTED", target)
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report = REPORT_DIR / f"INITIAL-INTAKE-{timestamp}.txt"

    content = (
        "LAB HACKER PUTIH V12\n"
        "LAPORAN INTAKE AWAL\n"
        "====================\n"
        f"Waktu       : {datetime.now().isoformat(timespec='seconds')}\n"
        f"Target      : {target}\n"
        f"Jenis       : {target_type(target)}\n"
        "Allowlist   : LULUS\n"
        "Konfirmasi  : TERCATAT\n"
        "Mode        : MOBILE_ASSESSMENT\n"
        "Status      : SIAP UNTUK PEMERIKSAAN PASIF\n"
        "Catatan     : Belum ada modul aktif yang dijalankan.\n"
    )

    report.write_text(content, encoding="utf-8")
    print("Intake berhasil.")
    print("Laporan:", report)
    audit("INITIAL_INTAKE", "OK", target)


def show_reports():
    reports = sorted(REPORT_DIR.glob("INITIAL-INTAKE-*.txt"))

    print("\n=== LAPORAN INTAKE ===")
    if not reports:
        print("Belum ada laporan.")
        return

    for report in reports[-10:]:
        print("-", report.name)


def main():
    while True:
        print("""
╔══════════════════════════════════╗
║       LAB HACKER PUTIH V12       ║
║       MOBILE COUNCIL EDITION      ║
╠══════════════════════════════════╣
║ 1. Status dan kebijakan lab      ║
║ 2. Daftar target yang diizinkan  ║
║ 3. Daftarkan target berizin      ║
║ 4. Buat intake awal target       ║
║ 5. Lihat daftar laporan          ║
║ 6. Kesehatan tools V12           ║
║ 0. Keluar                        ║
╚══════════════════════════════════╝
""")

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            show_status()
        elif choice == "2":
            show_targets()
        elif choice == "3":
            add_target()
        elif choice == "4":
            initial_intake()
        elif choice == "5":
            show_reports()
        elif choice == "6":
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "08-mobile-intake" / "tools_health.py"),
                ],
                check=False,
            )
        elif choice == "0":
            audit("EXIT", "OK")
            print("Council V12 selesai.")
            break
        else:
            print("Pilihan tidak tersedia.")


if __name__ == "__main__":
    main()
