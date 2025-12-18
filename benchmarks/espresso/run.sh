#!/bin/bash
START_TIME=$(date +%s.%N)
/usr/bin/time -v python3 input.py > espresso.log 2>&1
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)
echo "elapsed_time_seconds: $DURATION" | tee -a espresso.log
