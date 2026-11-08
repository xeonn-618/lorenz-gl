# lorenz-gl

A hardware-accelerated Lorenz attractor simulator written in Python using NumPy. The simulation uses moderngl, an OpenGL Python wrapper to render the simulation on the GPU and display it live in a window or even save it to a file using ffmpeg. The simulation. This project was created as a hobby project to generate video renders to use as a video wallpaper. 

# Installation

```bash
git clone https://github.com/xeonn-618/lorenz-gl.git
```

```bash
pip install -r requirements.txt
```

# Usage
To run the simulation in the window: 
```bash
python main.py
```

List of flags:

| Flag | Description |
| :------------------ | :-------------------: |
| --no-preview      |     Disable window preview; Run the simulation headless and **save** the .mp4 output.     |
| -f, --fps       |     Set the fps of the animation; only affects headless video      |
| -d, --duration       |     Video export time in seconds      |
| -o, --output     |  Target output filename when running headless

Example usage:
To render the simulation as a .mp4 video of 60 seconds at 30 fps and save to sim.mp4:
```bash
python main.py --no-preview --duration 60 --fps 30 --output "sim.mp4"
```

