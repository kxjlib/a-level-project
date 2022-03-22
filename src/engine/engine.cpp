#include "engine/engine.h"

Engine::Engine()
{
    init_gl();
    init_ui();
}

Engine::~Engine()
{
    // Terminate GLFW
    glfwTerminate();
}

void Engine::init_gl()
{
    // GLFW Initialisation + Error handling
    if (!glfwInit())
    {
        throw std::runtime_error("[Error] Failed to initialise GLFW");
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
        throw std::runtime_error("[Error] Failed to create GLFW window");
    }

    // Create OpenGL Context (VERY IMPORTANT)
    glfwMakeContextCurrent(window);

    // Initialise GLAD - Retrieve OpenGL function calls from the OS
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        throw std::runtime_error("[Error] Failed to initialise GLAD");
    }

    glViewport(0, 0, 800, 600);
}

void Engine::init_ui()
{
}

void Engine::run() {
    while (!glfwWindowShouldClose(window))
    {
        /*  Event Loop  */

        // Poll Window Events (Without This The Window Will Hang and Crash)
        glfwPollEvents();

        /*    Update    */

        // Clear Screen
        glClear(GL_COLOR_BUFFER_BIT);

        /* Begin Render */

        /*  End Render  */

        /* Flip Buffers */
        glfwSwapBuffers(window);
    }
}