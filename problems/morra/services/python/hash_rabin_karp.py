def rabin_karp(ASCII_white_string):
    hash = 0
    for i in range(len(ASCII_white_string)):
        hash = ( hash * 257 + ord(ASCII_white_string[i]) ) & ((1 << 64) -1)
    return hash

