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

correct_worst_answer = check_n_questions_worst_case(n) #verifica

TAc.print(LANG.render_feedback("n", f'Your vector lenght: [{ENV["n"]}] '), "yellow", ["bold"])
TAc.print(LANG.render_feedback("risp", f'Your minimum question number in the worst case: [{ENV["risp"]}] '), "yellow", ["bold"])

if risp != correct_worst_answer and ENV['silent'] == True:
    TAc.print(LANG.render_feedback("wrong answer", f'Some problems with your question number {ENV["risp"]} .-.'), "red", ["bold"])
    exit(0)
'''
elif ans != risp_correct and ENV['feedback'] == 'yes_no':
    TAc.print(LANG.render_feedback("wrong answer", f'No ._." Unfortunately you entered the wrong magic indexes for the vector [{ENV["input_vector"]}]. Remember the indexes start from 0...'), "red", ["bold"])
    #TAc.print(LANG.render_feedback("wrong answer", f'No \U0001F62C! Unfortunately you entered the wrong magic indexes for the vector [{ENV["input_vector"]}]. Remember the indexes start from 0...'), "red", ["bold"])
    exit(0)
elif ans != risp_correct and ENV['feedback'] == 'gimme_one_wrong':
    if len(risp_correct) > len(ans):
        TAc.print(LANG.render_feedback("wrong answer", f'Good try :\'c Unfortunately you entered too few magic indexes for the vector [{ENV["input_vector"]}].'), "red", ["bold"])
        #TAc.print(LANG.render_feedback("wrong answer", f'Good try \U0001F62C! Unfortunately you entered too few magic indexes for the vector [{ENV["input_vector"]}].'), "red", ["bold"])
        exit(0)
    else:
        wrong = [item for item in ans if item not in risp_correct]
        TAc.print(LANG.render_feedback("wrong answer", f'Good try :C Unfortunately you entered the wrong magic indexes for the vector [{ENV["input_vector"]}]. {wrong[0]} is not a magic index!'), "red", ["bold"])
        #TAc.print(LANG.render_feedback("wrong answer", f'Good try \U0001F62C! Unfortunately you entered the wrong magic indexes for the vector [{ENV["input_vector"]}]. {wrong[0]} is not a magic index!'), "red", ["bold"])
        exit(0)
else:
    TAc.print(LANG.render_feedback("correct answer", f'Correct :D The magic index/indexes list for the vector [{ENV["input_vector"]}] is [{ENV["input_list"]}]. '), "green", ["bold"])
    #TAc.print(LANG.render_feedback("correct answer", f'Correct \U0001F929! The magic index/indexes list for the vector [{ENV["input_vector"]}] is [{ENV["input_list"]}]. '), "green", ["bold"])
    exit(0)
'''
