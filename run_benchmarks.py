import os
import sys
import runpy

# Переходим в корневую директорию проекта
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Запускаем runner.py с корректной кодировкой через runpy (UTF-8 по умолчанию)
sys.path.insert(0, script_dir)
runner_path = os.path.join(script_dir, "scripts", "runner.py")
runpy.run_path(runner_path, run_name="__main__")

