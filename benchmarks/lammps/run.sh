#!/bin/bash
LAMMPS_BIN=$(command -v lmp_serial || command -v lmp_stable || command -v lmp || command -v lammps)
INPUT_FILE="input.lmp"
OUTPUT_FILE="lammps.log"

if [ -z "$LAMMPS_BIN" ]; then
  echo "[ERROR] LAMMPS binary not found!" | tee "$OUTPUT_FILE"
  exit 1
fi

# Генерируем input.lmp из общего конфига перед запуском
python3 generate_input.py

START_TIME=$(date +%s.%N)
/usr/bin/time -v "$LAMMPS_BIN" -in "$INPUT_FILE" > "$OUTPUT_FILE" 2>&1
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)
echo "elapsed_time_seconds: $DURATION" | tee -a "$OUTPUT_FILE"

# Удаляем временные файлы
rm -f "$INPUT_FILE" log.lammps log.* 2>/dev/null || true
