#include "renderer/bindable/ShaderProgram.h"
#include "renderer/Shader.h"
#include "utils/utils.h"

ShaderProgram::ShaderProgram(const char* vertFilepath, const char* fragFilepath) {
    // Create Program ID
    programID = glCreateProgram();

    // Load Shader Source from Filepaths specified in params

    std::string vertSource = readFile(vertFilepath);
    std::string fragSource = readFile(fragFilepath);

    // Create Shaders

    Shader vertShader(GL_VERTEX_SHADER, vertSource.c_str());
    Shader fragShader(GL_FRAGMENT_SHADER, fragSource.c_str());
    
    // Link & Compile Program
    glAttachShader(programID, vertShader.shaderID);
    glAttachShader(programID, fragShader.shaderID);

    glLinkProgram(programID);

    errorCheck();
}

ShaderProgram::~ShaderProgram() {
    glDeleteProgram(programID);
}

void ShaderProgram::errorCheck() {
    // Error Checking
    int success;
    glGetProgramiv(programID, GL_LINK_STATUS, &success);

    if (!success) {
        char infoLog[512];
        glGetProgramInfoLog(programID, 512, NULL, infoLog);
        std::string log = infoLog;
        throw std::runtime_error("[Error] Program Compilation:\n" + log + "\n");
    }
}

void ShaderProgram::use() {
    glUseProgram(programID);
}