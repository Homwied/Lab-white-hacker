#!/data/data/com.termux/files/usr/bin/bash
cd ~/hexalogy-lab
echo "🏛️ COUNCIL PUSH FIXED"
FOUND=$(find . -type f -name "test.txt" 2>/dev/null | grep -v ".git")
if [ -n "$FOUND" ]; then
  echo "❌ Ada file $FOUND"
  exit 1
else
  echo "✅ HRD PASS: BERSIH"
fi
echo "📊 RISK SCORE: 15/20 SULTAN - Tor 185.220.101.5"
MSG="feat: 07-council-war-room Risk 15/20 - REAL Tor brute 185.220.101.5 - Council FIXED via HP @homwied"
git add .
git commit -m "$MSG" 2>/dev/null || echo "commit sudah ada"
git push -u origin main
echo "✅ DONE REAL!"
