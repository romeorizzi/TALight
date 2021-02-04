#!/usr/bin/env python3

from os import environ
from sys import exit
from hash_rabin_karp import rabin_karp 

from multilanguage import *

ENV_lang = environ.get("TAL_lang")
ENV_white_string = environ.get("TAL_white_string")
ENV_hash_type = environ.get("TAL_hash_type")
ENV_colored_feedback = (environ.get("TAL_ISATTY") == "1")

set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("compute_hash_server", ENV_lang)

def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)

        

if ENV_white_string not in {None, "None"}:
    print_lang("give-only-hash", "yellow", "on_blue")
    #All-languages: print(f"{rabin_karp(ENV_white_string)}")
else:
    print_lang("open-channel", "green", "on_blue")        
    #English: print(f"# I will serve: problem=morra, service=compute_hash, white_string={ENV_white_string}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

    print_lang("ask-for-white-string", "yellow", "on_blue", ["bold"])
    #English: print("Since the parameter white_string was not specified in this call, we now ask you to insert the string in white, of which to compute the hash:");
    str=input()
    print_lang("give-hash-verbose", "yellow", "on_blue")
    #All-languages: print(f"h({str}) = {rabin_karp(str)}")
    
exit(0)
