# William Davies
# "Flight Fidelity" Project
# Model Analysis
# Mesh3D.py

# 3D Mesh handling class
#   - needs to open a model file from filename
#   - needs to encapsulate analysis functions
#   - not to be confused with future? glider class in simulation

# Imports
import pywavefront # Will allow us to get all vertex information about the triangle.

class Mesh3D:
    def __init__(self, filename):
        self.model = self.from_filename(filename)
        self.density = 30 # 30 KG/M^3

    def from_filename(self,filename) -> pywavefront.Wavefront:
        model = pywavefront.Wavefront(filename,collect_faces=True)
        self.vertices = model.vertices
        self.faces = model.mesh_list[0].faces
        self.volume = self.calc_volume()
        return model

    def calc_volume(self):
        # Uses answer by Frank Krueger on SOverflow Q 1406029
        def signed_vol_tri(p1,p2,p3):
            v321 = p3[0]*p2[1]*p1[2]
            v231 = p2[0]*p3[1]*p1[2]
            v312 = p3[0]*p1[1]*p2[2]
            v132 = p1[0]*p3[1]*p2[2]
            v213 = p2[0]*p1[1]*p3[2]
            v123 = p1[0]*p2[1]*p3[2]

            return (1/6)*(-v321 + v231 + v312 - v132 - v213 + v123)
        volumes = []
        for t in self.faces:
            volumes.append(signed_vol_tri(
                            self.vertices[t[0]],
                            self.vertices[t[1]],
                            self.vertices[t[2]]))
        return abs(sum(volumes))

    @property
    def weight(self):
        return self.volume * self.density * 9.8