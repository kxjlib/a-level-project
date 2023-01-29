# William Davies
# "Flight Fidelity" Project
# Model analysis
# main.py

# Imports

from .State import State
from ..impl.Button import Button
from ..impl.Text import Text
from ..impl.InformationManager import Info
from ..renderer.Renderer import Renderer
from ..renderer.Camera import Camera
from ..modelan.Mesh3D import Mesh3D

import moderngl
from win32 import win32gui
import win32con
import os

import pickle

class ModelMenu(State):
    buttons = {}
    text = {}
    other = False
    sfile_name = ""

    def __init__(self, gl_ctx: moderngl.Context):
        super().__init__(gl_ctx)

    def model_init(self, gl_ctx: moderngl.Context):
        self.text['sm_name'] = Text(
            gl_ctx, "Model Analysis", (255, 255, 255), 200, "mm_menu_main_text", 0, 0.7)
        
        self.buttons['start'] = Button(
            gl_ctx, "button", 0.5, 0.1 * Info.aspect_ratio, 0, -0.6, "Begin Analysis", (0, 0, 0))
        self.buttons['mod_select'] = Button(
            gl_ctx, "button", 0.4, 0.1 * Info.aspect_ratio, 0, 0.3, "Select File", (0,0,0)
        )

    def file_prompt(self):
        prompt_res = win32gui.GetOpenFileNameW(
            InitialDir=os.environ['temp'],
            Flags = win32con.OFN_EXPLORER,
            Title= "Select a Simulation",
            DefExt="sim"
        )
        return prompt_res[0]

    def update(self, gl_ctx: moderngl.Context = None):
        if self.buttons['start'].is_clicked():
            self.begin_analysis()
        if self.buttons['mod_select'].is_clicked():
            self.sfile_name = self.file_prompt()
            self.text['ff_filename'] = Text(
                gl_ctx, self.sfile_name, (255, 255, 255), 50, "ff_msel_filename", 0, 0.15)

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
    
    def begin_analysis(self):
        # Ensures that a filename has been set
        if self.sfile_name == None:
            return

        mesh = Mesh3D(self.sfile_name)

        m_volume = mesh.volume
        m_weight = mesh.weight
        m_uarea = mesh.calc_underside_area()

        # Create Dictionary to be stored to disk
        save_data = {
            "volume": m_volume,
            "weight": m_weight,
            "u_area": m_uarea,
            "m_file": self.sfile_name
        }

        filename_list = self.sfile_name.split("\\")
        filename = filename_list[len(filename_list)-1][:-4] + ".bin"

        with open(f"saved_models/{filename}","wb") as file:
            pickle.dump(save_data, file)

        print("Successfully stored file to Disk")