#!/bin/sh
# 在另一台有 Seed-VC 的機器換聲：seed-vc-ssh.sh 來源.wav 參考.wav 輸出.wav
# HOST=使用者@機器（必填）；SEED_VC=遠端 Seed-VC 資料夾（預設 seed-vc，相對於家目錄）
# 一定要開音高控制：不開會把音高拉到 140 Hz 上下，小孩和男聲都會不對
set -e
H=${HOST:?要設 HOST，例如 HOST=me@192.168.1.20}
D=${SEED_VC:-seed-vc}
T=tvd-$$
ssh "$H" "mkdir -p $D/$T"
scp -q "$1" "$H:$D/$T/src.wav"
scp -q "$2" "$H:$D/$T/ref.wav"
ssh "$H" "cd $D && .venv/bin/python inference.py --source $T/src.wav --target $T/ref.wav --output $T/out --diffusion-steps 30 --fp16 False --f0-condition True --auto-f0-adjust True >/dev/null 2>&1"
scp -q "$H:$D/$T/out/vc_*.wav" "$3"
ssh "$H" "rm -rf $D/$T"
