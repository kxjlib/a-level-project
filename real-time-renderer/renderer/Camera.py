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
    _res = [800.0,600.0]
    _pos = [0.0,0.0,0.0]
    _dir = [0.0,0.0,1.0]
    _up =  [0.0,1.0,0.0]

    def __init__(self, resolution, location, pointing):
        # Generate Matrices
        self.create_loc_mat(location, pointing)
        self.resize_camera(resolution)

    def create_loc_mat(self, location, pointing):
        self._pos = location
        self._dir = pointing

        # Calculate Location Matrix
        self._loc_mat = Matrix44.look_at(
            # Location of the camera being used to view the scene
            Vector3(self._pos),
            # location plus the axis which the camera is pointing
            Vector3([i+j for i,j in zip(self._pos, self._dir)]),
            Vector3(self._up) # the axis which is deemed as 'up'
        )
    
    # Resizes the cameras view and creates a new projection matrix
    def resize_camera(self,resolution):
        self._res = resolution
        
        # Calculate Projection Matrix
        self._proj_mat = Matrix44.perspective_projection(
            70.0,  # Fov angle
            # display aspect ratio (this will nead to be changed when we change the display size)
            resolution[0] / resolution[1],
            0.1,  # near plane (how close before something stops being rendered)
            100   # far plane (how far before something stops being renderered)
        )

    # Moves The Camera
    def move(self,dpos):
        self._pos = [p+d for p,d in zip(self._pos,dpos)]
        self.create_loc_mat()

    @property
    def mv(self):
        return self._proj_mat * self._loc_mat