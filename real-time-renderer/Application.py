# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Application.py

# The Application class needs to:
#   - allow for the creation of a window
#   - control the window mainloop
#   - allow for us to render objects
#   - control logic for the program

# Imports
from renderer.WindowManager import GLWindow
from renderer.Camera import Camera
from renderer.Renderer import Renderer
from renderer.bindable.ShaderProgram import ShaderProgram
from renderer.bindable.Object import Object

import numpy as np
import ctypes
import pathlib
import moderngl
import sdl2

class Application(object):
    # Variables which will be used by the class
    winst = None
    wdim = (800,600)
    run = False
    ctx = None
    rnd = None
    shaders = {}
    cam = None

    def __init__(self,title,dimensions):
        self.wdim = dimensions
        # We can unpack the dimensions tuple using the * prefix
        # This saves us from doing dimensions[0] and dimensions[1]
        self.winst = GLWindow(title,*dimensions)

        # ModernGL Works by 'piggybacking' of an existing openGL context, and as such we
        # first need to create an OpenGL context in SDL before in ModernGL
        self.ctx = moderngl.create_context(version=430)

        # set OpenGL Settings
        self.ctx.enable_only(moderngl.NOTHING)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Program initialisation
        self.shader_init()
        self.model_init()

        self.rnd = Renderer(self.shaders)

        # define Camera
        self.cam = Camera(dimensions, [0.0,0.0,-10.0], [0.0,0.0,1.0])

    # Loads all shader files into the program and stores them
    def shader_init(self):
        self.shaders['tri'] = ShaderProgram.from_filename(self.ctx, \
            pathlib.Path(__file__).parent.resolve().as_posix() + "/assets/tri")
    
    # Initialises all models to be used
    def model_init(self):
        tri_vertices = np.array([
            # x,y,z, rgb
            0.0,  1.0,  0.0, 1.0, 0.0, 0.0,
            -1.0, -1.0,  0.0, 0.0, 1.0, 0.0,
            1.0, -1.0,  0.0, 0.0, 0.0, 1.0,
        ], dtype='f4')  # Use 4-byte (32-bit) floats

        vbo = self.ctx.buffer(tri_vertices)

        vao = self.ctx.vertex_array(
            self.shaders['tri'].inst,
            [
                # in_vert needs to be first 3 floats
                # in_colour needs to be the last 3
                (vbo, '3f 3f', 'in_vert', 'in_colour')
            ]
        )

        self.tri = Object(vao, 'tri')

    # Runs every frame - will control the render of all models
    def render(self, renderer):
        self.ctx.clear(0.1, 0.1, 0.1)
        renderer.render_object(self.tri,self.cam)

    # Runs every frame - will handle the logic used by the program
    def update(self):
        pass

    # Will handle all window events every frame
    def event_loop(self,e):
        while sdl2.SDL_PollEvent(ctypes.byref(e)) != 0:
            if e.type == sdl2.SDL_QUIT:
                self.run = False

    def resize_window(self, res):
        # Changes all relevant instances of the window resolution (definately should only be one)
        self.wdim = res
        self.ctx.viewport = (0,0,*res)
        self.winst.resolution = res
        self.cam.resize_camera(res)

    # Main entrypoint into the program, will contain the mainloop
    def run(self):
        event = sdl2.SDL_Event()
        self.run = True
        while self.run:
            # Event Handling Loop
            self.event_loop(event)

            # Update Loop
            self.update()

            # Render Loop
            self.render(self.rnd)

            # Swap window buffers (make currently rendered frame visible)
            sdl2.SDL_GL_SwapWindow(self.winst.instance)

            # Arbitrary Delay to stop excess resource usage
            sdl2.SDL_Delay(10)

        
        # Stop Floating Memory after program finish
        self.ctx.release()
        sdl2.SDL_Quit()