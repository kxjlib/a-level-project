# William Davies
# "Flight Fidelity" Project
# Model Analysis
# Mesh3D.py

# 3D Mesh handling class
#   - needs to open a model file from filename
#   - needs to encapsulate analysis functions
#   - not to be confused with future? glider class in simulation

# Imports
# Will allow us to get all vertex information about the triangle.
import pywavefront
from pyrr import Matrix44, Vector3
import moderngl
import numpy as np
from PIL import Image
from sklearn.preprocessing import normalize


class Mesh3D:
    def __init__(self, filename):
        self.model = self.from_filename(filename)
        self.density = 30  # 30 KG/M^3

    def from_filename(self, filename) -> pywavefront.Wavefront:
        model = pywavefront.Wavefront(filename, collect_faces=True)
        self.vertices = model.vertices
        self.faces = model.mesh_list[0].faces
        self.volume = self.calc_volume()
        return model

    # CALCULATE MESH VOLUME AND WEIGHT

    def calc_volume(self):
        # Uses answer by Frank Krueger on SOverflow Q 1406029
        def signed_vol_tri(p1, p2, p3):
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

    def horiz_area_of_model(self):
        # Calculate the size of the model

        max_w= min_w = 0
        max_d= min_d = 0

        for vertex in self.vertices:
            max_w = max(max_w, vertex[0])
            min_w = min(min_w, vertex[0])

            max_d = max(max_d, vertex[2])
            min_d = min(min_d, vertex[2])

        width = max_w - min_w
        depth = max_d - min_d

        return width * depth

    # CALCULATE WING AREA

    def calc_underside_area(self):

        # This function creates a camera, which renders the underside of the model
        # using an orthographic view. Using this information we can calculate the
        # area on the underside of the craft - thus being able to calculate the
        # lift of the object using other information.
        
        # Create Orthographic Camera

        ctx = moderngl.create_standalone_context()

        # Create VAOs and Camera inform
        prog = ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_vert;

                void main() {
                    gl_Position = vec4(in_vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec3 f_colour;

                void main() {
                    f_colour = vec3(1.0,1.0,1.0);
                }
            ''',
        )

        # Creates a Framebuffer so that we can render the image to memory rather than the screen
        fbo = ctx.simple_framebuffer((512, 512))
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)

        verts = np.array(normalize(self.model.vertices), dtype=float)

        obj_vert = ctx.buffer(verts)
        obj_vao = ctx.simple_vertex_array(prog, obj_vert, "in_vert")

        obj_vao.render(moderngl.TRIANGLES)

        # Reads the image into a PIL image object and gets information from the picture
        bottom_side_image_read = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)


        # Calculate the percentage of the underside which is a part of the model
        bbox = bottom_side_image_read.getbbox()
        bounded = bottom_side_image_read.crop(bbox)
        num_of_n_blk = sum(bounded
                .point(lambda x: 255 if x else 0)
                .convert("L")
                .point(bool)
                .getdata())
        
        w,h = bounded.size

        ratio = w*h/num_of_n_blk

        underside_area = self.horiz_area_of_model() * ratio

        ctx.release()

        return underside_area
