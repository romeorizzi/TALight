def rabin_karp(ASCII_white_string):
    hash = 0
    for i in range(len(ASCII_white_string)):
        hash = ( hash * 257 + ord(ASCII_white_string[i]) ) & ((1 << 64) -1)
    return hash


def hash_value(white_str, hash_type):
    if hash_type == "rabin_karp":
        return rabin_karp(white_str)  # which returns a naural in [0,2**64): 
    else:
        import hashlib
        func_name=hash_type
        func_myhash = getattr(hashlib, func_name)
        result = func_myhash(white_str.encode()) 
        return result.hexdigest() 
