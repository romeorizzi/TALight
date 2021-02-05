#!/usr/bin/env python3

from os import environ
from sys import exit
import string 
import random

from multilanguage import *
from hash_and_cipher import hash_value

ENV_lang = environ.get("TAL_lang")
ENV_num_checks = int(environ.get("TAL_num_checks"))
ENV_hash_type = environ.get("TAL_hash_type")
ENV_alphabet_white_string = environ.get("TAL_alphabet_white_string")
ENV_length_white_string = int(environ.get("TAL_length_white_string"))
ENV_colored_feedback = (environ.get("TAL_ISATTY") == "1")
    
set_colors(ENV_colored_feedback)
messages_book = select_book_and_lang("verify_hash_server", ENV_lang)

def print_lang(msg_code, *msg_rendering, **kwargs):
    msg_text=eval(f"f'{messages_book[msg_code]}'")
    TAcprint(msg_text, *msg_rendering, **kwargs)

        

print_lang("open-channel", "green")        
#English: print(f"# I will serve: problem=morra, service=verify_hash, num_checks={ENV_num_checks}, hash_type={ENV_hash_type}, alphabet_white_string={ENV_alphabet_white_string}, length_white_string={ENV_length_white_string}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

for i in range(1,ENV_num_checks+1):
    if ENV_alphabet_white_string == "safely_printable":
        alphabet_string = string.ascii_letters + string.digits + string.punctuation
    else:
        alphabet_string = getattr(string, ENV_alphabet_white_string)
    white_string = ''.join(random.choices(alphabet_string, k=ENV_length_white_string))
    print_lang("prompt", "yellow")
    #English: print("Please, compute and send me the hash of the following string:");
    print_lang("put-white-string", "yellow", ["bold"])
    #All-languages: print("{white_string}");
    hash_str_submitted=input()
    hash_str_true=hash_value(white_string,ENV_hash_type)
    if hash_str_submitted==hash_str_true:
        TAcOK()
        print_lang("give-hash-verbose", "grey")
        #English: print(f"indeed, h({white_string}) = {hash_value(white_string,ENV_hash_type)}")
    else:
        TAcNO()
        print_lang("give-hash-verbose", "yellow", ["underline"])
        #English: print(f"indeed, h({white_string}) = {hash_value(white_string,ENV_hash_type)}")
        exit(0)
    
exit(0)
