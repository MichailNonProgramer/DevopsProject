import json
import os


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "common.json")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "/config/common.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "input.lmp")


def main():
    path = CONFIG_PATH
    if not os.path.isfile(path):
        path = DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    box = cfg.get("box", [10.0, 10.0, 10.0])
    time_step = cfg.get("time_step", 0.005)
    n_steps = cfg.get("n_steps", 1000)
    epsilon = cfg.get("lj_epsilon", 1.0)
    sigma = cfg.get("lj_sigma", 1.0)
    cutoff = cfg.get("cutoff", 2.5)

    x, y, z = box
    content = f"""# Generated from config/common.json
units       lj
atom_style  atomic

# Box and atoms
region      box block 0 {x} 0 {y} 0 {z}
create_box  1 box
create_atoms 1 box

# Mass and velocities
mass        1 1.0
velocity    all create 1.44 87287

# LJ interaction
pair_style  lj/cut {cutoff}
pair_coeff  1 1 {epsilon} {sigma} {cutoff}
neighbor    0.3 bin
neigh_modify every 20 delay 0 check no

# Integration
fix         1 all nve
timestep    {time_step}
thermo      100
run         {n_steps}
"""

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()