# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# main.py

# Imports
import ctypes
import sys

from renderer.WindowManager import GLWindow

import moderngl
import sdl2

# Guard clause to close the program if it's imported
# We do this instead of sticking all the code in a main function for cleanliness
if __name__ != "__main__":
    sys.exit(-1)

# Create Window
window = GLWindow("Real-time Renderer", 800, 600)

# Create GL Context

# ModernGL Works by 'piggybacking' of an existing openGL context, and as such we
# first need to create an OpenGL context in SDL before in ModernGL
ctx = moderngl.create_context(version=430)


# Window Mainloop

# Create a reference to window events of the SDL window
event = sdl2.SDL_Event()


def render(ctx):
    ctx.clear(0.1, 0.1, 0.1)


running = True
frames = 0
while running:
    # Event Handling Loop
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False

    render(ctx)

    if frames == 100:
        window.resolution = (1024, 768)

    # Swap window buffers (make currently rendered frame visible)
    sdl2.SDL_GL_SwapWindow(window.instance)

    # Arbitrary Delay to stop excess resource usage
    sdl2.SDL_Delay(10)
    frames += 1


# Stop Floating Memory after program finish
ctx.release()
sdl2.SDL_Quit()
