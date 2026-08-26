#!/bin/bash
cd /home/eileen/.openclaw/workspace/duke-lab
opencode run --auto "$(cat r3-critic-brief.md)" > r3-critic-out.txt 2>&1
echo "CRITIC_DONE rc=$?" >> r3-critic-out.txt
