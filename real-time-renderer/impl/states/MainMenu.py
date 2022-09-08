# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# MainMenu.py

from impl.states.State import State
from impl.Button import Button
from impl.Text import Text
from impl.InformationManager import Info
from renderer.Renderer import Renderer
from renderer.Camera import Camera

import moderngl


class MainMenu(State):
    buttons = {}
    text = {}
    other = False

    def __init__(self, gl_ctx: moderngl.Context):
        super().__init__(gl_ctx)

    def model_init(self, gl_ctx: moderngl.Context):
        self.text['ff_name'] = Text(
            gl_ctx, "Flight Fidelity", (255, 255, 255), 200, "ff_menu_name_tex", 0, 0.7)

        self.buttons['start'] = Button(
            gl_ctx, "start_button", 0.3, 0.1 * Info.aspect_ratio, 0, -0.6)
        # Create a settings button, and center it 0.1 off in the top right
        self.buttons['settings'] = Button(
            gl_ctx, "settings_icon", 0.1, 0.1 * Info.aspect_ratio, 0.9, 1 - (0.1 * Info.aspect_ratio))

    def update(self,gl_ctx: moderngl.Context =None):
        if self.buttons['start'].is_clicked():
            print("start")
        if self.buttons['settings'].is_clicked():
            Info.current_screen = "settings_menu"

    def render(self, gl_ctx: moderngl.Context, renderer: Renderer, camera: Camera):
        gl_ctx.clear(0.1, 0.1, 0.1)
        for v in self.buttons.values():
            v.render()
        self.text['ff_name'].render()
