# William Davies
# "Flight Fidelity" Project
# Realtime renderer
# main.py

# Imports
import ctypes
import sys

from renderer.WindowManager import GLWindow

import numpy as np

from pyrr import Matrix44, matrix44, Vector3

import moderngl
import sdl2

# Guard clause to close the program if it's imported
# We do this instead of sticking all the code in a main function for cleanliness
if __name__ != "__main__":
    sys.exit(-1)

# Create Window
window = GLWindow("Real-time Renderer", 1400, 600)

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

uniform mat4 mvp;

in vec3 in_vert;

in vec3 in_colour;
out vec3 v_colour; // To Fragment Shader

void main() {
    gl_Position = mvp * vec4(in_vert,1.0);
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

mvp = shader_program['mvp']

view_matrix = Matrix44.perspective_projection(
    70.0,  # Fov angle
    # display aspect ratio (this will nead to be changed when we change the display size)
    1400.0 / 600.0,
    0.1,  # near plane (how close before something stops being rendered)
    100   # far plane (how far before something stops being renderered)
)

look_at = Matrix44.look_at(
    # Location of the camera being used to view the scene
    Vector3([0.0, 0.0, -10.0]),
    # location plus the axis which the camera is pointing
    Vector3([0.0, 0.0, -9.0]),
    Vector3([0.0, 1.0, 0.0])  # the axis which is deemed as 'up'
)

model_matrix = Matrix44.from_translation(Vector3([0.0,0.0,0.0]))

tri_vertices = np.array([
    # x,y,z, rgb
    0.0,  1.0,  0.0, 1.0, 0.0, 0.0,
    -1.0, -1.0,  0.0, 0.0, 1.0, 0.0,
    1.0, -1.0,  0.0, 0.0, 0.0, 1.0,
], dtype='f4')  # Use 4-byte (32-bit) floats

vbo = ctx.buffer(tri_vertices)

vao = ctx.vertex_array(
    shader_program,
    [
        # in_vert needs to be first 3 floats
        # in_colour needs to be the last 3
        (vbo, '3f 3f', 'in_vert', 'in_colour')
    ]
)

ctx.enable_only(moderngl.NOTHING)
ctx.enable(moderngl.DEPTH_TEST)


def render(ctx, frames):
    ctx.clear(0.1, 0.1, 0.1)
    model_matrix = Matrix44.from_translation(Vector3([frames/10.0,0.0,0.0]))
    mvp.write((view_matrix * look_at * model_matrix).astype('f4'))
    vao.render()


running = True
frames = 0
while running:
    # Event Handling Loop
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False

    render(ctx, frames)

    # if frames == 100:
    #    window.resolution = (1024, 768)

    # Swap window buffers (make currently rendered frame visible)
    sdl2.SDL_GL_SwapWindow(window.instance)

    # Arbitrary Delay to stop excess resource usage
    sdl2.SDL_Delay(10)
    frames += 1


# Stop Floating Memory after program finish
ctx.release()
sdl2.SDL_Quit()
