# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# InformationManager.py

# Stores some global variables
class Info(object):
    # Class Variables
    scr_size = [1280, 720]
    aspect_ratio = scr_size[0] / scr_size[1]

    @classmethod
    def set_scr_size(cls, value):
        cls.scr_size = value
        cls.aspect_ratio = value[0] / value[1]