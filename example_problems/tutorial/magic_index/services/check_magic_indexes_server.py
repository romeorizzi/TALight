from sys import stderr, exit, argv
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="magic_indexes"
service="spot_magic_indexes_server"
args_list = [
    ('input_vector',str),
    ('input_list',str),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]


ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
vec = ENV['input_vector'].split(',')
vec = list(map(int, vec))
ans = ENV['input_list'].split(',')
ans = list(map(int, ans))
check_input_vector(vec, TAc, LANG)
check_input_vector(ans, TAc, LANG)

#risp_correct = spot_magic_index(vec)
risp_correct = spot_magic_index(vec)

TAc.print(LANG.render_feedback("input_vector", f'Your vector: [{ENV["input_vector"]}] '), "yellow", ["bold"])
TAc.print(LANG.render_feedback("input_list", f'Your answer: [{ENV["input_list"]}] '), "yellow", ["bold"])



if ans != risp_correct and ENV['feedback'] == 'silent':
    TAc.print(LANG.render_feedback("wrong answer", f'Some problems with your magic_indexes list [{ENV["input_list"]}] .-.'), "red", ["bold"])
    #TAc.print(LANG.render_feedback("wrong answer", f'Some problems with your magic_indexes list [{ENV["input_list"]}] \U0001F644!'), "red", ["bold"])
    exit(0)
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

