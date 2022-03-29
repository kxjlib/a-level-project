#include "application/Application.h"
#include "renderer/ShaderProgram.h"
#include "utils/AssetManager.h"

Application::Application() {
    if(!glHandler.init()) {
        throw std::runtime_error(glHandler.getError());
    }

    AssetManager assetManager;

    // Create Shader Programs
    ShaderProgram program(
        assetManager.getPath("assets/shaders/triangle.vert").c_str(),
        assetManager.getPath("assets/shaders/triangle.frag").c_str()
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