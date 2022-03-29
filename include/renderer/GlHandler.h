#pragma once
#include "common.h"

class GlHandler {
public:
    GlHandler();
    ~GlHandler();
    bool init();

    GLFWwindow* getWindowRef();

    const char* getError();
private:
    GLFWwindow* window;
    std::string glError;
};