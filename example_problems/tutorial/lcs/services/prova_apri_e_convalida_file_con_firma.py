#!/usr/bin/env python3
from sys import exit,stdout, stderr
import os

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

PRIVATE_KEY=Ed25519PrivateKey.from_private_bytes(open('FILE_CON_CHIAVE_PRIVATA','rb').read())

PUBLIC_KEY=PRIVATE_KEY.public_key()

def verify_authenticity(pk,c,s):
    try:
        pk.verify(s,c)
    except:
        return False
    return True


original_file_as_binary = open('original_file.txt','rb').read()

original_file_signature = open('original_file.txt.sig','rb').read()

if verify_authenticity(pk=PUBLIC_KEY,c=original_file_as_binary,s=original_file_signature):
    print("The signature of the original file is valid.")
else:
    print("The signature of the original file is NOT valid.")


n = 23
n_as_bin_string = (f"{n}".zfill(3)).encode()

binary_file_after_numbering = original_file_as_binary + n_as_bin_string
numberedfile_signature = open('numbered_file.txt.sig','rb').read()

if verify_authenticity(pk=PUBLIC_KEY,c=binary_file_after_numbering,s=numberedfile_signature):
    print("The signature of the numbered file is valid.")
else:
    print("The signature of the numbered file is NOT valid.")

exit(0)
