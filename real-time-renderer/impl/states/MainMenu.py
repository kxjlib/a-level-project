# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# MainMenu.py

from impl.states.State import State
from impl.InputManager import Input
from renderer.bindable.Object import Object
from renderer.ShaderManager import ShaderManager
from renderer.Renderer import Renderer
from renderer.Camera import Camera

import numpy as np
import moderngl


class MainMenu(State):
    def __init__(self, gl_ctx: moderngl.Context):
        super().__init__(gl_ctx)

    def model_init(self, gl_ctx: moderngl.Context):
        tri_vertices = np.array([
            # x,y texc
            -0.5, -0.5, 0.0, 0.0, # 1 5
            -0.5,  0.5, 0.0, -1.0, # 2 6
             0.5, -0.5, 1.0, 0.0, # 3
             0.5,  0.5, 1.0, -1.0, # 4
        ], dtype='f4')  # Use 4-byte (32-bit) floats

        indexes = np.array([
            0,1,2,
            1,2,3
        ], dtype='i4')

        vbo = gl_ctx.buffer(tri_vertices)
        ebo = gl_ctx.buffer(indexes)

        vao = gl_ctx.vertex_array(
            ShaderManager.shaders['UI2D'].inst,
            [
                # in_vert needs to be first 3 floats
                # in_colour needs to be the last 3
                (vbo, '2f 2f', 'in_vert', 'in_text')
            ],
            index_buffer = ebo
        )

        self.tri = Object(vao, 'UI2D')

    def update(self):
        pass

    def render(self, gl_ctx: moderngl.Context, renderer: Renderer, camera: Camera):
        gl_ctx.clear(0.1, 0.1, 0.1)
        renderer.render_ui(self.tri)
