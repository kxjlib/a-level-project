#include "utils/AssetManager.h"

AssetManager::AssetManager() {
    // Find Folder which holds the executable - so that we do not necessarily need to run the executable from its folder.
    // NOTE: this uses a windows function call, and if it is to be made cross-platform needs to have some OS-specific
    //  macros made.
    // However i kinda cba to do that rn
    char buffer[MAX_PATH];
    GetModuleFileNameA( NULL, buffer, MAX_PATH );
    // GetModuleFileNameA returns the path to the executable, not its folder so remove the executable name from the buffer.
    std::string::size_type pos = std::string(buffer).find_last_of("\\/");
    directoryPath = std::string(buffer).substr(0, pos+1);
}

std::string AssetManager::getPath(std::string relativeToPath) {
    return directoryPath + relativeToPath;
}

std::string AssetManager::getExecutableDirectory() {
    return directoryPath;
}