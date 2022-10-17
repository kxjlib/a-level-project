#version 330

in vec2 in_vert;
in vec2 in_text;

out vec2 v_texture;

void main() {
    gl_Position = vec4(in_vert,0.0,1.0);
    v_texture = in_text;
}