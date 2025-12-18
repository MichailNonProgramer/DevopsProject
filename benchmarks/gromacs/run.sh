#!/bin/bash
set -euo pipefail

GMX_BIN="gmx mdrun"
OUTPUT_LOG="gromacs.log"

# Перезаписываем лог
: > "$OUTPUT_LOG"

# Генерируем входные файлы и tpr из общего конфига
python3 generate_input.py 2>&1 | tee -a "$OUTPUT_LOG"
gmx grompp -f input.mdp -c input.gro -p input.top -o input.tpr 2>&1 | tee -a "$OUTPUT_LOG"

# Читаем n_steps из общего конфига (если нет — fallback 1000)
N_STEPS=$(python3 - <<'PY'
import json, os
cfg_path = os.path.join("/workspace", "config", "common.json")
default_steps = 1000
try:
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    print(int(cfg.get("n_steps", default_steps)))
except Exception:
    print(default_steps)
PY
)

START_TIME=$(date +%s.%N)
/usr/bin/time -v $GMX_BIN -s input.tpr -nt 1 -nsteps "$N_STEPS" 2>&1 | tee -a "$OUTPUT_LOG"
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)
echo "elapsed_time_seconds: $DURATION" | tee -a "$OUTPUT_LOG"
