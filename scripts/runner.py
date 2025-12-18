import subprocess
import os
import sys
import json
from datetime import datetime

SIMS = {
    "lammps": {
        "workdir": "benchmarks/lammps",
        "run_script": "run.sh",
        "log": "log.lammps",
        "docker_image": "lammps-bench"
    },
    "gromacs": {
        "workdir": "benchmarks/gromacs",
        "run_script": "run.sh",
        "log": "gromacs.log",
        "docker_image": "gromacs-bench"
    },
    "espresso": {
        "workdir": "benchmarks/espresso",
        "run_script": "run.sh",
        "log": "espresso.log",
        "docker_image": "espresso-bench"
    }
}

RESULTS_DIR = "results"
METRICS_SCRIPT = "scripts/metrics.py"

def run_sim(name, sim):
    print(f"\n===== RUN {name.upper()} =====")
    wd = sim["workdir"]
    docker_image = sim["docker_image"]
    
    # Получаем абсолютный путь к benchmarks директории
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    workdir_abs = os.path.join(project_root, wd)
    config_path = os.path.join(project_root, "config")
    
    # Запускаем Docker контейнер с монтированием benchmarks директории
    # Используем --rm для автоматического удаления контейнера после выполнения
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{workdir_abs}:/workspace",
        "-v", f"{config_path}:/config:ro",
        "-w", "/workspace",
        docker_image,
        "bash", "-lc",
        # Нормализуем CRLF -> LF внутри контейнера и только потом запускаем скрипт
        "sed -i 's/\\r$//' run.sh && bash run.sh"
    ]
    
    print(f"Running: {' '.join(docker_cmd)}")
    out = subprocess.run(docker_cmd)
    
    log_path = os.path.join(wd, sim["log"])
    out_json = os.path.join(RESULTS_DIR, f"{name}.json")
    
    if os.path.exists(log_path):
        subprocess.run([sys.executable, METRICS_SCRIPT, log_path, out_json])
        print(f"Metrics saved to {out_json}")
    else:
        print(f"Warning: Log file {log_path} not found!")

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
