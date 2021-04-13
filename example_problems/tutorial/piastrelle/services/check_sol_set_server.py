#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from piastrelle_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="piastrelle"
service="check_sol_set"
args_list = [
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
stopping_command_set={'#end'}
print("# waiting for your set of well-formed tilings.\nPlease, each tiling should go on a different line and each line should have the same length and comprise only '[' or ']' or '-' characters.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

line = None
while line == None:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\[|\]|-)*$", regex_explained="any string comprising of '[' and ']' characters.", TAc=TAc)
    if line == "#end":
        TAc.print(LANG.render_feedback("at-least-one-line", f"No. You are required to enter at least one valid formula before closing."), "yellow")
        
input_solution_list = [line]
input_solution_set = {line}
if not recognize(input_solution_list[-1], TAc, LANG):
    TAc.print(LANG.render_feedback("first-line-not-well-formed", f"No. Your very first tiling is not well formed."), "red", ["bold"])
    exit(0)
len_lines = len(line)
n_tiles = len_lines//2
p=Par(n_tiles)
while True:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\[|\]|-)+$", regex_explained="any string of '[' , ')' and '-' characters.", TAc=TAc)
    if line in stopping_command_set:
        break
    if not len(line) == len_lines:
        TAc.print(LANG.render_feedback("different_lengths", f"No. The tiling you just introduced (your line {len(input_solution_list)+1}) is different in length from the previous ones."), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if line in input_solution_set:
        TAc.print(LANG.render_feedback("repeated", f"No. The well-formed tiling you just introduced (your line {len(input_solution_list)+1}) is the same as the entry number {input_solution_list.index(line)+1}."), "red", ["bold"])
    input_solution_set.add(line)
    input_solution_list.append(line)

print("# FILE GOT")
TAc.print(LANG.render_feedback("your-formulas-all-ok", f"All the tilings you have introduced are ok (well formed)."), "green")
input_solution_list.sort(reverse=True)
#print(input_solution_list)
if len(input_solution_list) < p.num_sol(n_tiles) and ENV['feedback'] == "yes_no":
    TAc.print(LANG.render_feedback("one-formula-is-missing-no-feedback", f"No. Your set is missing at least one well-formed tiling."), "red", ["bold"])
    exit(0)
missing='empty'
def answer():
    if ENV['feedback'] == "give_one_missing":
        TAc.print(LANG.render_feedback("one-formula-is-missing-no-feedback", f"No. Your set is missing at least one well-formed tiling.\nConsider for example:"), "red", ["bold"])
        TAc.print(missing, "yellow", ["bold"])
    else:
        assert ENV['feedback'] == "tell_a_minimal_missing_prefix"
        min_len1 = 0
        if pos > 0:
            while missing[min_len1] == input_solution_list[pos-1][min_len1]:
                min_len1 += 1
        min_len2 = 0
        if pos < len(input_solution_list):
            while missing[min_len2] == input_solution_list[pos][min_len2]:
                min_len2 += 1
        minimal_missing_prefix = missing[0:1+max(min_len1,min_len2)]
        TAc.print(LANG.render_feedback("one-missing-minimal-prefix", f"No. Your set is missing at least one well-formed tiling.\nHere is the prefix of a well-formed formula and no formula in your set has this prefix:"), "red", ["bold"])
        TAc.print(minimal_missing_prefix, "yellow", ["bold"])
    exit(0)

for pos in range(1,len(input_solution_list)+1):
    #print(f"pos={pos}, input_solution_list[pos]={input_solution_list[pos]}, p.unrank(n_tiles)={p.unrank(n_tiles,pos,'loves_short_tiles')}")
    correct=p.unrank(n_tiles,pos,'loves_short_tiles')
    if input_solution_list[pos-1] != correct:
        missing = correct
        answer()
if missing=='empty' and len(input_solution_list) < p.num_sol(n_tiles):
    missing=p.unrank(n_tiles,pos+1,'loves_short_tiles')
    answer()
TAc.OK()
TAc.print(f"Congrats! You have input all the well-formed tilings of a corridor of dimension 1x{n_tiles}.", "green")
exit(0)
