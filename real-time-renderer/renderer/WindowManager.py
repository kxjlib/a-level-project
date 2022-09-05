# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# WindowManager.py

# GLWindow Class

# this class needs to:
#   - allow for the creation of the window
#   - allow showing the window
#   - construction of the SDL GL Context
#   - needs to allow access to the GL Context externally

# Imports
import ctypes
import sdl2
import sys


class GLWindow(object):
    # Variables which will be used to store window information
    _winstance = None
    _sdlctx = None
    _dimensions = (800, 600)
    _title = "OpenGL Window"

    def __init__(self, title: str, width: int, height: int):
        # Store arguments
        self._dimensions = (width, height)
        self._title = title

        # Initialise SDL2
        # If SDL fails to initialise then error out.
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            print(f"[ERROR] SDL2 Initialisation : {sdl2.SDL_GetError()}")
            sys.exit(-1)

        # Create Instance of SDL Window, and store in _winstance variable.
        self._winstance = \
            sdl2.SDL_CreateWindow(title.encode(),
                                  sdl2.SDL_WINDOWPOS_UNDEFINED,    # Window Location on the screen
                                  sdl2.SDL_WINDOWPOS_UNDEFINED,
                                  width,                            # Window Size
                                  height,
                                  sdl2.SDL_WINDOW_OPENGL          # Additional window flags
                                  )

        # If for whatever reason SDL fails to create the window, let the user know
        if self._winstance == None:
            print(f"[Error] Window Creation : {sdl2.SDL_GetError()}")
            sys.exit(-1)

        # Create the SDL2 GL Context
        self._sdlctx = sdl2.SDL_GL_CreateContext(self._winstance)

    # Custom Getters and Setters to prevent unexpected behaviour

    @property
    # The program should not be able to overwrite the window instance.
    def instance(self):
        return self._winstance

    # Memory Management
    @instance.deleter
    def instance(self):
        sdl2.SDL_DestroyWindow(self._winstance)

    @property
    def context(self):  # The context should only be initialised once, so should not be able to modify
        return self._sdlctx

    # Memory Management
    @context.deleter
    def context(self):
        sdl2.SDL_GL_DeleteContext(self._sdlctx)

    # Resolution property
    # When getter is called, should return the dimensions of the window
    # However when set should run relevant code to allow SDL2 Window to change size.
    @property
    def resolution(self):
        w = ctypes.c_int()  # This can be used as a pointer and modified by GetWindowSize
        h = ctypes.c_int()
        sdl2.SDL_GetWindowSize(self._winstance, w, h)
        return (w.value, h.value)

    @resolution.setter
    def resolution(self, value: tuple):
        # Set instance variable
        self._dimensions = value

        # Tell SDL2 to resize window.
        sdl2.SDL_SetWindowSize(self._winstance, value[0], value[1])
