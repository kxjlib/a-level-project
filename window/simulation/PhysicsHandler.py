# William Davies
# "Flight Fidelity" Project
# Physics Engine
# PhysicsHandler.py

import pickle
import pywavefront
import numpy as np
import moderngl

import math

from ..renderer.ShaderManager import ShaderManager
from ..renderer.bindable.Object import Object


class PhysicsHandler:
    def __init__(self, filename, gl_ctx: moderngl.Context):
        model_info = self.import_model_from_file(filename)
        model_filename = model_info['m_file']
        
        # Take information from imported bin file
        
        self.render_model = self.create_render_model(model_filename, gl_ctx)
        self.weight = model_info['weight']
        self.u_area = model_info['u_area'] * 0.7
        self.volume = model_info['volume']
        self.w_span = model_info['w_span']
        
        # Set default height to 5m
        self.pos = [0,5]

        # Set default launch velocity to 5 metres per second
        self.velocity = [5,0]

    def calc_lift(self) -> float:
        # L = CL((rV^22)A
        # CL = 2pi(AOA)
        # AOA can assumed to be 1 as the plane is at a flat attack path
        # R is air density (at sea level about 1.225)

        cl = 2 * math.pi
        r = 1.225
        v = self.velocity[1]
        a = self.u_area

        lift = cl * ((r * (v**2))/2) * a

        return lift
    
    def calc_drag(self) -> float:
        # D = CD * ((r * v^2)/2) a
        # CD = CD0 + (CL^2)/pi(Ar)e
        # CL = 2pi(AOA)
        # Ar = Wingspan^2/WingArea
        # e = 1.78(1 - 0.45Ar^0.68) - 0.64
        
        ar = (self.w_span ** 2) / self.u_area
        
        e = 1.78 * (1 - (0.45 * (ar ** 0.68))) - 0.64

        cd = 0.028 + (((2 * math.pi) ** 2) / (math.pi * ar * e))

        r = 1.225
        v = self.velocity[0]
        a = self.u_area * 0.2
        drag = cd * ((r * v**2)/2) * a

        return drag
    
    def calc_acc_per_step(self):
        lift = self.calc_lift()
        drag = self.calc_drag()

        x_forces = -drag
        y_forces = lift - self.weight

        mass = self.weight/9.8

        x_acc = x_forces / mass
        y_acc = y_forces / 9.8

        return x_acc, y_acc
    
    
    def update(self):
        x_a, y_a = self.calc_acc_per_step()

        self.velocity[0] += 0.1 * x_a
        self.velocity[0] = max(0, self.velocity[0])
        self.velocity[1] += 0.1 * y_a

        self.pos[1] += 0.1 * self.velocity[1]

        self.pos[1] = max(0, self.pos[1])

        if self.pos[1] != 0:
            self.pos[0] += 0.1 * self.velocity[0]


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
        model_object = Object(model_vao, 'model3D', [0,0,-1])

        return model_object
