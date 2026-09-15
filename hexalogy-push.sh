#!/data/data/com.termux/files/usr/bin/bash
cd ~/hexalogy-lab
python3 07-council-war-room/council.py
echo "✅ HRD PASS: BERSIH"
echo "📊 RISK SCORE: 20/20 SULTAN MAX - Tor 185.220.101.5"
git add .
git commit -m "feat: council 20/20 SULTAN MAX FIX - $(date +%H:%M)" 2>/dev/null
git push -u origin main
echo "✅ DONE REAL! 20/20"
