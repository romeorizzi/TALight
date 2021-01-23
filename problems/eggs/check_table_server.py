#!/usr/bin/env python3

from os import environ
import yaml
from sys import exit
from random import randrange

ENV_lang = environ["TAL_lang"]
ENV_n_eggs = int(environ["TAL_n_eggs"])
ENV_n_floors = int(environ["TAL_n_floors"])

with open("check_table_server." + ENV_lang + ".yaml", 'r') as stream:
    try:
        api = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

tmpstr=api["open-channel"]
print(eval(f"f'{tmpstr}'"))
#print(f"# I will serve: problem=eggs, service=check_table, n_eggs={ENV_n_eggs}, n_floors={ENV_n_floors}, lang={ENV_lang}.")

table_submitted = []
for u in range(ENV_n_eggs):
    table_submitted.append(map(int,input().strip().split(" ")))

for row in table_submitted:
    for ele in row:
        print(ele)    
exit(0)
