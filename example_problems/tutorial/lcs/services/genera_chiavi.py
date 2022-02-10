#!/usr/bin/env python3
from sys import exit,stdout, stderr
import os

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

with open('FILE_CON_CHIAVE_PRIVATA','wb') as fout:
    fout.write(Ed25519PrivateKey.generate().private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()))

exit(0)
