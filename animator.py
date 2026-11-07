import moderngl
import moderngl_window as mglw
from tracer import TRAIL_SIZE

class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Lorenz Attractor"
    window_size = (1920, 1080)

    def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # Pass the created Window context back to the animator class
            self.animator.ctx = self.ctx

            # Tell the animator to setup the graphics pipeline
            self.animator.setup_pipeline()

    def on_render(self, time: float, frametime: float):
        # Tell Animator to run and render the scene
        self.animator.render_frame()


class Animator():
    def __init__(self, sim, fps, duration, preview=True):
        self.sim = sim
        self.duration = duration
        self.preview = preview
        self.fps = fps
        self.ctx = None

        # Initalize Frames
        self.total_frames = int(duration * fps)
        self.current_frame = 0

        # Initalize render sizes
        self.width = 1920
        self.height = 1080

        # Inject self into window as attribute 
        Window.animator = self


    def setup_pipeline(self):
        # Create the program
        self.prog = self.ctx.program(
            vertex_shader='''
            #version 330 core
            
            in vec3 aPos;
            
            uniform vec3 offset;
            
            out vec3 aColor;

            void main() {
                aColor = vec3(0.0, 1.0, 1.0);
                
                vec3 centered = aPos - vec3(0.0, 0.0, 25.0);
                vec3 normalized = vec3(centered.x / (35.0 * 1.777), centered.z / 35.0, centered.y / 35.0);
                gl_Position = vec4(normalized + offset, 1.0);
            }
            ''',
            fragment_shader="""
            #version 330 core
            
            in vec3 aColor;
            
            out vec3 fColor;
            
            void main() {
                fColor = aColor;
            }
            """)

        # Reserve VRAM for 2000 rows of 3 coordinates of 4 bytes each
        self.vbo = self.ctx.buffer(reserve=TRAIL_SIZE * 3 * 4)

        # Create the vertex array object
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '3f', 'aPos')])

        # Set offset
        self.prog['offset'].value = (0.1, 0.0, 0.0)

    def render_frame(self):
        # Update the sim
        self.sim.update()

         # Clear canvas
        self.ctx.clear(0.1, 0.1, 0.1, 1.0)

        # For each trail, write to vbo and rendef
        trails = self.sim.get_trails()
        for i, trail in enumerate(trails):
            self.vbo.write(trail.astype('f4').tobytes())
            self.vao.render(moderngl.LINE_STRIP, vertices=len(trail))

        # Increment frame
        self.current_frame += 1

    def run(self):
        # If windowed preview enabled
        if self.preview:
            # Start and run the window loop
            mglw.run_window_config(Window)

        # If not windowed preview enabled
        else:
            # Run the simulation headless
            while self.current_frame < self.total_frames:
                self.render_frame()
        
