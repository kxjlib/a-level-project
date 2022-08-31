# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# main.py

# Imports
import ctypes
import sys

import numpy as np

import moderngl
import sdl2

# Guard clause to close the program if it's imported
# We do this instead of sticking all the code in a main function for cleanliness
if __name__ != "__main__":
    sys.exit(-1)


# Initialisation

# SDL2 init
# If SDL fails to initialise then error out.
if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
    print(f"[ERROR] : {sdl2.SDL_GetError()}")
    sys.exit(-1)

# Create Window and GL Contex

# Create window using SDL2
wnd = sdl2.SDL_CreateWindow(b"Real-time Renderer",
                            sdl2.SDL_WINDOWPOS_UNDEFINED,    # Window Location on the screen
                            sdl2.SDL_WINDOWPOS_UNDEFINED,
                            800,                            # Window Size
                            600,
                            sdl2.SDL_WINDOW_OPENGL          # Additional window flags
                            )

# Create GL Context

# ModernGL Works by 'piggybacking' of an existing openGL context, and as such we
# first need to create an OpenGL context in SDL before in ModernGL
sdl_context = sdl2.SDL_GL_CreateContext(wnd)
ctx = moderngl.create_context(version=430)


### Window Mainloop

# Create a reference to window events of the SDL window
event = sdl2.SDL_Event()

def render(ctx):
    ctx.clear(0.1,0.1,0.1)

running = True
while running:
    # Event Handling Loop
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
    
    render(ctx)

    # Swap window buffers (make currently rendered frame visible)
    sdl2.SDL_GL_SwapWindow(wnd)

    # Arbitrary Delay to stop excess resource usage
    sdl2.SDL_Delay(10)


## Stop Floating Memory after program finish
ctx.release()
sdl2.SDL_GL_DeleteContext(sdl_context)
sdl2.SDL_DestroyWindow(wnd)
sdl2.SDL_Quit()