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
print("# waiting for your set of well-formed tilings.\nPlease, each tiling should go on a different line and is a sequence over the set {'[]', '[--]'} of allowed tiles. Each line should have the same length.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in this TAL_util at the 'rtal connect' command, like you would do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

line = None
while line == None:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\[|\]|-)+$", regex_explained="any string of '[' , ']' and '-' characters (actually, more precisely, any string on the alphabet {'[]', '[--]'}).", line_recognizer=recognize, TAc=TAc, LANG=LANG)
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
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\[|\]|-)+$", regex_explained="any string of '[' , ']' and '-' characters (actually, more precisely, any string on the alphabet {'[]', '[--]'}).", line_recognizer=recognize, TAc=TAc, LANG=LANG)
    if line in stopping_command_set:
        break
    if line == None:
        continue
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
    elif ENV['feedback'] == "tell_a_minimal_missing_prefix":
        pos1 = 0
        if rank > 0:
            while missing[pos1] == input_solution_list[rank-2][pos1]:
                pos1 += 1
        pos2 = 0
        if rank < len(input_solution_list):
            while missing[pos2] == input_solution_list[rank-1][pos2]:
                pos2 += 1
        last_char = max(pos1,pos2)
        print(last_char)
        while missing[last_char]!=']':
            last_char += 1
        print(last_char)
        minimal_missing_prefix = missing[0:last_char+1]
        TAc.print(LANG.render_feedback("one-missing-minimal-prefix", f"No. Your set is missing at least one well-formed tiling.\nHere is the prefix of a well-formed formula that is missing from the set you entered:"), "red", ["bold"])
        TAc.print(minimal_missing_prefix, "yellow", ["bold"])
    else:
        assert ENV['feedback'][0:27] == "tell_prefix_of_missing_len_"
        length = int(ENV['feedback'][27:])
        missing_prefix = missing[0:length]
        TAc.print(LANG.render_feedback("one-missing-prefix-length", f"No. Your set is missing at least one well-formed tiling.\nHere is the prefix of length {length} of a well-formed formula that is missing from the set you entered:"), "red", ["bold"])
        TAc.print(missing_prefix, "yellow", ["bold"])
    exit(0)

for rank in range(1,len(input_solution_list)+1):
    #print(f"rank={rank}, input_solution_list[rank]={input_solution_list[rank]}, p.unrank(n_tiles)={p.unrank(n_tiles,rank,'loves_short_tiles')}")
    correct=p.unrank(n_tiles,rank,'loves_short_tiles')
    if input_solution_list[rank-1] != correct:
        missing = correct
        answer()
if missing=='empty' and len(input_solution_list) < p.num_sol(n_tiles):
    missing=p.unrank(n_tiles,rank+1,'loves_short_tiles')
    answer()
TAc.OK()
TAc.print(f"Congrats! You have input all the well-formed tilings of a corridor of dimension 1x{n_tiles}.", "green")
exit(0)
