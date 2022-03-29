#include "renderer/ShaderProgram.h"
#include "renderer/Shader.h"
#include <fstream>
#include <vector>

// Readfile Function
std::string readFile(const char* filename) {
    
    // Open file to ifs
    std::ifstream ifs(filename, std::ios::in | std::ios::binary | std::ios::ate);

    // get Filesize and set readhead to pos 0
    std::ifstream::pos_type fileSize = ifs.tellg();
    ifs.seekg(0, std::ios::beg);

    // load file contents into bytes vector
    std::vector<char> bytes(fileSize);
    ifs.read(&bytes[0], fileSize);

    // return as string
    return std::string(&bytes[0], fileSize);
}

ShaderProgram::ShaderProgram(Shader vertex, Shader fragment) {
    // Create Program Id
    programID = glCreateProgram();

    // Attach Fragment and Vertex Shaders
    glAttachShader(programID, vertex.shaderID);
    glAttachShader(programID, fragment.shaderID);

    // Compile the Program
    glLinkProgram(programID);

    errorCheck();
}

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