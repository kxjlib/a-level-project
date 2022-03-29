#pragma once
#include "common.h"

class Shader {
public:
    GLuint shaderID;
    Shader(GLenum type, const char* source);
    ~Shader();
};