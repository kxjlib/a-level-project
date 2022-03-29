#pragma once

#include <iostream>
#include <Windows.h>

class AssetManager {
private:
    std::string directoryPath;
public:
    AssetManager();
    std::string getPath(std::string relativeToPath);
    std::string getExecutableDirectory();
};