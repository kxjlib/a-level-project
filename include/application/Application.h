#pragma once
#include "common.h"

#include "renderer/GlHandler.h"

class Application {
public:
    Application();
    ~Application();
    void run();

private:
    GlHandler glHandler;
};