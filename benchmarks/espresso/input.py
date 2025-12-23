import json
import os
import sys

import espressomd


DEFAULT_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "common.json"))
CONFIG_PATH = os.environ.get("CONFIG_PATH", "/config/common.json")


def load_config():
    path = CONFIG_PATH
    if not os.path.isfile(path):
        path = DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


cfg = load_config()
box = cfg.get("box", [10.0, 10.0, 10.0])
time_step = cfg.get("time_step", 0.01)
positions = cfg.get("positions", [[5.0, 5.0, 5.0], [6.0, 5.0, 5.0]])
epsilon = cfg.get("lj_epsilon", 1.0)
sigma = cfg.get("lj_sigma", 1.0)
cutoff = cfg.get("cutoff", 2.5)
n_steps = int(cfg.get("n_steps", 10))

system = espressomd.System(box_l=box)
system.time_step = time_step

for pos in positions:
    system.part.add(pos=pos)

system.non_bonded_inter[0, 0].lennard_jones.set_params(
    epsilon=epsilon, sigma=sigma, cutoff=cutoff, shift="auto"
)

# В актуальных версиях ESPResSo интеграторы находятся в espressomd.integrate
from espressomd import integrate

# VelocityVerlet в новой API не принимает system в конструктор,
# система уже выбрана глобально при создании espressomd.System.
integrator = integrate.VelocityVerlet()

# Чтобы не засорять лог, выводим энергию не на каждом шаге,
# а примерно 10 раз за всю траекторию + последний шаг.
print_interval = max(1, n_steps // 10)
for i in range(n_steps):
    integrator.run(1)
    if i % print_interval == 0 or i == n_steps - 1:
        print(f"step {i}", system.analysis.energy())
