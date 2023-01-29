# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Renderer.py

# The Renderer Class needs to:
#   - Render any model class it is given
#   - Control Deltatime

from .bindable.Object import Object
from .Camera import Camera
from pyrr import Matrix44, Vector3

from .ShaderManager import ShaderManager

class Renderer(object):
    # Variables used by class
    _no_move = Matrix44.from_translation(Vector3([0.0, 0.0, 0.0]))

    def __init__(self):
        pass

    def render_object(self, obj: Object, camera: Camera):
        mat_transform = self._no_move
        if obj.pos != [0, 0, 0]:
            mat_transform = obj.mat

        ShaderManager.shaders[obj.shaderid]['mvp'].write(
            (camera.mv * mat_transform).astype('f4'))
        obj.vao.render()
    
    def render_ui(self, obj: Object):
        obj.vao.render()
