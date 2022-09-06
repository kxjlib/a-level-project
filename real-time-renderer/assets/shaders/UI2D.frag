#version 330

in vec2 v_texture;

uniform sampler2D Texture;

out vec4 f_colour;

void main() {
    f_colour = vec4(texture(Texture, v_texture).rgb, 1.0);
}