#!/usr/bin/env python3
from sys import exit,stdout, stderr
import os

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

PRIVATE_KEY=Ed25519PrivateKey.from_private_bytes(open('FILE_CON_CHIAVE_PRIVATA','rb').read())

original_file_as_binary = open('original_file.txt','rb').read()

with open('original_file.txt.sig','wb') as fout:
    fout.write(PRIVATE_KEY.sign(original_file_as_binary))

    
n = 23
n_as_bin_string = (f"{n}".zfill(3)).encode()

with open('numbered_file.txt.sig','wb') as fout:
    fout.write(PRIVATE_KEY.sign(original_file_as_binary + n_as_bin_string))


exit(0)
