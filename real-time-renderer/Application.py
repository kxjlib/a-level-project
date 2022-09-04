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
from renderer.bindable.ShaderProgram import ShaderProgram
from pyrr import Matrix44, Vector3

import numpy as np
import ctypes
import pathlib
import moderngl
import sdl2

class Application(object):
    # Variables which will be used by the class
    _winst = None
    _wdim = (800,600)
    _run = False
    _ctx = None
    _shaders = {}

    def __init__(self,title,dimensions):
        self._wdim = dimensions
        # We can unpack the dimensions tuple using the * prefix
        # This saves us from doing dimensions[0] and dimensions[1]
        self._winst = GLWindow(title,*dimensions)

        # ModernGL Works by 'piggybacking' of an existing openGL context, and as such we
        # first need to create an OpenGL context in SDL before in ModernGL
        self._ctx = moderngl.create_context(version=430)

        self.view_matrix = Matrix44.perspective_projection(
            70.0,  # Fov angle
            # display aspect ratio (this will nead to be changed when we change the display size)
            800.0 / 600.0,
            0.1,  # near plane (how close before something stops being rendered)
            100   # far plane (how far before something stops being renderered)
        )

        self.look_at = Matrix44.look_at(
            # Location of the camera being used to view the scene
            Vector3([0.0, 0.0, -10.0]),
            # location plus the axis which the camera is pointing
            Vector3([0.0, 0.0, -9.0]),
            Vector3([0.0, 1.0, 0.0])  # the axis which is deemed as 'up'
        )

        self._ctx.enable_only(moderngl.NOTHING)
        self._ctx.enable(moderngl.DEPTH_TEST)

    
    # Loads all shader files into the program and stores them
    def shader_init(self):
        self._shaders['tri'] = ShaderProgram.from_filename(self._ctx, pathlib.Path(__file__).parent.resolve().as_posix() + "/assets/tri")
    
    # Initialises all models to be used
    def model_init(self):
        tri_vertices = np.array([
            # x,y,z, rgb
            0.0,  1.0,  0.0, 1.0, 0.0, 0.0,
            -1.0, -1.0,  0.0, 0.0, 1.0, 0.0,
            1.0, -1.0,  0.0, 0.0, 0.0, 1.0,
        ], dtype='f4')  # Use 4-byte (32-bit) floats

        vbo = self._ctx.buffer(tri_vertices)

        self.vao = self._ctx.vertex_array(
            self._shaders['tri'].inst,
            [
                # in_vert needs to be first 3 floats
                # in_colour needs to be the last 3
                (vbo, '3f 3f', 'in_vert', 'in_colour')
            ]
        )

    # Runs every frame - will control the render of all models
    def render(self, frames):
        self._ctx.clear(0.1, 0.1, 0.1)
        tri_loc = Matrix44.from_translation(Vector3([frames/10.0,0.0,0.0]))
        self._shaders['tri']['mvp'].write((self.view_matrix * self.look_at * tri_loc).astype('f4'))
        self.vao.render()

    # Runs every frame - will handle the logic used by the program
    def update(self):
        pass

    # Will handle all window events every frame
    def event_loop(self,e):
        while sdl2.SDL_PollEvent(ctypes.byref(e)) != 0:
            if e.type == sdl2.SDL_QUIT:
                self._run = False

    # Main entrypoint into the program, will contain the mainloop
    def run(self):
        # Program initialisation
        self.shader_init()
        self.model_init()

        event = sdl2.SDL_Event()
        frames = 0
        self._run = True
        while self._run:
            # Event Handling Loop
            self.event_loop(event)

            self.render(frames)

            # Swap window buffers (make currently rendered frame visible)
            sdl2.SDL_GL_SwapWindow(self._winst.instance)

            # Arbitrary Delay to stop excess resource usage
            sdl2.SDL_Delay(10)
            frames += 1

        
        # Stop Floating Memory after program finish
        self._ctx.release()
        sdl2.SDL_Quit()
