# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Camera.py

# The Camera class needs to:
#   - Be able to mvoe around
#   - Calculate a new view matrix based on a change in resolution

# Imports
from pyrr import Matrix44, Vector3

class Camera(object):
    # Define variables we'll be using during the class
    _proj_mat = None
    _loc_mat = None
    _pos = [0.0,0.0,0.0]
    _dir = [0.0,0.0,1.0]
    _up = [0.0,1.0,0.0]

    def __init__(self, resolution, location, pointing):
        # Calculate Projection Matrix
        self._proj_mat = Matrix44.perspective_projection(
            70.0,  # Fov angle
            # display aspect ratio (this will nead to be changed when we change the display size)
            800.0 / 600.0,
            0.1,  # near plane (how close before something stops being rendered)
            100   # far plane (how far before something stops being renderered)
        )

        # Generate Location Matrix
        self.create_loc_mat(location, pointing)

        self._loc_mat = Matrix44.look_at(
            # Location of the camera being used to view the scene
            Vector3([0.0, 0.0, -10.0]),
            # location plus the axis which the camera is pointing
            Vector3([0.0, 0.0, -9.0]),
            Vector3([0.0, 1.0, 0.0])  # the axis which is deemed as 'up'
        )

    
    def create_loc_mat(self, location, pointing):
        self._pos = location
        self._dir = pointing

        # Calculate Location Matrix
        self._loc_mat = Matrix44.look_at(
            # Location of the camera being used to view the scene
            Vector3([0.0, 0.0, -10.0]),
            # location plus the axis which the camera is pointing
            Vector3([0.0, 0.0, -9.0]),
            Vector3([0.0, 1.0, 0.0])  # the axis which is deemed as 'up'
        )

    @property
    def mv(self):
        return self._loc_mat * self._proj_mat