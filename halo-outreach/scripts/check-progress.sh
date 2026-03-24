#!/bin/bash
# Quick progress checker for lead scraping

echo "🎯 Halo Lead Scraper - Progress Report"
echo "========================================"
echo ""

# Check if scraper is running
if ps aux | grep -v grep | grep selenium-scraper > /dev/null; then
    echo "✅ Scraper is RUNNING"
else
    echo "❌ Scraper is NOT running"
fi

echo ""
echo "📊 Lead Count:"
echo ""

for file in /Users/carterbooth/.openclaw/workspace/halo-outreach/targets/*.csv; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        # Count lines minus header
        count=$(($(wc -l < "$file") - 1))
        echo "  $filename: $count leads"
    fi
done

echo ""
echo "🔍 Recent Activity:"
echo ""
tail -5 /Users/carterbooth/.openclaw/workspace/halo-outreach/logs/scraper-run.log 2>/dev/null | grep -E "Extracted:|Searching:|Waiting"

echo ""
echo "⏱️  To stop scraper: kill \$(ps aux | grep selenium-scraper | grep -v grep | awk '{print \$2}')"
