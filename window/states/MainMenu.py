# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# MainMenu.py

import moderngl

from .State import State
from ..renderer.Renderer import Renderer
from ..renderer.Camera import Camera

from ..impl.Text import Text
from ..impl.Button import Button
from ..impl.InformationManager import Info


class MainMenu(State):
    buttons = {}
    text = {}

    def __init__(self, gl_ctx: moderngl.Context):
        self.text['ff_name'] = Text(
            gl_ctx, "Flight Fidelity", (255, 255, 255), 200, "ff_menu_name_tex", 0, 0.7)

        # Create a settings button, and center it 0.1 off in the top right
        self.buttons['ff_settings'] = Button(
            gl_ctx, "settings_icon", 0.1, 0.1 * Info.aspect_ratio, 0.9, 1 - (0.1 * Info.aspect_ratio))

        self.buttons['ff_sim_menu'] = Button(
            gl_ctx, "button", 0.65, 0.1 * Info.aspect_ratio, 0, -0.4, "Physics Simulation", (0, 0, 0))

        self.buttons['ff_mod_menu'] = Button(
            gl_ctx, "button", 0.5, 0.1 *
            Info.aspect_ratio, 0, -0.15, "Model Analysis", (0, 0, 0))

        super().__init__(gl_ctx)

    def model_init(self, gl_ctx: moderngl.Context):
        pass

    def update(self, gl_ctx: moderngl.Context):
        if self.buttons['ff_settings'].is_clicked():
            Info.current_screen = "settings_menu"
        
        if self.buttons['ff_sim_menu'].is_clicked():
            Info.current_screen = "sim_menu"
        
        if self.buttons['ff_mod_menu'].is_clicked():
            Info.current_screen = "model_menu"

    def render_ui(self, gl_ctx: moderngl.Context):
        gl_ctx.disable(moderngl.DEPTH_TEST)

        # Render Buttons
        for v in self.buttons.values():
            v.render()

        # Render Text over Buttons
        for v in self.text.values():
            v.render()

        gl_ctx.enable(moderngl.DEPTH_TEST)

    def render(self, gl_ctx: moderngl.Context, renderer: Renderer, camera: Camera):
        gl_ctx.clear(0.1, 0.1, 0.1)
        self.render_ui(gl_ctx)
