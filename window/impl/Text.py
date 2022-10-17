# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Text.py

# This class needs to:
#   - Create text surface using sdl2
#   - Render text to a moderngl texture
#   - Store Texture in TextureManager
#   - Give the Text a Quad

import moderngl
import sdl2
import sdl2.sdlttf
import sdl2.ext
import pathlib
from ..renderer.ShaderManager import ShaderManager
from .InformationManager import Info
from ..renderer.TextureManager import TextureManager
import numpy as np


class Text(object):
    contents = ""
    text_name = ""
    pos = [0, 0]
    active = True
    size = (0,0)

    def __init__(self, gl_ctx: moderngl.Context, contents, colour, size, text_name, x, y):
        self.contents = contents
        self.text_name = text_name
        self.pos = (x, y)

        font = sdl2.sdlttf.TTF_OpenFont((pathlib.Path(
            __file__).parent.resolve().as_posix() + f"/../assets/calibri.ttf").encode(), size)

        surface = sdl2.sdlttf.TTF_RenderText_Blended(
            font, contents.encode(), sdl2.SDL_Color(*colour))

        sdl2.SDL_LockSurface(surface)

        surf = surface.contents

        pixels = sdl2.ext.surface_to_ndarray(surface)

        tex = gl_ctx.texture((surf.w, surf.h), 4, pixels)
        TextureManager.from_tex(tex, text_name)

        width = surf.w / Info.scr_size[0]
        height = surf.h / Info.scr_size[1]

        self.size = (width,height)

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

        sdl2.SDL_FreeSurface(surface)

    def render(self):
        if not self.active:
            return
        TextureManager.use(self.text_name)
        self.vao.render()
