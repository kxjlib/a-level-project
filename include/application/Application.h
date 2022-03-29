#pragma once
#include "common.h"

#include "renderer/GlHandler.h"
#include "utils/AssetManager.h"

class Application {
public:
    Application();
    void run();

private:
    GlHandler glHandler;
    AssetManager assetManager;
    void init();
};