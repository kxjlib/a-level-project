# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# main.py

# Imports
import ctypes
import sys

from renderer.WindowManager import GLWindow

import numpy as np

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


# Create Shaders and Program
vert_shader = """
#version 330

in vec2 in_vert;

in vec3 in_colour;
out vec3 v_colour; // To Fragment Shader

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_colour = in_colour;
}
"""

frag_shader = """
#version 330

in vec3 v_colour;
out vec4 f_colour;

void main() {
    f_colour = vec4(v_colour, 1.0);
}
"""

shader_program = ctx.program(vertex_shader=vert_shader,
                             fragment_shader=frag_shader)

tri_vertices = np.array([
    # x,y, rgb
     0.0,  0.8, 1.0, 0.0, 0.0,
    -0.6, -0.8, 0.0, 1.0, 0.0,
     0.6, -0.8, 0.0, 0.0, 1.0,
], dtype='f4') # Use 4-byte (32-bit) floats

vbo = ctx.buffer(tri_vertices)

vao = ctx.vertex_array(
    shader_program,
    [
        # in_vert needs to be first 2 floats
        # in_colour needs to be the last 3
        (vbo, '2f 3f', 'in_vert', 'in_colour')
    ]
)

def render(ctx):
    ctx.clear(0.1, 0.1, 0.1)
    vao.render()

running = True
frames = 0
while running:
    # Event Handling Loop
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False

    render(ctx)

    #if frames == 100:
    #    window.resolution = (1024, 768)

    # Swap window buffers (make currently rendered frame visible)
    sdl2.SDL_GL_SwapWindow(window.instance)

    # Arbitrary Delay to stop excess resource usage
    sdl2.SDL_Delay(10)
    frames += 1


# Stop Floating Memory after program finish
ctx.release()
sdl2.SDL_Quit()
