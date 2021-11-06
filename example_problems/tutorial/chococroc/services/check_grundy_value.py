import sys
from chococroc_lib import get_grundy_value
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="check_grundy_value"
args_list = [
    ('m',int),
    ('n',int),
    ('value',int),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#print(f"# I will serve: problem=chococroc, service=check_grundy_value")


# START CODING YOUR SERVICE:
rowM = ENV['m']
columnN = ENV['n']
value = ENV['value']
silent = ENV['silent']
lang = ENV['lang']

tableGrundy = get_grundy_value(rowM, columnN)


"""se silent è posto a 1 stampiamo solo la scritta falso quando la scommessa viene
persa e non stampiamo niente quando invece è vincente, mentre se è posto a 0 allora
stampiamo la scritta vinto quando si vince la scommessa e perso quando si perde."""


if((tableGrundy[rowM-1][columnN-1]) == value and silent == 0):
    TAc.OK()
    TAc.print(LANG.render_feedback("winning value", f'You are guessing the grundy value for the bar of {rowM} rows and {columnN} columns.'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("losing value.", f"You are not guessing the grundy value for the bar of {rowM} rows and {columnN} columns."), "red", ["bold"])

exit(0)


