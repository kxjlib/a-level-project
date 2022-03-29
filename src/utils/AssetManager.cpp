#include "utils/AssetManager.h"

AssetManager::AssetManager() {
    char buffer[MAX_PATH];
    GetModuleFileNameA( NULL, buffer, MAX_PATH );
    std::string::size_type pos = std::string(buffer).find_last_of("\\/");
    directoryPath = std::string(buffer).substr(0, pos+1);
}

std::string AssetManager::getPath(std::string relativeToPath) {
    return directoryPath + relativeToPath;
}

std::string AssetManager::getExecutableDirectory() {
    return directoryPath;
}