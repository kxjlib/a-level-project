# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Button.py

# Import
import numpy as np
import moderngl
from renderer.ShaderManager import ShaderManager
from renderer.TextureManager import TextureManager
from impl.InputManager import Input


class Button(object):
    # Variables used by the instance
    tex_id = ""
    vao = None
    size = [0, 0]
    pos = [0, 0]
    active = True

    def __init__(self, gl_ctx: moderngl.Context, texture_id, width, height, x, y):
        self.size = [width, height]
        self.pos = [x, y]
        self.tex_id = texture_id

        self.create_vao(gl_ctx)

    def create_vao(self, gl_ctx: moderngl.Context):
        width, height = self.size
        x, y = self.pos

        vertices = np.array([
            # x,y texc
            x - width/2, y - height/2, 0.0,  0.0,  # 1 5
            x - width/2, y + height/2, 0.0, -1.0,  # 2 6
            x + width/2, y - height/2, 1.0,  0.0,  # 3
            x + width/2, y + height/2, 1.0, -1.0,  # 4
        ], dtype='f4')  # Use 4-byte (32-bit) floats

        indices = np.array([
            0, 1, 2,
            1, 2, 3
        ], dtype='i4')

        vbo = gl_ctx.buffer(vertices)
        ebo = gl_ctx.buffer(indices)

        self.vao = gl_ctx.vertex_array(
            ShaderManager.shaders['UI2D'].inst,
            [
                # in_vert needs to be first 3 floats
                # in_colour needs to be the last 3
                (vbo, '2f 2f', 'in_vert', 'in_text')
            ],
            index_buffer=ebo
        )

    def is_clicked(self):
        mouse_pos = Input.mouse_to_screen()
        x, y = self.pos
        w, h = self.size
        if x - w/2 <= mouse_pos[0] <= x + w/2 and y - h/2 <= mouse_pos[1] <= y + h/2:
            return Input.MPressed.get(1) and not Input.lMPressed.get(1)
        return False

    def render(self):
        if not self.active:
            return
        TextureManager.use(self.tex_id)
        self.vao.render()
