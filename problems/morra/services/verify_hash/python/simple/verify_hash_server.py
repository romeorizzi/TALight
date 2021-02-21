#!/usr/bin/env python3

from os import environ
from sys import stderr, exit
import string 
import random

from hash_and_cipher import hash_value

ENV['num_checks'] = int(environ.get("TAL_num_checks"))
ENV['hash_type'] = environ.get("TAL_hash_type")
ENV['alphabet_white_string'] = environ.get("TAL_alphabet_white_string")
ENV['length_white_string'] = int(environ.get("TAL_length_white_string"))
    
print(f"# I will serve: problem=morra, service=verify_hash, num_checks={ENV['num_checks']}, hash_type={ENV['hash_type']}, alphabet_white_string={ENV['alphabet_white_string']}, length_white_string={ENV['length_white_string']}.")

for i in range(1,ENV['num_checks']+1):
    if ENV['alphabet_white_string'] == "safely_printable":
        alphabet_string = string.ascii_letters + string.digits + string.punctuation
    else:
        alphabet_string = getattr(string, ENV['alphabet_white_string'])
    white_string = ''.join(random.choices(alphabet_string, k=ENV['length_white_string']))
    print("Please, compute and send me the hash of the following string:");
    print("{white_string}");
    hash_str_submitted=input()
    hash_str_true=hash_value(white_string,ENV['hash_type'])
    if hash_str_submitted==hash_str_true:
        print(f"Ok! indeed, h({white_string}) = {hash_value(white_string,ENV['hash_type'])}")
    else:
        print(f"No! indeed, h({white_string}) = {hash_value(white_string,ENV['hash_type'])}")
        exit(0)
    
exit(0)
