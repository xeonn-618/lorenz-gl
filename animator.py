import moderngl
import moderngl_window as mglw
from tracer import TRAIL_SIZE
import glm

# Trail_colors = [
#     (0.172, 0.145, 0.960), # Dark Blue
#     (0.521, 0.654, 1.000), # Light Blue
#     (0.949, 0.419, 0.745), # Light Pink
#     (0.929, 0.000, 0.572) # Hot Pink
# ]

Trail_colors = [
    (0.000, 1.000, 0.000), # Neon Green
    (0.000, 0.000, 1.000), # Dark Green
]

class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Lorenz Attractor"
    window_size = (1920, 1080)

    # 16x MSAA
    samples = 16

    def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # Pass the created Window context back to the animator class
            self.animator.ctx = self.ctx

            # Tell the animator to setup the graphics pipeline
            self.animator.setup_pipeline()

    def on_render(self, time: float, frametime: float):
        # Tell Animator to run and render the scene
        self.animator.render_frame(time)


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
            uniform mat4 transform;
            uniform int trail_len;

            out float v_alpha;
            out vec3 v_pos;
            
            void main() {
                v_alpha = float(gl_VertexID) / max(float(trail_len - 1), 1.0);
                
                vec3 centered = aPos - vec3(0.0, 0.0, 25.0);
                vec3 normalized = vec3(centered.x / (35.0 * 1.777), centered.z / 35.0, centered.y / 35.0);
                gl_Position = transform * vec4(normalized + offset, 1.0);
                v_pos = gl_Position.xyz;
            }
            ''',
            fragment_shader="""
            #version 330 core
            
            in float v_alpha;
            in vec3 v_pos;

            uniform vec3 uColor;
            
            out vec4 fColor;
            
            void main() {
                float depth = clamp((30.0 - v_pos.y) / 60.0, 0.2, 1.0);

                float depthIntensity = pow(depth, 1.1);

                vec3 litColor = uColor * depthIntensity;
                fColor = vec4(litColor * v_alpha, v_alpha);
            }
            """)

        # Reserve VRAM for 2000 rows of 3 coordinates of 4 bytes each
        self.vbo = self.ctx.buffer(reserve=TRAIL_SIZE * 3 * 4)

        # Create the vertex array object
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '3f', 'aPos')])

        # Modify line width
        self.ctx.line_width = 1.5

        # Enable blending with background
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.ONE, moderngl.ONE)

        # Enable mutlisampling
        self.ctx.multisample = True

        # Set offset
        self.prog['offset'].value = (0.0, 0.0, 0.0)

        # Create transformation matrix
        trans = glm.mat4(1.0)
        trans = glm.rotate(trans, 1, glm.vec3(0.5, 0.5, 0.0))
        self.prog['transform'].write(trans.to_bytes())

    def render_frame(self, time: float):
        # Update the sim
        self.sim.update()

         # Clear canvas
        self.ctx.clear(0.1, 0.1, 0.1, 1.0)

        # For each trail, write to vbo and rendef
        trails = self.sim.get_trails()
        for i, trail in enumerate(trails):
            # Write trail color
            uColor = Trail_colors[i % len(Trail_colors)]
            self.prog['uColor'].value = uColor

            # Send verticies len
            self.prog['trail_len'].value = len(trail)

            # Write to vbo and render
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
        
