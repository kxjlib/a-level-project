# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Settings.py

from impl.states.State import State
from impl.Button import Button
from impl.InformationManager import Info
from renderer.Renderer import Renderer
from renderer.Camera import Camera
from impl.Text import Text
from impl.TextButton import TextButton

import moderngl


class Settings(State):
    buttons = {}
    res_buttons = {}
    text = {}

    def __init__(self, gl_ctx: moderngl.Context):
        super().__init__(gl_ctx)

    def model_init(self, gl_ctx: moderngl.Context):
        self.text['ff_settings_name'] = Text(
            gl_ctx, "Settings", (255, 255, 255), 128, "ff_settings_name_tex", 0, 0.7)
        self.text['ff_settings_res_label'] = Text(
            gl_ctx, "Resolution", (255, 255, 255), 64, "ff_settings_res_label_tex", -0.8, 0.2)
        self.text['ff_settings_res_value'] = Text(
            gl_ctx, f"{Info.scr_size[0]}x{Info.scr_size[1]}", (255, 255, 255), 48, "ff_settings_res_val_tex", -0.58, 0.2)

        # Resolutions
        self.res_buttons['ff_settings_rb_1024'] = TextButton(
            gl_ctx, "1024x576", (255, 255, 255), 32, "ff_settings_res_1024", -0.5, 0.1)
        self.res_buttons['ff_settings_rb_1280'] = TextButton(
            gl_ctx, "1280x720", (255, 255, 255), 32, "ff_settings_res_1280", -0.5, 0.05)
        self.res_buttons['ff_settings_rb_1366'] = TextButton(
            gl_ctx, "1366x768", (255, 255, 255), 32, "ff_settings_res_1366", -0.5, 0.0)
        self.res_buttons['ff_settings_rb_1600'] = TextButton(
            gl_ctx, "1600x900", (255, 255, 255), 32, "ff_settings_res_1600", -0.5, -0.05)
        self.res_buttons['ff_settings_rb_1920'] = TextButton(
            gl_ctx, "1920x1080", (255, 255, 255), 32, "ff_settings_res_1920", -0.5, -0.1)

        for v in self.res_buttons.values():
            v.active = False

        # Create a settings button, and center it 0.1 off in the top right
        self.buttons['settings'] = Button(
            gl_ctx, "settings_icon", 0.1, 0.1 * Info.aspect_ratio, 0.9, 1 - (0.1 * Info.aspect_ratio))
        self.buttons['res_dd'] = Button(
            gl_ctx, "dropdown_icon", 0.025, 0.0125 * Info.aspect_ratio, -0.45, 0.2)

    def update(self, gl_ctx: moderngl.Context = None):
        if self.buttons['settings'].is_clicked():
            Info.current_screen = "main_menu"
        if self.buttons['res_dd'].is_clicked():
            for k in self.res_buttons.keys():
                self.res_buttons[k].active = not self.res_buttons[k].active

        clicked = [v.is_clicked() for v in self.res_buttons.values()]
        if any(clicked):
            for k in self.res_buttons.keys():
                self.res_buttons[k].active = not self.res_buttons[k].active
            loc = clicked.index(True)
            new_text = self.res_buttons[list(self.res_buttons.keys())[loc]].contents

            self.text['ff_settings_res_value'] = Text(
                gl_ctx, new_text, (255, 255, 255), 48, "ff_settings_res_val_tex", -0.58, 0.2)
            new_res = [int(i) for i in new_text.split("x")]
            Info.new_res = new_res

    def render(self, gl_ctx: moderngl.Context, renderer: Renderer, camera: Camera):
        gl_ctx.clear(0.1, 0.1, 0.1)
        for v in self.buttons.values():
            v.render()
        for v in self.text.values():
            v.render()
        for v in self.res_buttons.values():
            v.render()
