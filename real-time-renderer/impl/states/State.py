# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# State.py

# The State class needs to:
#   - Control one screen of the UI
#   - Store its own models
#   - Have its own logic

# Imports
from abc import ABCMeta, abstractmethod
import moderngl
from renderer.Renderer import Renderer
from renderer.Camera import Camera

class State(metaclass=ABCMeta):
    # Variables used by the class
    _objects = {}

    def __init__(self, gl_ctx: moderngl.Context):
        self.model_init(gl_ctx)

    @abstractmethod
    def model_init(self, gl_ctx: moderngl.Context):
        pass
    
    @abstractmethod
    def update(self, gl_ctx: moderngl.Context):
        pass
    
    @abstractmethod
    def render(self, gl_ctx: moderngl.Context, renderer: Renderer, camera: Camera):
        pass