#!/usr/bin/env python3

from os import environ
from sys import exit
import string 
import random

from multilanguage import *
from hash_and_cipher import hash_value

ENV_lang = environ.get("TAL_lang")
ENV_num_rounds = int(environ.get("TAL_num_rounds"))
ENV_hash_type = environ.get("TAL_hash_type")
ENV_colored_feedback = (environ.get("TAL_ISATTY") == "1")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("play_server", ENV_lang)
        
def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)

        

print_lang("open-channel", "green")        
#English: print(f"# I will serve: problem=morra, service=play, num_rounds={ENV_num_rounds}, hash_type={ENV_hash_type}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

score_mine = 0
score_yours = 0
cheated = 0
for i in range(1,ENV_num_rounds+1):
    TAcprint(f"?", "yellow", ["bold"])
    m = random.randrange(5)
    s = m + random.randrange(5)
    alphabet_string = string.ascii_letters + string.digits
    white_string_mine = chr(m+ord("0")) + "_" + chr(s+ord("0")) + "_" + ''.join(random.choices(alphabet_string, k=60))
    hash_str_mine = str(hash_value(white_string_mine,ENV_hash_type))
    TAcprint(f"{hash_str_mine}", "yellow", ["bold"])
    hash_str_yours = input().strip()
    while hash_str_yours[0] == '#':
        hash_str_yours = input().strip()
    TAcprint(f"{white_string_mine}", "yellow", ["bold"])
    white_str_yours = input().strip()
    while white_str_yours[0] == '#':
        white_str_yours = input().strip()
    should_be = str(hash_value(white_str_yours,ENV_hash_type))
    if hash_str_yours != should_be:
        TAcprint("No! ", "red", ["blink", "bold"], end="")
        print_lang("you-cheated", "yellow", ["underline"])        
        #English: print(f"You tried to cheat: h({white_str_yours}) = {should_be} != {hash_str_yours}.")
        score_mine += 10
        cheated += 1
    else:
        m_yours = ord(hash_str_yours[0])-ord("0")
        s_yours = ord(hash_str_yours[2])-ord("0")                       
        if s_yours == m + m_yours:
            score_yours += 1                  
        if s == m + m_yours:
            score_mine += 1                  

print_lang("summary", "white", ["underline"])        
#English: print(f"Your score: {score_yours}. My score: {score_mine}. You cheated {cheated} times.")
            
exit(0)
