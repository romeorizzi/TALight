#!/usr/bin/env python3

from os import environ

def main():
    numero = environ['TAL_num']
    print(numero)

if __name__ == "__main__":
    main()
