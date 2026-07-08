#!/bin/bash
# idb-based simulator driver — taps in DEVICE POINTS (stable, no window mapping).
export PATH="$HOME/Library/Python/3.9/bin:/opt/homebrew/bin:$PATH"
SIM=6DD0DEBC-742C-4F8F-B569-A17046F661D2
SHOTDIR=/Users/nnhubbard/Documents/cachly-website-github/docs/assets/screenshots
mkdir -p "$SHOTDIR"
# iPhone 17 Pro Max: 440 x 956 pt. Tab bar centers (5 tabs), y~897.
TAB_Y=897
declare -A TABX=( [live]=44 [lists]=132 [logs]=220 [trackables]=308 [more]=396 )

itap()  { idb ui tap --udid "$SIM" "$1" "$2" 2>/dev/null; echo "tap $1,$2"; }
itab()  { idb ui tap --udid "$SIM" "${TABX[$1]}" "$TAB_Y" 2>/dev/null; echo "tab $1"; }
iswipe(){ idb ui swipe --udid "$SIM" "$1" "$2" "$3" "$4" 2>/dev/null; echo "swipe $1,$2->$3,$4"; }
ishot() { xcrun simctl io "$SIM" screenshot "$SHOTDIR/$1.png" >/dev/null 2>&1; echo "shot $1.png"; }
idesc() { idb ui describe-all --udid "$SIM" 2>/dev/null; }
# Print labeled elements (label @ x,y center)
ielems(){ idb ui describe-all --udid "$SIM" 2>/dev/null | python3 -c "
import json,sys
for e in json.load(sys.stdin):
    l=e.get('AXLabel') or ''
    f=e.get('frame',{})
    if l: print(f\"{int(f.get('x',0)+f.get('width',0)/2)},{int(f.get('y',0)+f.get('height',0)/2)}  {e.get('type','')}  {l!r}\")
"; }
