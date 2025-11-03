#!/bin/bash
# Minimal GROMACS runner for benchmark
GMX_BIN="gmx mdrun"
INPUT_TPR="input.tpr"
OUTPUT_LOG="gromacs.log"
START_TIME=$(date +%s.%N)
$GMX_BIN -s $INPUT_TPR -nt 1 > $OUTPUT_LOG 2>&1
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)
echo "elapsed_time_seconds: $DURATION" | tee -a $OUTPUT_LOG
