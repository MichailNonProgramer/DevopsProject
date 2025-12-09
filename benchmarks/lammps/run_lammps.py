import subprocess
import psutil
import time
import json
import os

INPUT_FILE = "input.lmp"
OUTPUT_FILE = "log.lammps"
METRICS_FILE = "lammps_metrics.json"

# Find LAMMPS binary (you can hardcode if needed)
LAMMPS_BIN = (
    subprocess.getoutput("command -v lmp_serial || command -v lmp_stable || command -v lmp || command -v lammps")
    .strip()
)

if not LAMMPS_BIN:
    print("[ERROR] LAMMPS binary not found!")
    with open(OUTPUT_FILE, "w") as f:
        f.write("[ERROR] LAMMPS binary not found!\n")
    exit(1)

def get_total_memory(process):
    """Sum memory of process and all children in MB"""
    mem = process.memory_info().rss
    for child in process.children(recursive=True):
        try:
            mem += child.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return mem / (1024**2)

print("Running LAMMPS with monitoring...")

with open(OUTPUT_FILE, "w") as log_file:
    start_time = time.time()

    proc = subprocess.Popen(
        [LAMMPS_BIN, "-in", INPUT_FILE],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    p = psutil.Process(proc.pid)
    cpu_max = 0
    ram_max = 0

    for line in proc.stdout:
        log_file.write(line)
        log_file.flush()
        try:
            cpu = p.cpu_percent(interval=0.1)
            ram = get_total_memory(p)
            cpu_max = max(cpu_max, cpu)
            ram_max = max(ram_max, ram)
        except psutil.NoSuchProcess:
            break

    proc.wait()
    end_time = time.time()

elapsed = end_time - start_time

with open(OUTPUT_FILE, "a") as f:
    f.write(f"\nelapsed_time_seconds: {elapsed}\n")

metrics = {
    "wall_time_seconds": elapsed,
    "cpu_percent_max": cpu_max,
    "ram_mb_max": ram_max
}

with open(METRICS_FILE, "w") as f:
    json.dump(metrics, f, indent=2)

print("\nLAMMPS benchmark completed")
print(json.dumps(metrics, indent=2))
