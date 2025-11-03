import subprocess
import os
import sys
import json
from datetime import datetime

SIMS = {
    "lammps": {
        "workdir": "benchmarks/lammps",
        "run_script": "run.sh",
        "log": "log.lammps"
    },
    "gromacs": {
        "workdir": "benchmarks/gromacs",
        "run_script": "run.sh",
        "log": "gromacs.log"
    },
    "espresso": {
        "workdir": "benchmarks/espresso",
        "run_script": "run.sh",
        "log": "espresso.log"
    }
}

RESULTS_DIR = "results"
METRICS_SCRIPT = "scripts/metrics.py"

def run_sim(name, sim):
    print(f"\n===== RUN {name.upper()} =====")
    wd = sim["workdir"]
    out = subprocess.run(["bash", sim["run_script"]], cwd=wd)
    log_path = os.path.join(wd, sim["log"])
    out_json = os.path.join(RESULTS_DIR, f"{name}.json")
    subprocess.run([sys.executable, METRICS_SCRIPT, log_path, out_json])
    print(f"Metrics saved to {out_json}")

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    sims = sys.argv[1:] if len(sys.argv) > 1 else list(SIMS.keys())
    for sim_name in sims:
        run_sim(sim_name, SIMS[sim_name])
    # Итоговый сводный файл
    summary = {}
    for sim_name in sims:
        json_path = os.path.join(RESULTS_DIR, f"{sim_name}.json")
        if os.path.exists(json_path):
            with open(json_path) as f:
                summary[sim_name] = json.load(f)
    summary_path = os.path.join(RESULTS_DIR, "benchmark_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written to {summary_path}")

if __name__ == "__main__":
    main()
