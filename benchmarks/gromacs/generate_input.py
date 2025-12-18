import json
import os
from textwrap import dedent


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.abspath(os.path.join(HERE, "..", "..", "config", "common.json"))
CONFIG_PATH = os.environ.get("CONFIG_PATH", "/config/common.json")


def load_config():
    path = CONFIG_PATH
    if not os.path.isfile(path):
        path = DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_gro(cfg):
    """Пишем простой .gro с атомами из positions и размерами box (nm)."""
    box = cfg.get("box", [3.0, 3.0, 3.0])
    positions = cfg.get("positions", [[1.0, 1.0, 1.0]])

    lines = ["Generated from config/common.json", f"{len(positions):5d}"]
    for i, pos in enumerate(positions, start=1):
        # формат GRO: resnr(5) resname(5) atomname(5, right) atomnr(5) x y z
        # Совмещаем с top: resname LJ, atomnames LJ1, LJ2, ...
        atomname = f"LJ{i}"
        lines.append(f"{1:5d}{'LJ':>5}{atomname:>5}{i:5d}{pos[0]:8.3f}{pos[1]:8.3f}{pos[2]:8.3f}")
    lines.append(f"{box[0]:10.5f}{box[1]:10.5f}{box[2]:10.5f}")

    with open(os.path.join(HERE, "input.gro"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_top(cfg):
    """Минимальный топ-файл с одним типом LJ-частиц (масса=1)."""
    sigma = cfg.get("lj_sigma", 1.0)
    epsilon = cfg.get("lj_epsilon", 1.0)
    positions = cfg.get("positions", [[1.0, 1.0, 1.0]])

    content = dedent(
        f"""
        ; Generated from config/common.json
        [ defaults ]
        ; nbfunc  comb-rule  gen-pairs  fudgeLJ  fudgeQQ
        1        2          yes        1.0      1.0

        [ atomtypes ]
        ; name   mass    charge  ptype  sigma   epsilon
        LJ      1.0     0.0     A      {sigma}  {epsilon}

        [ moleculetype ]
        ; name  nrexcl
        LJBOX  1

        [ atoms ]
        ; nr  type  resnr  resname  atom  cgnr  charge  mass
        """
    ).strip() + "\n"

    atom_lines = []
    for i in range(len(positions)):
        atom_lines.append(f"{i+1:5d}  LJ    1   LJ    LJ{i+1:<3d}  {i+1:5d}  0.0   1.0")

    footer = dedent(
        """
        [ system ]
        LJ box

        [ molecules ]
        LJBOX  1
        """
    ).strip() + "\n"

    with open(os.path.join(HERE, "input.top"), "w", encoding="utf-8") as f:
        f.write(content + "\n".join(atom_lines) + "\n" + footer)


def write_mdp(cfg):
    """Минимальный mdp для NVE (без термостата/баростата)."""
    dt = cfg.get("time_step", 0.001)
    nsteps = cfg.get("n_steps", 1000)
    cutoff = cfg.get("cutoff", 1.0)

    mdp = dedent(
        f"""
        ; Generated from config/common.json
        integrator    = md
        dt            = {dt}
        nsteps        = {nsteps}

        nstxout       = 0
        nstvout       = 0
        nstenergy     = 100
        nstlog        = 100

        cutoff-scheme = Verlet
        rlist         = {cutoff}
        rcoulomb      = {cutoff}
        rvdw          = {cutoff}
        coulombtype   = Cut-off
        vdwtype       = Cut-off

        constraints   = none
        tcoupl        = no
        pcoupl        = no
        pbc           = xyz
        """
    ).strip() + "\n"

    with open(os.path.join(HERE, "input.mdp"), "w", encoding="utf-8") as f:
        f.write(mdp)


def main():
    cfg = load_config()
    write_gro(cfg)
    write_top(cfg)
    write_mdp(cfg)


if __name__ == "__main__":
    main()

