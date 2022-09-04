# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Renderer.py

# The Renderer Class needs to:
#   - Render any model class it is given
#   - Control Deltatime

from renderer.bindable.Object import Object
from renderer.Camera import Camera
from pyrr import Matrix44, Vector3

class Renderer(object):
    # Variables used by class
    _shaders = {}
    _no_move = Matrix44.from_translation(Vector3([0.0,0.0,0.0]))

    def __init__(self, shaders):
        self._shaders = shaders

    def render_object(self, obj:Object, camera:Camera):
        mat_transform = self._no_move
        if obj.pos != [0,0,0]:
            mat_transform = obj.mat
        
        self._shaders[obj.shaderid]['mvp'].write((camera.mv * mat_transform).astype('f4'))
        obj.vao.render()