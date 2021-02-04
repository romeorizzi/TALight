def rabin_karp(ASCII_string):
    hash = 0
    for i in range(len(ASCII_string)):
        hash = ( hash * 257 + ord(ASCII_string[i]) ) & ((1 << 64) -1)
    return hash

