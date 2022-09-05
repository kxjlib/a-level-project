# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Input.py

# The input class needs to:
#   - Store all pressed keys

class Input(object):
    Pressed = {}
    MPressed = {}
    MPos = (0,0)

    lPressed = {}
    lMPressed = {}
    lMPos = (0,0)

    @classmethod
    def next(cls):
        cls.lPressed = cls.Pressed
        cls.lMPressed = cls.MPressed
        cls.lMPos = cls.MPos