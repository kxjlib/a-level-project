# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# Application.py

# The Application class needs to:
#   - allow for the creation of a window
#   - control the window mainloop
#   - allow for us to render objects
#   - control logic for the program

# Imports
from renderer.WindowManager import GLWindow
from renderer.TextureManager import TextureManager
from renderer.Camera import Camera
from renderer.Renderer import Renderer
from renderer.bindable.ShaderProgram import ShaderProgram
from renderer.bindable.Object import Object
from renderer.ShaderManager import ShaderManager

from impl.InformationManager import Info
from impl.InputManager import Input

# States
from impl.states.MainMenu import MainMenu
from impl.states.Settings import Settings

import ctypes
import moderngl
import sdl2


class Application(object):
    # Variables which will be used by the class
    winst = None
    run = False
    ctx = None
    rnd = None
    shaders = {}
    cam = None
    app_states = {}
    current_state = ""

    def __init__(self, title, dimensions):
        Info.scr_size = dimensions
        # We can unpack the dimensions tuple using the * prefix
        # This saves us from doing dimensions[0] and dimensions[1]
        self.winst = GLWindow(title, *dimensions)

        # ModernGL Works by 'piggybacking' of an existing openGL context, and as such we
        # first need to create an OpenGL context in SDL before in ModernGL
        self.ctx = moderngl.create_context(version=430)

        # set OpenGL Settings
        self.ctx.enable_only(moderngl.NOTHING)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)

        # Program initialisation
        self.shader_init()
        self.texture_init()

        # Initialise States
        self.app_states = {
            "main_menu" : MainMenu(self.ctx),
            "settings_menu" : Settings(self.ctx)
        }
        Info.current_screen = "main_menu"

        self.rnd = Renderer(self.shaders)

        # define Camera
        self.cam = Camera(dimensions, [0.0, 0.0, -10.0], [0.0, 0.0, 1.0])

    # Loads all shader files into the program and stores them
    def shader_init(self):
        # all Shaders (Registry Name, Filename)
        shaders = {'texture3D': "texture3D",
                   'UI2D': "UI2D"}
        
        ShaderManager.from_dict(self.ctx,shaders)

    # Initialises all Textures
    def texture_init(self):
        # Registry Name : Filename(Starting at assets)
        textures = {'start_button': 'startbutton.png',
                    'settings_icon': 'settingsicon.png'}
        for k, v in textures.items():
            TextureManager.from_image(self.ctx, v, k)

    # Will handle all window events every frame
    def event_loop(self, e):
        Input.next()
        while sdl2.SDL_PollEvent(ctypes.byref(e)) != 0:
            if e.type == sdl2.SDL_QUIT:
                self.run = False
                return

            if e.type == sdl2.SDL_KEYDOWN:
                Input.Pressed[e.key.keysym.sym] = True
            elif e.type == sdl2.SDL_KEYUP:
                Input.Pressed[e.key.keysym.sym] = False
            elif e.type == sdl2.SDL_MOUSEMOTION:
                mPos = [e.motion.x, e.motion.y]
                Input.MPos = mPos
            elif e.type == sdl2.SDL_MOUSEBUTTONDOWN:
                Input.MPressed[e.button.button] = True
            elif e.type == sdl2.SDL_MOUSEBUTTONUP:
                Input.MPressed[e.button.button] = False

    def resize_window(self, res):
        # Changes all relevant instances of the window resolution (definately should only be one)
        self.ctx.viewport = (0, 0, *res)
        self.winst.resolution = res
        self.cam.resize_camera(res)
        Info.set_scr_size(res)

    # Main entrypoint into the program, will contain the mainloop
    def run(self):
        event = sdl2.SDL_Event()
        self.run = True
        while self.run:
            # Event Handling Loop
            self.event_loop(event)

            # State Machine update and render
            self.app_states[Info.current_screen].update()
            self.app_states[Info.current_screen].render(self.ctx, self.rnd, self.cam)

            # Swap window buffers (make currently rendered frame visible)
            sdl2.SDL_GL_SwapWindow(self.winst.instance)

            # Arbitrary Delay to stop excess resource usage
            sdl2.SDL_Delay(10)

        # Stop Floating Memory after program finish
        self.ctx.release()
        sdl2.SDL_Quit()
