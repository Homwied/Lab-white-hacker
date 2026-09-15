#!/data/data/com.termux/files/usr/bin/bash
cd ~/hexalogy-lab
echo "🏛️ COUNCIL PUSH FIXED"
python3 07-council-war-room/council.py
SCORE=$(cat /tmp/council_score)
if [ "$SCORE" -lt 19 ]; then
  echo "❌ Score $SCORE/20 belum MAX, fix dulu!"
  exit 1
fi
echo "✅ HRD PASS: BERSIH"
echo "📊 RISK SCORE: $SCORE/20 SULTAN - Tor 185.220.101.5"
git add .
git commit -m "feat: 07-council-war-room $SCORE/20 SULTAN MAX - $(date +%H:%M)" 2>/dev/null
git push -u origin main
echo "✅ DONE REAL! $SCORE/20"
