#version 330

in vec3 v_colour;
out vec4 f_colour;

void main() {
    f_colour = vec4(v_colour, 1.0);
}