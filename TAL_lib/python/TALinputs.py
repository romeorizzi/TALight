#!/usr/bin/env python3
from sys import stderr, exit
import re

def try_to_convert(tk, tk_type):
    if tk_type == "int":
        try: 
            risp = int(tk)
            return risp
        except (TypeError, ValueError):
            return None
    elif tk_type == "float":
        try: 
            risp = float(tk)
            return risp
        except (TypeError, ValueError):
            return None
    elif tk_type[0] == "str_token":
        matched = re.match("[a-z][0-9][a-z][0-9]+", test_string)
        if bool(matched):
            return tk
        else:
            return None
    else:
        print(f"Internal error (please, report it to the problem maker): the TALinputs library does not support the '{tk_type}' token type. The problem maker should either extend the library or adapt to it.", file=stderr)
        exit(1)
        


def TALinput(tokens_type, ignore_lines_starting_with='#'):
    spoon = input()
    while spoon[0] == ignore_lines_starting_with:
        spoon = input()
    tokens = spoon.split() 
    if len(tokens) != len(tokens_type):
        print(f"Input error: the server was expecting a line with {len(tokens_type)} tokens but the line you entered:\n{spoon}\ncontains {len(tokens)} != {len(tokens_type)} tokens.\n\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=stderr)
        exit(1)
    vals = []
    for tk, tk_type in zip(tokens,tokens_type):
        vals.append(try_to_convert(tk, tk_type))
        if vals[-1] == None:
            print(f"Input error: the server was expecting a token of type {tk_type} when it got the token '{tk}'.\n\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=stderr)
            exit(1) 
    return (val for val in vals)
