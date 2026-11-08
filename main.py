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
    cfg = load_config("presets/phosphor.toml")


    # Create simulator universe
    simulator = Simulator(cfg['simulation'])

    # Create tracers
    simulator.create_tracers(cfg['simulation']['tracers'])
    
    # Run the simulation
    anim = Animator(simulator, cfg)
    anim.run()


if __name__ == "__main__":
    main()