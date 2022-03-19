#include <iostream>

#include <glad/glad.h>
#include <GLFW/glfw3.h>

int main()
{
    // GLFW Initialisation + Error handling
    if (!glfwInit())
    {
        std::cout << "[Error] Failed to initialise GLFW\n";
        return -1;
    }

    // Set OpenGL Settings (OpenGL Version and Profile)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Create Window + Error Handling
    GLFWwindow *window = glfwCreateWindow(800, 600, "A-Level CS", NULL, NULL);
    if (!window)
    {
        std::cout << "[Error] Failed to create GLFW window\n";
        glfwTerminate();
        return -1;
    }

    // Create OpenGL Context (VERY IMPORTANT)
    glfwMakeContextCurrent(window);

    // Initialise GLAD - Retrieve OpenGL function calls from the OS
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "[Error] Failed to initialise GLAD\n";
        return -1;
    }

    glViewport(0, 0, 800, 600);

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
    // Close Application + GLFW Memory Management
    return 0;
}
