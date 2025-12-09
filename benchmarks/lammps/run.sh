#!/bin/bash
# Minimal LAMMPS benchmark runner
# Автоопределяем бинарник
# LAMMPS_BIN=$(command -v lmp_serial || command -v lmp_stable || command -v lmp || command -v lammps)
# INPUT_FILE="input.lmp"
# OUTPUT_FILE="log.lammps"

# if [ -z "$LAMMPS_BIN" ]; then
#   echo "[ERROR] LAMMPS binary not found!" | tee "$OUTPUT_FILE"
#   exit 1
# fi

# START_TIME=$(date +%s.%N)
# $LAMMPS_BIN -in $INPUT_FILE > $OUTPUT_FILE 2>&1
# END_TIME=$(date +%s.%N)
# DURATION=$(echo "$END_TIME - $START_TIME" | bc)
# echo "elapsed_time_seconds: $DURATION" | tee -a $OUTPUT_FILE
python3 run_lammps.py
