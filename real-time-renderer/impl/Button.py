# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Button.py

import numpy as np

class Button(object):
    def __init__(self, width, height, x, y):
        vertices = np.array([
            # x,y texc
            -0.5, -0.5, 0.0, 0.0, # 1 5
            -0.5,  0.5, 0.0, -1.0, # 2 6
             0.5, -0.5, 1.0, 0.0, # 3
             0.5,  0.5, 1.0, -1.0, # 4
        ], dtype='f4')  # Use 4-byte (32-bit) floats