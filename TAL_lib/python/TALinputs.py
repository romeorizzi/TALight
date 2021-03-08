#!/usr/bin/env python3
from sys import stdout, stderr, exit
import re

def try_to_convert(tk, tk_type, regex):
    if tk_type == int:
        try: 
            risp = int(tk)
            return risp
        except (TypeError, ValueError):
            return None
    elif tk_type == float:
        try: 
            risp = float(tk)
            return risp
        except (TypeError, ValueError):
            return None
    elif tk_type == str:
        if tk.upper() == "END":
            return "end"
        matched = re.match(regex, tk)
        if bool(matched):
            return tk
        else:
            return None
    else:
        for out in [stdout, stderr]:
            print(f"Internal error (please, report it to the problem maker): the TALinputs library does not support the '{tk_type}' token type. The problem maker should either extend the library or adapt to it.", file=out)
        exit(1)
        


def TALinput(tokens_type, regex="^((\S)+)$", regex_explained=None, ignore_lines_starting_with='#'):
    while True:
        spoon = input()
        if len(spoon) == 0:
            print(f"You have entered an unexpected empty line. I assume you want to drop this TALight service call. See you next time ;))")
            exit(0)
        if spoon[0] not in ignore_lines_starting_with:
            break
    tokens = spoon.split() 
    if len(tokens) != len(tokens_type):
        for out in [stdout, stderr]:
            print(f"Input error from the problem-solver: the server was expecting a line with {len(tokens_type)} tokens but the line you entered:\n{spoon}\ncontains {len(tokens)} != {len(tokens_type)} tokens.\n\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
        exit(0)
    vals = []
    for tk, tk_type, i in zip(tokens,tokens_type,range(1,1+len(tokens))):
        vals.append(try_to_convert(tk, tk_type,regex))
        if vals[-1] == None:
            if tk_type == str:
                for out in [stdout, stderr]:
                    print(f"Input error from the problem-solver:  when parsing the {i}-th token of your input line, namely the string:\n{tk}\nthe server was actually expecting a string matching the regex:\n{regex}\nbut the string you entered does not comply the regex.\n", file=out)
                    if regex_explained != None:
                        print(f"In practice, the expected string should be either 'end' (to close the input) or {regex_explained}", file=out)
                    print(f"\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
            else:
                for out in [stdout, stderr]:
                    print(f"Input error from the problem-solver: the server was expecting a token of type {tk_type} when it got the token '{tk}'.\n\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
            exit(1) 
    return (val for val in vals)
