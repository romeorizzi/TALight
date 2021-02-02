#!/usr/bin/env python3

from os import environ
from sys import exit

#ENV_lang = environ["TAL_lang"]
#ENV_s = environ["TAL_clean_string"]
ENV_s = None

def rabin_karp(ASCII_string):
    hash = 0
    for i in range(len(ASCII_string)):
        hash = ( hash * 257 + ord(ASCII_string[i]) ) & ((1 << 64) -1)
    return hash

if ENV_s != None:
    print(f"h({ENV_s})=\n{rabin_karp(ENV_s)}")
else:
    print("Poichè non hai specificato il parametro 'clean_string', ti chiediamo di immettere ora la stringa in chiaro, di cui computare l'hash:");
    str=input()
    print(f"h({str})=\n{rabin_karp(str)}")
    
exit(0)
