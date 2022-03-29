#pragma once
#include "common.h"
#include "renderer/Shader.h"

class ShaderProgram {
public:
    ShaderProgram(const char* vertexFilepath, const char* fragmentFilepath);
    ~ShaderProgram();

    void use();

private:
    GLuint programID;
    void errorCheck();
};