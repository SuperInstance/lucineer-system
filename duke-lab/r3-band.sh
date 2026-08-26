#!/bin/bash
cd /home/eileen/.openclaw/workspace/duke-lab
opencode run --auto "$(cat r3-band-brief.md)" > r3-band-out.txt 2>&1
echo "BAND_DONE rc=$?" >> r3-band-out.txt
