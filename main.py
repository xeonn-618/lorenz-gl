from simulator import Simulator

# Lorenz Attractor parameters

sigma = 10.0
rho = 28.0
beta = 8.0/3.0

# Initalize simulator
dt = 0.001
simulator = Simulator(sigma, rho, beta, dt=dt)

# Add initial tracer
simulator.add_tracer(0.0, 1.0, 1.0)

# Run the simulation
steps = 20000

while True:
    simulator.update()
    # Break the loop after a certain number of iterations
    if simulator.time > dt*steps - dt:
        break