#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
LAB="$HOME/lab-hacker-putih"
cd "$LAB"

R="\033[1;31m"; G="\033[1;32m"; Y="\033[1;33m"; B="\033[1;34m"; C="\033[1;36m"; N="\033[0m"

while true; do
    clear
    echo -e "${C}"
    cat <<'BANNER'
╔══════════════════════════════════════════════════╗
║         PURPLE TEAM LAB - TERMUX v1.0            ║
║         Red + Blue + Council REAL                ║
╚══════════════════════════════════════════════════╝
BANNER
    echo -e "${N}"
    echo -e "  ${R}[RED]${N}  1) Scan target (whitelist enforced)"
    echo -e "  ${R}[RED]${N}  2) Lihat whitelist"
    echo -e "  ${B}[BLUE]${N} 3) Log parser"
    echo -e "  ${B}[BLUE]${N} 4) Timeline builder"
    echo -e "  ${B}[BLUE]${N} 5) IOC Triage (VT+AbuseIPDB)"
    echo -e "  ${B}[BLUE]${N} 6) Phishing header check"
    echo -e "  ${C}[PURPLE]${N} 7) Council War Room (korelasi MITRE)"
    echo -e "  ${C}[PURPLE]${N} 8) Buka main_v12.py (lab management)"
    echo -e "  ${Y}[UTIL]${N}  9) Health check HP"
    echo -e "  ${Y}[UTIL]${N} 10) Lihat report terbaru"
    echo -e "  ${Y}[UTIL]${N} 11) Lihat audit log"
    echo -e "  ${R}0)${N} Keluar"
    echo
    read -p "Pilih [0-11]: " c

    case "$c" in
        1) read -p "Target: " t; ./red/scan.sh "$t" ;;
        2) grep -v '^#' 00-config/targets_allow | grep -v '^$' ;;
        3) read -p "Path log: " f; python blue/log_parser.py "$f" ;;
        4) read -p "File log (spasi): " -a fs; python blue/timeline_builder.py "${fs[@]}" ;;
        5) read -p "IP: " ip; python blue/triage.py "$ip" ;;
        6) python blue/phishing_check.py ;;
        7) python purple/council_real.py ;;
        8) python main_v12.py ;;
        9) bash 07-council-war-room/hp-health.sh 2>/dev/null || ping -c1 8.8.8.8 ;;
        10) ls -lt 06-report/ | head -10 ;;
        11) tail -30 09-audit-log/events.log ;;
        0) echo "Bye!"; exit 0 ;;
        *) echo -e "${R}Pilihan invalid${N}" ;;
    esac
    echo; read -p "Enter lanjut..."
done
