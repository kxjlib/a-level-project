# William Davies
# "Flight Fidelity" Project
# Physics Engine
# PhysicsHandler.py

import pickle
import pywavefront
import numpy as np
import moderngl

from ..renderer.ShaderManager import ShaderManager
from ..renderer.bindable.Object import Object


class PhysicsHandler:
    def __init__(self, filename, gl_ctx: moderngl.Context):
        model_info = self.import_model_from_file(filename)
        model_filename = model_info['m_file']
        self.render_model = self.create_render_model(model_filename, gl_ctx)

    def import_model_from_file(self, filename) -> dict:
        # Load model file into memory using pickle
        imported_file = None
        with open(filename, 'rb') as file:
            imported_file = pickle.load(file)

        # Ensure that the file was able to be opened and read
        if not imported_file:
            raise ValueError(f"Model File {filename} could not be opened!")

        return imported_file

    def create_render_model(self, filename, gl_ctx: moderngl.Context):
        # Import model from file and grab vertices
        wavefront_model = pywavefront.Wavefront(filename, collect_faces=True)
        model_vertices = wavefront_model.vertices

        # convert vertices to numpy format
        numpy_vertices = np.array(model_vertices, dtype='f4').flatten()

        # create VAO based on given model information
        vertices_vbo = gl_ctx.buffer(numpy_vertices)
        model_vao = gl_ctx.vertex_array(
            ShaderManager.shaders['model3D'].inst,
            [
                (vertices_vbo, '3f', 'in_vert')
            ]
        )

        # create object instance
        model_object = Object(model_vao, 'model3D')

        return model_object
