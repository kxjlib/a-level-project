#include "application/Application.h"
#include "renderer/ShaderProgram.h"

Application::Application() {
    if(!glHandler.init()) {
        throw std::runtime_error(glHandler.getError());
    }

    // Create Shader Programs
    ShaderProgram program(
        "assets/shaders/triangle.vert",
        "assets/shaders/triangle.frag"
    );
}

Application::~Application() {

}

void Application::run() {
    GLFWwindow* window = glHandler.getWindowRef();
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