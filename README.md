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
## Общий конфиг входных данных

Все симуляторы используют единый конфиг `config/common.json`. Меняя его, вы синхронно обновляете входные данные для LAMMPS, GROMACS и ESPResSo.

Пример `config/common.json`:
```
{
  "description": "Общий конфиг для минимальных LJ-систем в LAMMPS, GROMACS и ESPResSo",
  "box": [10.0, 10.0, 10.0],
  "time_step": 0.01,
  "n_steps": 1000,
  "lj_epsilon": 1.0,
  "lj_sigma": 1.0,
  "cutoff": 2.5,
  "positions": [
    [5.0, 5.0, 5.0],
    [6.0, 5.0, 5.0]
  ]
}
```

Как применяется:
- **LAMMPS**: `benchmarks/lammps/generate_input.py` генерирует `input.lmp` из `common.json` при старте `run.sh`.
- **GROMACS**: `benchmarks/gromacs/generate_input.py` генерирует `input.gro`, `input.top`, `input.mdp`, далее `gmx grompp` → `input.tpr`; все параметры берутся из `common.json`.
- **ESPResSo**: `benchmarks/espresso/input.py` читает `common.json` напрямую.

Пути внутри контейнеров:
- При запуске через `scripts/runner.py` конфиг монтируется как `/config/common.json` (read-only).
- Скрипты ищут конфиг сначала в `/config/common.json`, затем fallback в локальном `../config/common.json`.

Единицы:
- В GROMACS координаты/бокс трактуются как нанометры. В LAMMPS и ESPResSo сейчас используются те же численные значения без пересчёта. При необходимости строгой конверсии добавьте масштабирование в генераторы.

---
## Быстрый старт (любая ОС, нужен Docker и Python >=3.7 для runner.py)

### 1. Сборка Docker-образа и запуск
- LAMMPS:
  ```bash
  docker build -f docker/lammps.Dockerfile -t lammps-bench .
  docker run --rm lammps-bench
  ```
- GROMACS:
  ```bash
  docker build -f docker/gromacs.Dockerfile -t gromacs-bench .
  docker run --rm gromacs-bench
  ```
- ESPResSo:
  ```bash
  docker build -f docker/espresso.Dockerfile -t espresso-bench .
  docker run --rm espresso-bench
  ```

### 2. Автоматизация запусков и сбор результатов
Можно запускать все benchmarks подряд и собирать метрики (wall time, CPU, RAM):
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
  "lammps": { "wall_time_seconds": 3.04, "cpu_percent_max": 392.0, "ram_mb_max": 512.3 },
  "gromacs": { "wall_time_seconds": 2.21, ...},
  ...
}
```
- `wall_time_seconds` — время выполнения от запуска до окончания симуляции (секунды). Берётся из обёртки в `run.sh` (ручной замер) или из `Wall clock time` `/usr/bin/time -v`.
- `cpu_percent_max` — максимальный процент CPU, который получил процесс (может быть >100% при многопоточности). Парсится из строки `Percent of CPU this job got` в выводе `/usr/bin/time -v`.
- `ram_mb_max` — пиковое использование RAM в мегабайтах. Парсится из строки `Maximum resident set size (kbytes)` в выводе `/usr/bin/time -v` и переводится из KB в MB.

## FAQ
- **Q:** Можно ли запускать вручную из-под Windows?  
  **A:** Да, если установлен bash и все зависимости. Но проще и надёжнее — использовать Docker.
- **Q:** Как генерировать input.tpr для GROMACS?
  **A:** Необходимо подготовить .gro/.top/.mdp и собрать tpr через gmx grompp (см. оф. инструкции GROMACS).
- **Q:** Как сделать метрики по CPU/RAM?
  **A:** Добавьте соответствующий код в scripts/metrics.py (например, через psutil, top, time -v …).

---
Проект открыт для pull request и пожеланий!
