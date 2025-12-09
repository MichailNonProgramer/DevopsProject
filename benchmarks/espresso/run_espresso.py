import subprocess
import psutil
import time
import json
import os

LOG = "espresso.log"
METRICS = "espresso_metrics.json"

cmd = ["python3", "input.py"]

print("Running ESPResSo with monitoring")

with open(LOG, "w") as log_file:
    start_time = time.time()

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    p = psutil.Process(proc.pid)
    cpu_max = 0
    ram_max = 0

    for line in proc.stdout:
        log_file.write(line)
        try:
            cpu = p.cpu_percent(interval=0.1)
            mem = p.memory_info().rss / (1024**2)   # MB
            cpu_max = max(cpu_max, cpu)
            ram_max = max(ram_max, mem)
        except psutil.NoSuchProcess:
            break

    proc.wait()
    end_time = time.time()

elapsed = end_time - start_time

with open(LOG, "a") as f:
    f.write(f"elapsed_time_seconds: {elapsed}\n")

metrics = {
    "wall_time_seconds": elapsed,
    "cpu_percent_max": cpu_max,
    "ram_mb_max": ram_max
}

with open(METRICS, "w") as f:
    json.dump(metrics, f, indent=2)

print("\nBenchmark completed")
print(json.dumps(metrics, indent=2))
