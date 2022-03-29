#include "application/Application.h"
#include "renderer/bindable/ShaderProgram.h"

Application::Application() {
    init();
}

void Application::init() {
    // Initialise GL Handler and complete Error Checking
    if(!glHandler.init()) {
        throw std::runtime_error(glHandler.getError());
    }
}

void Application::run() {
    
    // Create Shader Programs
    ShaderProgram triangleProgram(
        assetManager.getPath("assets/shaders/triangle.vert").c_str(),
        assetManager.getPath("assets/shaders/triangle.frag").c_str()
    );
    
    // Vertices for a triangle to fill the screen with
    float vertices[] = {
        -0.5f, -0.5f, 0.0f,
        0.5f, -0.5f, 0.0f,
        0.0f,  0.5f, 0.0f
    };

    GLuint VBO, VAO;

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);

    // Bind VAO
    glBindVertexArray(VAO);
    
    // Copy Vertices Information into a VBO for OpenGL to Use
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    // Set the active VBO to be bound to Location 0 in the Vertex Shader
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    // Unbind Objects
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    GLFWwindow* window = glHandler.getWindowRef();
    while (!glfwWindowShouldClose(window))
    {
        /*  Event Loop  */

        /*    Update    */

        // Clear Screen
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        /* Begin Render */
        // Draw Triangle
        triangleProgram.use();
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        /*  End Render  */

        /* Flip Buffers */
        glfwSwapBuffers(window);

        // Poll Window Events (Without This The Window Will Hang and Crash)
        glfwPollEvents();
    }
}