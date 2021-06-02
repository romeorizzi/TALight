from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="magic_indexes"
service="check_worst_case_num_questions"
args_list = [
    ('n',str),
    ('risp',str),
    ('more_or_less_hint_if_wrong',bool),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
n = int(ENV['n'])
risp = int(ENV['risp'])

correct_worst_answer = check_n_questions_worst_case(n)

TAc.print(LANG.render_feedback("n", f'Your vector lenght: [{ENV["n"]}] '), "yellow", ["bold"])
TAc.print(LANG.render_feedback("risp", f'Your minimum question number in the worst case: [{ENV["risp"]}] '), "yellow", ["bold"])

if risp != correct_worst_answer and ENV['silent'] == False and ENV['more_or_less_hint_if_wrong'] == True:
    if risp > correct_worst_answer:
        TAc.print(LANG.render_feedback("wrong answer", f'Some problems with your question number {ENV["risp"]}.\
        \nIt is possible to find all the magic indexes in less than {ENV["risp"]} questions'), "red", ["bold"])
        exit(0)
    elif risp < correct_worst_answer:
        TAc.print(LANG.render_feedback("wrong answer", f'Some problems with your question number {ENV["risp"]}.\
        \nIt is not possible to find all the magic indexes in exactly {ENV["risp"]} questions. You should make more queries.'), "red", ["bold"])
        exit(0)
elif risp != correct_worst_answer:
    TAc.print(LANG.render_feedback("wrong answer", f'Some problems with your question number {ENV["risp"]} .-.'), "red", ["bold"])
    exit(0)
elif risp == correct_worst_answer and ENV['silent'] == False:
    TAc.print(LANG.render_feedback("right answer", f'Your number of queries {ENV["risp"]} is correct! :D'), "green", ["bold"])
    exit(0)