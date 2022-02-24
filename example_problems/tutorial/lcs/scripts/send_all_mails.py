#!/usr/bin/python3
from sys import argv, exit, stderr
import os
from shutil import copyfile

from deadline import DEADLINE_STRING

# script che invia tutte le mail ai docenti per la richiesta di preferenze sugli assegnamenti dei tutor.
# script da lanciare dalla cartella:
# ~/commissioni/tutor
# dopo che lo script extract_table_from_docx.py ha creato le cartelle DEST_*

def usage(onstream):
    print("\nSono lo script che invia tutte le mail ai docenti per la richiesta di preferenze sugli assegnamenti dei tutor.\n\nUsage: %s  {SUDO | ME | SAY }\n\n   where the three alternative options are:\n   * SUDO: really act! Send all the mails to the person.\n   * ME: send all the mails but just to myself. In this way, I can have a look at a few mails before sending a ton of them.\n   * SAY: only tell the action in the gun but do not really take it." % os.path.basename(argv[0]), file=onstream)

# THE MAIN PROGRAM:
if len(argv) != 2 or argv[1] not in {"SUDO","ME","SAY"}:
    usage(stderr)
    exit(1)

if 'DEST_' in os.listdir():    
    os.rmdir('DEST_')
for dir in os.listdir():
    if dir[0:5] == 'DEST_':
        os.chdir(dir)
        datastring=dir[5:]
        print(f"\nopero nella cartella {dir} ossia su {datastring}:\n     ./sendMailWithTable.py '{argv[1]} {DEADLINE_STRING}'")
#        risp = os.system(f"./sendMailWithTable.py {argv[1]} '{DEADLINE_STRING}'")
        risp = os.system(f"python3 sendMailWithTable.py {argv[1]} '{DEADLINE_STRING}'")
        os.chdir('..')
