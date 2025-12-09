import subprocess
import psutil
import time
import json
import sys
import os

def metrics(cmd, log_file):
    start_time = time.time()
    cpu_max = 0
    ram_max = 0

    with open(log_file, "w") as log:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        p = psutil.Process(proc.pid)

        for line in proc.stdout:
            log.write(line)
            try:
                cpu = p.cpu_percent(interval=0.1)
                mem = p.memory_info().rss / (1024**2)  # MB
                cpu_max = max(cpu_max, cpu)
                ram_max = max(ram_max, mem)
            except psutil.NoSuchProcess:
                break

        proc.wait()

    elapsed = time.time() - start_time

    # Append time into log
    with open(log_file, "a") as lf:
        lf.write(f"elapsed_time_seconds: {elapsed}\n")

    return {
        "wall_time_seconds": elapsed,
        "cpu_percent_max": cpu_max,
        "ram_mb_max": ram_max
    }


def main():
    if len(sys.argv) < 4:
        print("Usage: python metrics.py <output_json> <log_file> <cmd...>")
        sys.exit(1)

    output_json = sys.argv[1]
    log_file = sys.argv[2]
    cmd = sys.argv[3:]

    metrics_result = metrics(cmd, log_file)

    with open(output_json, "w") as f:
        json.dump(metrics_result, f, indent=2)

    print(json.dumps(metrics_result, indent=2))


if __name__ == "__main__":
    main()
