import sys
import re
import os
import json

def parse_time(log):
    matches = re.findall(r"elapsed_time_seconds:\s*([0-9.]+)", log)
    if matches:
        return float(matches[-1])
    return None

def parse_cpu_mem(log):
    # Placeholder: расширить при необходимости для сбора из топа
    return None, None

def main():
    if len(sys.argv) < 3:
        print("Usage: python metrics.py <log_file> <output_json>")
        sys.exit(1)
    log_file, output_json = sys.argv[1], sys.argv[2]
    with open(log_file, 'r') as f:
        log = f.read()
    wall_time = parse_time(log)
    cpu, mem = parse_cpu_mem(log)
    data = {
        "wall_time_seconds": wall_time,
        "cpu_percent_max": cpu,
        "ram_mb_max": mem
    }
    with open(output_json, 'w') as f:
        json.dump(data, f, indent=2)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
