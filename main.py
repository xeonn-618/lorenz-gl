import argparse
import sys
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

def parse_args():
    parser = argparse.ArgumentParser(
        prog="lorenz-gl",
        description="A Hardware-accelerated Lorenz Attractor simulation running on OpenGL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Preview toggle
    parser.add_argument("--preview", action=argparse.BooleanOptionalAction, default=True, help="Preview the simulation in a window")

    # Render & Export settings
    parser.add_argument(
        "-f", "--fps",
        type=int,
        default=60,
        help="Frames per second for window / exported video."
    )
    parser.add_argument(
        "-d", "--duration",
        type=float,
        default=10.0,
        help="Total duration in seconds to run/render."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="outputs/lorenz_export.mp4",
        help="Target output filename when running headless."
    )

    return parser.parse_args()

def main():
    args = parse_args()
    # Run the simulation
    anim = Animator(simulator, args.fps, args.duration, args.preview, output_filename=args.output)
    anim.run()


if __name__ == "__main__":
    main()