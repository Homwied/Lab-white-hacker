from pathlib import Path
import shutil

file = Path("main_v12.py")
backup = Path("main_v12.py.bak-menu6")

if not file.exists():
    raise SystemExit("ERROR: main_v12.py tidak ditemukan")

if not backup.exists():
    shutil.copy2(file, backup)
    print("Backup dibuat:", backup)

text = file.read_text(encoding="utf-8")

if "import subprocess" not in text:
    text = text.replace(
        "import re\n",
        "import re\nimport subprocess\nimport sys\n",
        1,
    )

menu5 = "║ 5. Lihat daftar laporan          ║"
menu6 = "║ 6. Kesehatan tools V12           ║"

if menu6 not in text:
    if menu5 not in text:
        raise SystemExit("ERROR: baris menu 5 tidak ditemukan")
    text = text.replace(menu5, menu5 + "\n" + menu6, 1)

branch6 = '''        elif choice == "6":
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "08-mobile-intake" / "tools_health.py"),
                ],
                check=False,
            )
'''

if 'elif choice == "6":' not in text:
    marker = '        elif choice == "0":\n'
    if marker not in text:
        raise SystemExit("ERROR: blok pilihan 0 tidak ditemukan")
    text = text.replace(marker, branch6 + marker, 1)

file.write_text(text, encoding="utf-8")
print("UPGRADE MENU 6: BERHASIL")
