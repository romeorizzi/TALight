uint64_t rabin_karp(const char* data) {
    uint64_t hash = 0;
    size_t size = strlen(data);
    for(size_t i = 0; i < size; i++) {
        hash = hash * 257ULL + data[i];
    }
    return hash;
}
