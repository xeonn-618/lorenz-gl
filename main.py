import argparse
import tomllib
from pathlib import Path
import sys
from simulator import Simulator
from animator import Animator

def load_config(config_path="config.toml") -> dict:
    with open(config_path, 'rb') as f:
        return tomllib.load(f)

def main():
    cfg = load_config("config.toml")


    # Create simulator universe
    simulator = Simulator(cfg['simulation'])

    # Add initial tracer
    simulator.add_tracer(0.0, 1.0, 1.0)
    simulator.add_tracer(0.0, 1.0, 0.0)
    simulator.add_tracer(0.0, 0.0, 1.0)
    simulator.add_tracer(1.0, 0.0, 1.0)
    simulator.add_tracer(1.0, 0.0, 0.0)

    # Run the simulation
    anim = Animator(simulator, cfg)
    anim.run()


if __name__ == "__main__":
    main()