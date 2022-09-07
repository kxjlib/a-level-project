# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# MainMenu.py

from impl.states.State import State
from impl.Button import Button
from impl.InformationManager import Info
from renderer.Renderer import Renderer
from renderer.Camera import Camera

import moderngl


class Settings(State):
    buttons = {}

    def __init__(self, gl_ctx: moderngl.Context):
        super().__init__(gl_ctx)

    def model_init(self, gl_ctx: moderngl.Context):
        # Create a settings button, and center it 0.1 off in the top right
        self.buttons['settings'] = Button(
            gl_ctx, "settings_icon", 0.1, 0.1 * Info.aspect_ratio, 0.9, 1 - (0.1 * Info.aspect_ratio))

    def update(self):
        if self.buttons['settings'].is_clicked():
            Info.current_screen = "main_menu"

    def render(self, gl_ctx: moderngl.Context, renderer: Renderer, camera: Camera):
        gl_ctx.clear(0.1, 0.1, 0.1)
        for k, v in self.buttons.items():
            v.render()
