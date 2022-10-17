#version 330

in vec2 v_texture;
out vec4 f_colour;

uniform sampler2D Texture;

void main() {
    f_colour = texture(Texture, v_texture);
}