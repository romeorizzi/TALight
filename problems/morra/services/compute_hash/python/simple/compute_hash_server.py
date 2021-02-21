#!/usr/bin/env python3

from os import environ
from sys import exit

from hash_and_cipher import hash_value

ENV['white_string'] = environ.get("TAL_white_string")
ENV['hash_type'] = environ.get("TAL_hash_type")
    

if ENV['white_string'] not in {None, "None"}:
    print(f"{hash_value(ENV['white_string'],ENV['hash_type'])}")
else:
    print(f"# I will serve: problem=morra, service=compute_hash, white_string={ENV['white_string']}, hash_type={ENV['hash_type']}.")

    print("Since the parameter white_string was not specified in this call, we now ask you to insert the string in white, of which to compute the hash:");
    white_str=input()
    print(f"h({white_str}) = {hash_value(white_str,ENV['hash_type'])}")
    
exit(0)
