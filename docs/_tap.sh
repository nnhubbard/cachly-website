#!/bin/bash
# Device-point tap driver: idb reads (describe-all) + System Events AX writes.
# idb HID taps AND cliclick clicks are silently broken on this runtime
# (macOS 26 / iOS 26.5 sim); System Events "click at" (AX-synthesized) is the
# one method that registers — VERIFIED 2026-07-01 (tapped Map/List segment).
# Coordinates are DEVICE POINTS (440x956 on iPhone 17 Pro Max) — same space
# ielems prints, so read → tap directly.
# Requires: Accessibility permission for the hosting terminal; run unsandboxed
# (dangerouslyDisableSandbox from Claude). Window > Show Device Bezels OFF
# (content fills window 1:1 below the 52 pt title bar).
export PATH="$HOME/Library/Python/3.9/bin:/opt/homebrew/bin:$PATH"
SIM=6DD0DEBC-742C-4F8F-B569-A17046F661D2
DEV_W=440; DEV_H=956
TITLE=52   # Simulator window title bar height (bezels OFF; window h - 956)
SHOTDIR=/Users/nnhubbard/Documents/cachly-website-github/docs/assets/screenshots
mkdir -p "$SHOTDIR"

_win() { # echoes "wx wy ww wh"
  osascript -e 'tell application "Simulator" to activate' -e 'delay 0.3' \
    -e 'tell application "System Events" to tell process "Simulator"' \
    -e 'set p to position of window 1' -e 'set s to size of window 1' \
    -e 'return (item 1 of p as string) & " " & (item 2 of p) & " " & (item 1 of s) & " " & (item 2 of s)' \
    -e 'end tell'
}

dcoord() { # px py -> screen "X Y"
  local b; b=$(_win)
  python3 -c "
wx,wy,ww,wh=[float(x) for x in '$b'.split()]
ch=wh-$TITLE; cw=ch*$DEV_W/$DEV_H; mx=(ww-cw)/2
print(int(wx+mx+$1/$DEV_W*cw), int(wy+$TITLE+$2/$DEV_H*ch))"
}

dtap() { # px py (device points) — atomic: activate → bounds → click in ONE script
  osascript <<EOF
tell application "Simulator" to activate
delay 0.3
tell application "System Events"
    tell process "Simulator"
        set {wx, wy} to position of window 1
        set {ww, wh} to size of window 1
        set ch to wh - $TITLE
        set cw to ch * $DEV_W / $DEV_H
        set mx to (ww - cw) / 2
        set cx to wx + mx + ($1 / $DEV_W) * cw
        set cy to wy + $TITLE + ($2 / $DEV_H) * ch
        click at {cx, cy}
        return "tap dev($1,$2) -> screen(" & (cx as integer) & "," & (cy as integer) & ")"
    end tell
end tell
EOF
}

# UNVERIFIED on this runtime: cliclick clicks don't register, so this drag
# likely doesn't either. Prefer app-level navigation over swipes; test before
# relying on it, and fall back to asking the user to scroll if broken.
dswipe() { # px1 py1 px2 py2
  read X1 Y1 < <(dcoord $1 $2); read X2 Y2 < <(dcoord $3 $4)
  cliclick dd:$X1,$Y1 w:200 m:$X2,$Y2 du:$X2,$Y2
  echo "swipe dev($1,$2)->($3,$4)"
}

dpress() { # px py [ms] — long press (cliclick drags DO register, unlike its clicks)
  local MS=${3:-800}
  read X Y < <(dcoord $1 $2)
  cliclick dd:$X,$Y w:$MS du:$X,$Y
  echo "press dev($1,$2) ${MS}ms"
}

# UNVERIFIED: cliclick typing may be broken like its clicks. Alternatives if
# so: System Events "keystroke", or simctl pasteboard + long-press Paste.
dtype() { # type text into focused field
  cliclick t:"$1"
}

ishot() { xcrun simctl io "$SIM" screenshot "$SHOTDIR/$1.png" >/dev/null 2>&1; echo "shot $1.png"; }

CAPD=/Users/nnhubbard/Documents/cachly-website-github/docs/_captures
icap() { # name — screenshot + ielems dump in one step
  ishot "$1"; ielems > "$CAPD/$1.txt"
}
iscroll() { # name — capture rest of a scrollable screen as name-2, name-3... until content stops changing
  # Swipes hug the right edge (x=425): clear of toggles/fields, works in SwiftUI forms.
  # NOTE: do not use on sheets you must keep open — the final scroll-back can dismiss them.
  local i=2 before after
  while : ; do
    before=$(ielems | md5)
    dswipe 425 780 425 280 >/dev/null; sleep 1.3
    after=$(ielems | md5)
    [ "$before" = "$after" ] && break
    icap "$1-$i"
    i=$((i+1)); [ $i -gt 6 ] && break
  done
  dswipe 425 300 425 800 >/dev/null; sleep 0.8; dswipe 425 300 425 800 >/dev/null; sleep 0.8  # back to top
}

ielems() { idb ui describe-all --udid "$SIM" 2>/dev/null | python3 -c "
import json,sys
for e in json.load(sys.stdin):
    l=e.get('AXLabel') or ''
    f=e.get('frame',{})
    if l.strip(): print(f\"{int(f.get('x',0)+f.get('width',0)/2)},{int(f.get('y',0)+f.get('height',0)/2)}  {e.get('type','')}  {l!r}\")
"; }
