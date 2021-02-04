#include <string.h>
#include <inttypes.h>

uint64_t rabin_karp(const char* ASCII_string) {
    uint64_t hash = 0;
    size_t size = strlen(ASCII_string);
    for(size_t i = 0; i < size; i++) {
        hash = hash * 257ULL + ASCII_string[i];
    }
    return hash;
}
