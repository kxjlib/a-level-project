#include "renderer/Shader.h"

Shader::Shader(GLenum type, const char* source) {
    // Create Shader ID
    shaderID = glCreateShader(type);

    // Set the Shaders source-code and compile it
    glShaderSource(shaderID, 1, &source, NULL);
    glCompileShader(shaderID);

    // Error Checking
    int success;
    glGetShaderiv(shaderID, GL_COMPILE_STATUS, &success);

    if (!success) {
        char infoLog[512];
        glGetShaderInfoLog(shaderID, 512, NULL, infoLog);

        std::string log = infoLog;
        throw std::runtime_error("[Error] Shader Compilation:\n" + log + "\n");
    }
}

Shader::~Shader() {
    glDeleteShader(shaderID);
}