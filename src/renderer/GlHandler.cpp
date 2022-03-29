#include "renderer/GlHandler.h"

GlHandler::GlHandler() {
    glError = "";
}

GlHandler::~GlHandler() {
    // Terminate GLFW
    glfwTerminate();
}

const char* GlHandler::getError() {
    return glError.c_str();
}

bool GlHandler::init() {
    // GLFW Initialisation + Error handling
    if (!glfwInit())
    {
        glError = "[Error] Failed to initialise GLFW";
        return false;
    }

    // Set OpenGL Settings (OpenGL Version and Profile)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Create Window + Error Handling
    window = glfwCreateWindow(800, 600, "A-Level CS", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        glError = "[Error] Failed to create GLFW window";
        return false;
    }

    // Create OpenGL Context (VERY IMPORTANT)
    glfwMakeContextCurrent(window);

    // Initialise GLAD - Retrieve OpenGL function calls from the OS
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        glError = "[Error] Failed to initialise GLAD";
        return false;
    }


    // Set Window Viewport to Render to
    glViewport(0, 0, 800, 600);

    // There was no error with OpenGL Initialisation
    return true;
}

GLFWwindow* GlHandler::getWindowRef() {
    return window;
}