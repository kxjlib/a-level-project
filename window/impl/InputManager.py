# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Input.py

# The input class needs to:
#   - Store all pressed keys

from .InformationManager import Info

class Input(object):
    Pressed = {}
    MPressed = {}
    MPos = (0, 0)

    lPressed = {}
    lMPressed = {}
    lMPos = (0, 0)

    @classmethod
    def next(cls):
        cls.lPressed = cls.Pressed.copy()
        cls.lMPressed = cls.MPressed.copy()
        cls.lMPos = cls.MPos

    @classmethod
    def mouse_to_screen(cls):
        # Maps an x,y coordinate to its relative location on the screen
        mouse_adj = [(2 * cls.MPos[i])/Info.scr_size[i] - 1 for i in range(2)]
        mouse_adj[1] = -mouse_adj[1]
        return mouse_adj
