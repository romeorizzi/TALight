import sys
from chococroc_lib import build_table
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="check_is_losing"
args_list = [
    ('m',int),
    ('n',int),
    ('value',bool),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#print(f"# I will serve: problem=chococroc, service=check_is_losing")


# START CODING YOUR SERVICE:
rowM = ENV['m']
columnN = ENV['n']
value = ENV['value']
silent = ENV['silent']
lang = ENV['lang']

table = build_table(rowM, columnN)
"""COMMENTO PERSONALE: Ho una tabella 2x3: se printo la tabella in posizione [-1]
mi torna la seconda riga mentre se printo la tabella in posizione [-2]
mi torna la prima riga.
Se printo la tabella in posizione [-1] mi torna l'ultima riga.
Se printo la tabella in posizione [-2] mi torna la penultima riga.
Se printo la tabella in posizione [-1][-1] mi torna l'ultimo elemento
dell'ultima riga della tabella.
Se printo la tabella in posizione [-1][-2] mi torna il penultimo elemento
dell'ultima riga della tabella."""

"""se silent è posto a 1 stampiamo solo la scritta falso quando la scommessa viene
persa e non stampiamo niente quando invece è vincente, mentre se è posto a 0 allora
stampiamo la scritta vinto quando si vince la scommessa e perso quando si perde."""

if((table[rowM-1][columnN-1]) == 2 and silent == 0):
    TAc.OK()
    TAc.print(LANG.render_feedback("winning game", f'Your configuration {rowM} x {columnN} is a losing one.'), "yellow", ["bold"])
elif((table[rowM-1][columnN-1]) == 1):
    TAc.print(LANG.render_feedback("lost game", f"Your configuration {rowM} x {columnN} is a winning one."), "red", ["bold"])


exit(0)

