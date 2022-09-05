#version 330

in vec3 v_colour;
in vec2 v_texture;
out vec4 f_colour;

uniform sampler2D Texture;

void main() {
    f_colour = vec4(texture(Texture, v_texture).rgb, 1.0);
}