import sys
import re
import os
import json


def parse_time(log: str):
    matches = re.findall(r"elapsed_time_seconds:\s*([0-9.]+)", log)
    if matches:
        return float(matches[-1])

    m = re.search(r"Wall clock time \(h:mm:ss or m:ss\):\s*([0-9:]+)", log)
    if m:
        t = m.group(1)
        parts = [float(p) for p in t.split(":")]
        if len(parts) == 3:
            h, m_, s = parts
            return h * 3600 + m_ * 60 + s
        if len(parts) == 2:
            m_, s = parts
            return m_ * 60 + s
    return None


def parse_cpu_mem(log: str):
    cpu_percent = None
    ram_mb_max = None

    m_cpu = re.search(r"Percent of CPU this job got:\s*([0-9.]+)%", log)
    if m_cpu:
        cpu_percent = float(m_cpu.group(1))

    m_mem = re.search(r"Maximum resident set size \(kbytes\):\s*([0-9]+)", log)
    if m_mem:
        kb = float(m_mem.group(1))
        ram_mb_max = kb / 1024.0

    return cpu_percent, ram_mb_max


def main():
    if len(sys.argv) < 3:
        print("Usage: python metrics.py <log_file> <output_json>")
        sys.exit(1)
    log_file, output_json = sys.argv[1], sys.argv[2]
    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
        log = f.read()
    wall_time = parse_time(log)
    cpu, mem = parse_cpu_mem(log)
    data = {
        "wall_time_seconds": wall_time,
        "cpu_percent_max": cpu,
        "ram_mb_max": mem,
    }
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
