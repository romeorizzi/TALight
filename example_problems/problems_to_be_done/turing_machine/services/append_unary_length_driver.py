#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange
from os import environ
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import random
import turing_machine_lib as tr


def iterationSeq(line):
    for i in range(int(line)):
        print("Sequenza numero " + str(i) + "\n")
        sequence = tr.random_seq(ENV['seed'] + i, ENV['max_lengh'])
        validation(sequence)


def validation(sequence):

    # TODO:
    # X movimento sul nastro
    #converti gli elementi di sequence in stringhe
    for i in range(len(sequence)):
        sequence[i] = str(sequence[i])

    print("\nSequenza iniziale: ", end="")
    for i in sequence:
        print(i, end="")
    print("\n")
    final_sequence = tr.tick(rules, sequence)
    print("Sequenza finale: ", end="")
    for i in final_sequence:
        print(i, end="")
    print("\n")
    length = len(sequence)
    new_sequence = ["#"]
    for i in range(length):
        new_sequence.append("1")
    if final_sequence == new_sequence:
        print("Risultato corretto! Bravo!\n")
    else:
        print(len(final_sequence))
        print(len(new_sequence))
        print("Risultato errato: il risultato finale dovrebbe essere la sequenza formata da uno # seguito da tanti 1 quanti la lunghezza della stringa iniziale\n")
        print("Risultato atteso: ", end="")
        for i in new_sequence:
            print(i, end="")
        print("\n")





# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('max_lengh',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# X TODO: Corregere l'output del problema,dando prima la definizione del problema e poi la stringa d'esempio

# START CODING YOUR SERVICE: 
LANG.print_opening_msg()

print("\nProblema: scrivere le istruzioni per una macchina di Turing che,\ndata una sequenza di caratteri binaria,\nscorre tutta la sequenza e aggiunge uno # alla fine della stringa,\npoi una sequenza di 1 lunga quanto la stringa data, eliminando la stringa iniziale")

#TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
#TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])

#catch input while the string isn't stop
print("\nInserisci la tua soluzione, un'istruzione per ogni riga premendo invio.\nQuando hai finito, scrivi stop e premi invio")
text = ""
while True:
    line = input()
    if line.lower() == 'stop':
        break
    text += (line + "\n")
#print("\nLa tua soluzione:")
#print(text)
rules = tr.getRules(text)
#print("\nRegole generate:")
#print(rules)

# X TODO: aggiungere la possibilità di inserire una sequenza di input

print("\nVuoi inserire una sequenza di input? (s/n)")

while True:
    line = input()
    if line.lower() == 's':
        print("\nInserisci la sequenza di input binaria:")
        while True:
            line = input()
            if line == '':
                break
            for c in line:
                if c not in '01':
                    print("\nErrore! Inserisci una sequenza binaria corretta:")
                    break
            else:
                validation(list(line))
                break
        break
    elif line.lower() == 'n':
        print("\nSu quante sequenze vuoi testare la tua soluzione?")
        while True:
            line = input()
            if line == '':
                break
            for c in line:
                if c not in '0123456789':
                    print("\nErrore! Inserisci un numero:")
                    break
            else:
                iterationSeq(line)
                break
        break
    else:
        print("\nInserisci una risposta valida (s/n)")
 
exit(0)





# Possibile soluzione
# (0, 0, 0, 0, >)
# (0, 1, 0, 1, >)
# (0, -, A, #, <)
# (A, 0, A, 0, <)
# (A, 1, A, 1, <)
# (A, #, A, #, <)
# (A, -, B, -, >)
# (B, 0, C, -, >)
# (B, 1, C, -, >)
# (C, 0, C, 0, >)
# (C, 1, C, 1, >)
# (C, #, C, #, >)
# (C, -, A, 1, <)
# (B, #, F, #, -)
# stop