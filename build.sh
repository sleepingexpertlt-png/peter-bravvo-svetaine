#!/usr/bin/env bash
# Perkuria svetainę iš src/ ir nukopijuoja į site/ (tai publikuojama).
set -euo pipefail
cd "$(dirname "$0")"
python3 src/build2.py
find site -mindepth 1 -not -name CNAME -not -name .nojekyll -delete
cp -a src/dist2/. site/
cp src/404.html site/404.html
echo "Puslapių: $(find site -name index.html | wc -l)"
