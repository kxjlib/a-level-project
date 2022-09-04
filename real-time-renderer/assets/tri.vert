#version 330

uniform mat4 mvp;

in vec3 in_vert;

in vec3 in_colour;
out vec3 v_colour; // To Fragment Shader

void main() {
    gl_Position = mvp * vec4(in_vert,1.0);
    v_colour = in_colour;
}