# MD-Benchmark: автоматизация DevOps-бенчмаркинга молекулярной динамики

## О проекте

Автоматизированный запуск и сравнение производительности симуляторов молекулярной динамики (LAMMPS, GROMACS, ESPResSo) на минимальных примерах клеточных мембран. Метрики: время выполнения (wall time), использование CPU, RAM, результат — JSON-отчёт. Всё работает в Docker и легко расширяется.

## Структура проекта
```
benchmarks/
  lammps/      # пример LAMMPS: input.lmp, run.sh
  gromacs/     # пример GROMACS: input.tpr (placeholder), run.sh
  espresso/    # пример ESPResSo: input.py, run.sh
results/       # логи и json с метриками
scripts/       # metrics.py (сбор метрик), runner.py (автоматизация)
docker/        # Dockerfiles для симуляторов
README.md      # этот файл
```

---
## Быстрый старт (любая ОС, нужен Docker и Python >=3.7 для runner.py)

### 1. Install required packages for runner.py to work correcly
```bash
  pip install psutil
```

### 1. Сборка Docker-образа
- LAMMPS:
  ```bash
  docker build -f docker/lammps.Dockerfile -t lammps-bench .
  ```
- GROMACS:
  ```bash
  docker build -f docker/gromacs.Dockerfile -t gromacs-bench .
  ```
- ESPResSo:
  ```bash
  docker build -f docker/espresso.Dockerfile -t espresso-bench .
  ```

### 2. Автоматизация запусков и сбор результатов
Можно запускать все benchmarks подряд и собирать метрики:
```bash
python scripts/runner.py          # Запуск всех симуляторов + сбор метрик
python scripts/runner.py lammps   # Запуск только lammps
```
В папке `results/` появится json-отчет по каждому симулятору и общий benchmark_summary.json.

## Как добавить новый симулятор?
1. Создайте папку в `benchmarks/NEWNAME/`
2. Напишите входной пример, run.sh с аналогичной обёрткой по времени.
3. Создайте Dockerfile в docker/NEWNAME.Dockerfile.
4. Добавьте описание в README.md.
5. (Опционально) расширьте scripts/runner.py, если структура иначе.

## Интерпретация результатов
Метрики будут в json-файле, пример:
```json
{
  "lammps": { "wall_time_seconds": 3.04, "cpu_percent_max": null, "ram_mb_max": null },
  "gromacs": { "wall_time_seconds": 12.55, "cpu_percent_max": 109.7, "ram_mb_max": 115.88 },
  ...
}
```
- `wall_time_seconds` — время выполнения от запуска до окончания симуляции
- `cpu_percent_max` — maximum CPU usage during simulation
- `ram_mb_max` — maximum RAM usage in MB


## FAQ
- **Q:** Можно ли запускать вручную из-под Windows?  
  **A:** Да, если установлен bash и все зависимости. Но проще и надёжнее — использовать Docker.
- **Q:** Как генерировать input.tpr для GROMACS?
  **A:** Необходимо подготовить .gro/.top/.mdp и собрать tpr через gmx grompp (см. оф. инструкции GROMACS).
- **Q:** How to get CPU/RAM metrics?
  **A:** CPU and RAM monitoring is now implemented via psutil.

---
Проект открыт для pull request и пожеланий!
