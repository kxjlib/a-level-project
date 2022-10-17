#version 330

uniform mat4 mvp;

in vec3 in_vert;
in vec2 in_text;

out vec2 v_texture;

void main() {
    gl_Position = mvp * vec4(in_vert,1.0);
    v_texture = in_text;
}