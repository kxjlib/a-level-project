#include "application/Application.h"
#include "renderer/Shader.h"

Application::Application() {
    if(!glHandler.init()) {
        throw std::runtime_error(glHandler.getError());
    }

    // Create Shader Programs
    const char* shaderSource = "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
    "}\0";
    Shader shader = Shader(GL_VERTEX_SHADER, shaderSource);
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