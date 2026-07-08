#!/bin/bash
# Simulator UI driver helpers (fraction-based, device-independent).
# Usage: source /tmp/sim.sh ; sim_shot name ; sim_tap fx fy ; sim_swipe fx1 fy1 fx2 fy2
SIM=9BF8A62D-32B2-4C3C-9E7A-A89F7516F96D
SHOTDIR=/Users/nnhubbard/Documents/cachly-website-github/docs/assets/screenshots
mkdir -p "$SHOTDIR"

# screenshot pixel aspect (w/h) — set after first shot
ASPECT=""

_sim_bounds() {
  osascript -e 'tell application "Simulator" to activate' \
            -e 'delay 0.4' \
            -e 'tell application "System Events" to perform action "AXRaise" of window 1 of process "Simulator"' >/dev/null 2>&1
  osascript -e 'tell application "System Events" to tell process "Simulator"' \
            -e 'set p to position of window 1' -e 'set s to size of window 1' \
            -e 'return (item 1 of p as string) & " " & (item 2 of p) & " " & (item 1 of s) & " " & (item 2 of s)' \
            -e 'end tell'
}

_sim_aspect() {
  if [ -z "$ASPECT" ]; then
    local tmp=/tmp/_aspect.png
    xcrun simctl io $SIM screenshot "$tmp" >/dev/null 2>&1
    ASPECT=$(sips -g pixelWidth -g pixelHeight "$tmp" | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{printf "%.5f", w/h}')
  fi
  echo "$ASPECT"
}

sim_shot() { # name (saved into docs screenshots dir)
  xcrun simctl io $SIM screenshot "$SHOTDIR/$1.png" >/dev/null 2>&1 && echo "shot -> $1.png"
}

sim_coord() { # fx fy -> screenX screenY (echoes "X Y")
  local b; b=$(_sim_bounds); local a; a=$(_sim_aspect)
  python3 -c "
wx,wy,ww,wh=[float(x) for x in '$b'.split()]
a=$a; cw=wh*a; mx=(ww-cw)/2
print(int(wx+mx+$1*cw), int(wy+$2*wh))"
}

sim_tap() { # fx fy
  read X Y < <(sim_coord $1 $2)
  cliclick c:$X,$Y
  echo "tap ($1,$2) -> $X,$Y"
}

sim_swipe() { # fx1 fy1 fx2 fy2  (drag)
  read X1 Y1 < <(sim_coord $1 $2); read X2 Y2 < <(sim_coord $3 $4)
  cliclick dd:$X1,$Y1 w:150 m:$X2,$Y2 du:$X2,$Y2
  echo "swipe ($1,$2)->($3,$4)"
}
