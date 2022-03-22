#pragma once

#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>


class Engine
{
public:
    Engine();
    ~Engine();
    void run();
private:
    GLFWwindow* window;
    void init_gl();
    void init_ui();
};