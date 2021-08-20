from sys import stderr, exit
import re

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from magic_indexes_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="magic_indexes"
service="spot_magic_indexes_server"
args_list = [
    ('input_vector',str),
    ('magic_indexes',str),
    ('feedback',str),
    ('lang',str),
]


ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
vec = ENV['input_vector'].split(',')
vec = list(map(int, vec))
ans = ENV['magic_indexes'].split(',')
if ans[0]=='':
    ans=[]
else:
    ans = list(map(int, ans))
check_input_vector(vec, TAc, LANG)
check_input_vector(ans, TAc, LANG)
risp_correct = spot_magic_index(vec)

ok = (ans == risp_correct)
if not ok or not ENV['feedback'] == 'silent':
    TAc.print(LANG.render_feedback("input_vector", f'Your vector: [{ENV["input_vector"]}] '), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("magic_indexes", f'Your answer: [{ENV["magic_indexes"]}] '), "yellow", ["bold"])
    if not ok:
        if ENV['feedback'] == 'yes_no':
            TAc.print(LANG.render_feedback("wrong answer", f'No ._. Some problems with your magic_indexes. Remember the indexes start from 0.'), "red", ["bold"])
            #with Emoji: TAc.print(LANG.render_feedback("wrong answer", f'No \U0001F644. Some problems with your magic_indexes. Remember the indexes start from 0.', "red", ["bold"])
        elif ENV['feedback'] == 'gimme_one_wrong':
            if len(risp_correct) > len(ans):
                missing = [item for item in risp_correct if item not in ans]
                TAc.print(LANG.render_feedback("wrong answer", f'Good try :( However, you missed the magic index {missing[0]}.'), "red", ["bold"])
                #with Emoji: TAc.print(LANG.render_feedback("wrong answer", f'Good try \U0001F62C! However, you missed the magic index {missing[0]}.'), "red", ["bold"])
            else:
                wrong = [item for item in ans if item not in risp_correct]
                TAc.print(LANG.render_feedback("wrong answer", f'Good try :( However, {wrong[0]} is not a magic index!'), "red", ["bold"])
                #with Emoji: TAc.print(LANG.render_feedback("wrong answer", f'Good try \U0001F62C! However, {wrong[0]} is not a magic index!'), "red", ["bold"])
elif not ENV['feedback'] == 'silent':
    TAc.print(LANG.render_feedback("correct answer", f'Correct :D. '), "green", ["bold"])
    #with Emoji: TAc.print(LANG.render_feedback("correct answer", f'Correct \U0001F929! The magic index/indexes list for the vector [{ENV["input_vector"]}] is [{ENV["magic_indexes"]}]. '), "green", ["bold"])

exit(0)

