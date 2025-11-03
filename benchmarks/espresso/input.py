import espressomd
system = espressomd.System(box_l=[10, 10, 10])
system.time_step = 0.01
system.part.add(pos=[5,5,5])
system.part.add(pos=[6,5,5])
system.non_bonded_inter[0,0].lennard_jones.set_params(epsilon=1.0, sigma=1.0, cutoff=2.5, shift="auto")

integrator = espressomd.integrator.VelocityVerlet(system)
for i in range(10):
    integrator.run(1)
    print(f"step {i}", system.analysis.energy())
