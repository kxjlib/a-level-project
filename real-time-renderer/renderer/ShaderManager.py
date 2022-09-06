# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# ShaderManager.py

from renderer.bindable.ShaderProgram import ShaderProgram
import moderngl
import pathlib

class ShaderManager(object):
    shaders = {}

    @classmethod
    def from_dict(cls, gl_ctx: moderngl.Context, shaders):
        for k, v in shaders.items():
            cls.shaders[k] = ShaderProgram. \
                from_filename(gl_ctx,
                              pathlib.Path(__file__)
                              .parent.resolve()
                              .as_posix()
                              + f"/../assets/shaders/{v}")