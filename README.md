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
  "gromacs": { "wall_time_seconds": 2.21, ...},
  ...
}
```
- `wall_time_seconds` — время выполнения от запуска до окончания симуляции
- `cpu_percent_max`, `ram_mb_max` пока не реализованы (можно добавить через расширение metrics.py)

## FAQ
- **Q:** Можно ли запускать вручную из-под Windows?  
  **A:** Да, если установлен bash и все зависимости. Но проще и надёжнее — использовать Docker.
- **Q:** Как генерировать input.tpr для GROMACS?
  **A:** Необходимо подготовить .gro/.top/.mdp и собрать tpr через gmx grompp (см. оф. инструкции GROMACS).
- **Q:** Как сделать метрики по CPU/RAM?
  **A:** Добавьте соответствующий код в scripts/metrics.py (например, через psutil, top, time -v …).

---
Проект открыт для pull request и пожеланий!
