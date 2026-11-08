from simulator import Simulator
from animator import Animator

# Lorenz Attractor parameters

sigma = 10.0
rho = 28.0
beta = 8.0/3.0

# Initalize simulator
dt = 0.005
simulator = Simulator(sigma, rho, beta, dt=dt)

# Add initial tracer
simulator.add_tracer(0.0, 1.0, 1.0)
simulator.add_tracer(0.0, 1.0, 0.0)
simulator.add_tracer(0.0, 0.0, 1.0)
simulator.add_tracer(1.0, 0.0, 1.0)
simulator.add_tracer(1.0, 0.0, 0.0)

# Run the simulation
anim = Animator(simulator, 60, 10, False)
anim.run()