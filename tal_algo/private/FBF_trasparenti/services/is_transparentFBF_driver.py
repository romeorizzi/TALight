#!/usr/bin/env python3
from sys import stderr, exit
from os import environ

from FBF_trasparenti_lib import recognize

is_FBF, is_transparent = recognize(environ["TAL_FBF"])
if not is_FBF:
        print(f'No. Your formula of parentheses is NOT an FBF.')
        exit(0)
len_input = len(environ["TAL_FBF"])
assert len_input % 2 == 0
print(f'OK. First positive confirm: Your string is indeed a well-formed formula (FBF). It has {len_input//2} pairs of parentheses.')
if not is_transparent:
    print(f'No. Your FBF is NOT transparent.')
    exit(0)
print(f'OK. Second positive confirm: Your FBF is indeed transparent.')

