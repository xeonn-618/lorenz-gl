import numpy as np

RING_BUFFER = 2000

class Tracer():
    def __init__(self, sigma, rho, beta, x, y, z):

        # Lorenz Parameters
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        
        # Initalize time
        self.t = 0

       # Initialize the tracer
        self.tracer = np.array([x, y, z], dtype=np.float64)

        # Keep coordinate history in ring buffer (N, 3)
        self.history = np.zeros(shape=(RING_BUFFER, 3), dtype=np.float64)

        # Initialize ring buffer head position
        self.head = 0

        # Counters for trail tracking
        self.count = 0

    def update(self, dt):
        x, y, z = self.tracer

        # Calculate the derivatives
        dx_dt = self.sigma * (y - x)
        dy_dt = x * (self.rho - z) - y
        dz_dt = (x * y) - (self.beta * z)

        # Update the positions
        self.tracer += np.array([dx_dt*dt, dy_dt*dt, dz_dt*dt], dtype=np.float64)

        # Update history
        #   - Overwrite current head position
        self.history[self.head, :] = self.tracer

        #   - Increment head position
        self.head = (self.head + 1) % RING_BUFFER
        self.count += 1

        # Update time
        self.t += dt

    def get_trail(self):

        if self.count <= RING_BUFFER:
            # [Start -> Head-1] | Head part writing over zeros
            a1 = self.history[:self.head, :]

            # [Head -> End]   | Unwritten zeros
            a2 = self.history[self.head:, :]

            return np.vstack((a1, a2))

        else:
            # [Start -> Head-1] | New part head is overwriting
            a1 = self.history[:self.head, :]

            # [Head -> End]   | Old part being overwritten
            a2 = self.history[self.head:, :]

            return np.vstack((a2, a1))
