#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange
from os import environ
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import random
import turing_machine_lib as tr
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('max_lengh',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE: 
LANG.print_opening_msg()
sequence = tr.random_seq(ENV['seed'], ENV['max_lengh'])

#TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
print("\nSequenza: ", end="")
#converti gli elementi di sequence in stringhe
for i in range(len(sequence)):
    sequence[i] = str(sequence[i])
for i in sequence:
    print(i, end="")
print("\n")
#TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
#catch input while the string isn't stop
print("Inserisci la tua soluzione, un'istruzione per ogni riga premendo invio.\nQuando hai finito, scrivi stop e premi invio")
text = ""
while True:
    line = input()
    if line.lower() == 'stop':
        break
    text += (line + "\n")
print("\nLa tua soluzione:")
print(text)
rules = tr.getRules(text)
print("\nRegole generate:")
print(rules)


# TODO:
# X movimento sul nastro
final_sequence = tr.tick(rules, sequence)
print("\nSequenza finale: ", end="")
for i in final_sequence:
    print(i, end="\n")
new_sequence = sequence.copy()
new_sequence.append('1')
if final_sequence == new_sequence:
    print("Risultato corretto! Bravo!\n")
else:
    print("Risultato errato: il risultato finale dovrebbe essere la sequenza binaria iniziale con un 1 aggiunto alla fine\n")


 
exit(0)




# Possibile soluzione
# (0, 0, 0, 0, >)
# (0, 1, 0, 1, >)
# (0, -, F, 1, -)
