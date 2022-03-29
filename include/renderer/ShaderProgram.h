#pragma once
#include "common.h"
#include "renderer/Shader.h"

class ShaderProgram {
public:
    ShaderProgram(Shader vertex, Shader fragment);
    ShaderProgram(const char* vertexFilepath, const char* fragmentFilepath);
    ~ShaderProgram();

    GLuint programID;
private:
    void errorCheck();
};