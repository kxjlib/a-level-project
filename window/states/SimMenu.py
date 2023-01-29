# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# MainMenu.py

from .State import State
from ..impl.Button import Button
from ..impl.Text import Text
from ..impl.InformationManager import Info
from ..renderer.Renderer import Renderer
from ..renderer.Camera import Camera
from ..simulation.PhysicsHandler import PhysicsHandler

import moderngl
from win32 import win32gui
import win32con
import os

class SimMenu(State):
    buttons = {}
    text = {}
    other = False
    sfile_name = ""

    def __init__(self, gl_ctx: moderngl.Context):
        super().__init__(gl_ctx)
        self.simulation_began = False

    def model_init(self, gl_ctx: moderngl.Context):
        self.text['sm_name'] = Text(
            gl_ctx, "Physics Simulation", (255, 255, 255), 200, "sm_menu_main_text", 0, 0.7)
        
        self.buttons['start'] = Button(
            gl_ctx, "button", 0.3, 0.1 * Info.aspect_ratio, 0, -0.6, "Start", (0, 0, 0))
        self.buttons['sim_select'] = Button(
            gl_ctx, "button", 0.4, 0.1 * Info.aspect_ratio, 0, 0.3, "Select File", (0,0,0)
        )

    def file_prompt(self):
        prompt_res = win32gui.GetOpenFileNameW(
            InitialDir=os.environ['temp'],
            Flags = win32con.OFN_EXPLORER,
            Title= "Select a Model File",
            DefExt="bin"
        )
        return prompt_res[0]

    def update(self, gl_ctx: moderngl.Context = None):
        if self.buttons['start'].is_clicked():
            self.phys_handler = PhysicsHandler(self.sfile_name, gl_ctx)
            self.simulation_began = True

        if self.buttons['sim_select'].is_clicked():
            self.sfile_name = self.file_prompt()
            self.text['ff_filename'] = Text(
                gl_ctx, self.sfile_name, (255, 255, 255), 50, "ff_menu_filename", 0, 0.15)

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
        
        if not self.simulation_began:
            self.render_ui(gl_ctx)

        if self.simulation_began:
            renderer.render_object(self.phys_handler.render_model, camera)
