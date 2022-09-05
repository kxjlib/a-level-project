# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Object.py

# Object class needs to
#   - Store VAO
#   - Store Transformation Matrix

# Imports
from pyrr import Matrix44, Vector3


class Object(object):
    # Variables stored by the class
    _vao = None
    _loc_matrix = None
    shaderid = None
    _pos = [0.0, 0.0, 0.0]

    def __init__(self, vao, shaderid, location=[0.0, 0.0, 0.0]):
        # Set instance Variables
        self._vao = vao
        self.shaderid = shaderid
        self._pos = location
        if location != [0.0, 0.0, 0.0]:
            self._loc_matrix = Matrix44.from_translation(Vector3(self._pos))

    def move(self, dpos):
        self.pos = [x+y for x, y in zip(self._pos, dpos)]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._loc_matrix = Matrix44.from_translation(Vector3(self._pos))

    @property
    def mat(self):
        return self._loc_matrix

    @property
    def vao(self):
        return self._vao
