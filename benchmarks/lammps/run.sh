#!/bin/bash
# Minimal LAMMPS benchmark runner
LAMMPS_BIN="lmp_serial"
INPUT_FILE="input.lmp"
OUTPUT_FILE="log.lammps"
START_TIME=$(date +%s.%N)
$LAMMPS_BIN -in $INPUT_FILE > $OUTPUT_FILE 2>&1
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)
echo "elapsed_time_seconds: $DURATION" | tee -a $OUTPUT_FILE
