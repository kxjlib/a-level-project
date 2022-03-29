#include "utils/utils.h"

// Readfile Function
std::string readFile(const char* filename) {
    
    // Open file to ifs
    std::ifstream ifs(filename, std::ios::in | std::ios::binary | std::ios::ate);

    // get Filesize and set readhead to pos 0
    std::ifstream::pos_type fileSize = ifs.tellg();
    ifs.seekg(0, std::ios::beg);

    // load file contents into bytes vector
    std::vector<char> bytes(fileSize);
    ifs.read(&bytes[0], fileSize);

    // return as string
    return std::string(&bytes[0], fileSize);
}