import json
import os

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

system = espressomd.System(box_l=box)
system.time_step = time_step

for pos in positions:
    system.part.add(pos=pos)

system.non_bonded_inter[0, 0].lennard_jones.set_params(
    epsilon=epsilon, sigma=sigma, cutoff=cutoff, shift="auto"
)

integrator = espressomd.integrator.VelocityVerlet(system)
for i in range(cfg.get("n_steps", 10)):
    integrator.run(1)
    print(f"step {i}", system.analysis.energy())
