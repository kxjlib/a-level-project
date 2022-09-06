#version 330

in vec2 v_texture;

uniform sampler2D Texture;

out vec4 f_colour;

void main() {
    f_colour = texture(Texture, v_texture);
}