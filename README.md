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

Configure the project parameters in `config.toml`.

To change the config, edit the `load_config()` line in main.py
with the desired .toml filename.

## Simulation parameters

|  Parameter | Description                 |
|:----------:|-----------------------------|
| dt         | `float`: Time step value in seconds. |
| tracers    | `int`: Number of tracer objects    |
| trail_size | `int`: Length of a tracer's trail  |
| sigma      | `float`: Prandtl number              |
| rho        | `float`: Rayleigh number             |
| beta       | `float`: Geometric factor            |

## Rendering parameters

|    Parameter    |  Description                                                     |
|:---------------:|------------------------------------------------------------------|
| width           | `int`: Screen width                                              |
| height          | `int`: Screen height                                             |
| rotate          | `list`: [x, y, z] where each is a float. This vector represents the axis of rotation                |
| rot_speed       | `float`: Speed of rotation. Set 0.0 to turn off rotation                                             |
| fps             | `int`: FPS of saved video                                        |
| duration        | `float`: Duration of saved video                                 |
| samples         | `int`: Number of samples in MSAA (Multisampling)                 |
| preview         | `boolean`: Renders a window if true, otherwise saves to a video. |
| output_filename | `str`: Directory and filename of saved video                     |

## Theme parameters
The palette parameter contains a nested list, where each row list contains the [0, 1] normalized RGB values of tracers, which gets applied to each tracer in a circular looping fashion.

```toml
palette = [
    [0.0, 1.0, 0.5],
    [0.0, 0.8, 1.0],
    [1.0, 0.2, 0.4],
    [1.0, 0.7, 0.1]
]
```
The bg parameter takes a tuple of length 3 with RGB values normalized between 0 and 1 respectively. It changes the background color of the render.
```toml
bg = [0.1, 0.1, 0.1]
```
