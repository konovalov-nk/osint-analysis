#!/bin/bash
set -u
cd /home/br11k/Downloads/scam/house-of-el-ai
URL="https://www.youtube.com/watch?v=rDKzAml5nn8"
dl() {
  local fmt="$1" name="$2"
  echo "=== START $name ($fmt) $(date +%T) ==="
  yt-dlp --no-playlist -f "$fmt" --merge-output-format webm \
    -o "rDKzAml5nn8_${name}.%(ext)s" "$URL" 2>&1 | tail -6
  echo "=== DONE $name $(date +%T) ==="
}
dl "247+251-20" "720p"
dl "248+251-20" "1080p"
dl "271+251-20" "1440p"
dl "313+251-20" "2160p_vp9"
echo "ALL DONE"
