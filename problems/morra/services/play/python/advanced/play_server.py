#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="morra"
service="play"
args_list = [
    ('num_rounds',int),
    ('hash_type',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
import string 
import random

from hash_and_cipher import hash_value

from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:


score_mine = 0
score_yours = 0
cheated = 0
for i in range(1,ENV['num_rounds']+1):
    TAc.print(f"?", "yellow", ["bold"])
    m = random.randrange(5)
    s = m + random.randrange(5)
    alphabet_string = string.ascii_letters + string.digits
    white_string_mine = chr(m+ord("0")) + "_" + chr(s+ord("0")) + "_" + ''.join(random.choices(alphabet_string, k=60))
    hash_str_mine = str(hash_value(white_string_mine,ENV['hash_type']))
    TAc.print(f"{hash_str_mine}", "yellow", ["bold"])
    hash_str_yours = input().strip()
    while hash_str_yours[0] == '#':
        hash_str_yours = input().strip()
    TAc.print(f"{white_string_mine}", "yellow", ["bold"])
    white_str_yours = input().strip()
    while white_str_yours[0] == '#':
        white_str_yours = input().strip()
    should_be = str(hash_value(white_str_yours,ENV['hash_type']))
    if hash_str_yours != should_be:
        TAc.print("No! ", "red", ["blink", "bold"], end="")
        TAc.print(LANG.render_feedback("you-cheated", f"You tried to cheat: h({white_str_yours}) = {should_be} != {hash_str_yours}."), "yellow", ["underline"])
        score_mine += 10
        cheated += 1
    else:
        m_yours = ord(hash_str_yours[0])-ord("0")
        s_yours = ord(hash_str_yours[2])-ord("0")                       
        if s_yours == m + m_yours:
            score_yours += 1                  
        if s == m + m_yours:
            score_mine += 1                  

TAc.print(LANG.render_feedback("summary", f"Your score: {score_yours}. My score: {score_mine}. You cheated {cheated} times."), "white", ["underline"])        
            
exit(0)
