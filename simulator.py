import numpy as np
from tracer import Tracer

class Simulator():
    def __init__(self, sim_cfg: dict):

        # Universe Lorenz Parameters
        self.sigma = sim_cfg['sigma']
        self.rho = sim_cfg['rho']
        self.beta = sim_cfg['beta']
        self.trail_size = sim_cfg['trail_size']


        # Time 
        self.time = 0.0
        self.dt = sim_cfg['dt']

        # Tracer Object Storage
        self.tracers = []


    def add_tracer(self, x, y, z):

        # Create and add new tracer 
        new_tracer  = Tracer(self.sigma, self.rho, self.beta, x, y, z, self.trail_size)
        self.tracers.append(new_tracer)

    def get_trails(self):
        """ Return all the tracers' trails in a list
        [tracer1_arr, tracer2_arr, ...]"""
        
        trails = []
        for tracer in self.tracers:
            trails.append(tracer.get_trail())
        
        return trails

    def update(self):

        # DEBUG
        # print(f' TIME : {self.time:.3f}')

        # Update all tracers
        for tracer in self.tracers:
            tracer.update(self.dt)

        # Update clock
        self.time += self.dt


