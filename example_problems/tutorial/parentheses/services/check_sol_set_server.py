#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('feedback',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

stopping_command_set={"#end"}
print("#? waiting for your set of well-formed formulas of parentheses.\nPlease, each formula should go on a different line and each line should have the same length and comprise only '(' or ')' characters.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

p = Par(20)      
      
line = None
while line == None:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\(|\))*$", regex_explained="any string comprising of '(' and ')' characters.", TAc=TAc)
    if line == "#end":
        TAc.print(LANG.render_feedback("at-least-one-line", f'No. You are required to enter at least one valid formula before closing.'), "yellow")
        
input_solution_list = [line]
input_solution_set = {line}
if not recognize(input_solution_list[-1], TAc, LANG):
    TAc.print(LANG.render_feedback("first-line-not-well-formed", f'No. Your very first formula of parentheses is not well formed.'), "red", ["bold"])
    exit(0)
len_lines = len(line)
n_pairs = len_lines//2

while True:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters.", TAc=TAc)
    if line in stopping_command_set:
        break
    if not len(line) == len_lines:
        TAc.print(LANG.render_feedback("different_lengths", f'No. The parentheses formula you just introduced (your line {len(input_solution_list)+1}) is different in length from the previous ones.'), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if line in input_solution_set:
        TAc.print(LANG.render_feedback("repeated", f'No.The parentheses formula you just introduced (your line {len(input_solution_list)+1}) is the same as the one in line {input_solution_list.index(line)+1}. Nothing is lost: this double entry will be ignored. You can go on.'), "red", ["bold"])
    else:
        input_solution_set.add(line)
        input_solution_list.append(line)

print("# FILE GOT")
TAc.print(LANG.render_feedback("your-formulas-all-ok", f'All the formulas you have introduced are ok (well formed).'), "green")

input_solution_list.sort(reverse=True)
#print(input_solution_list)
if len(input_solution_list) == p.num_sol(n_pairs):
    TAc.OK()
    TAc.print(f'Congrats! You have input all the well-formed formulas of {n_pairs} pairs of parentheses.', "green")
    exit(0)
else:
    TAc.print(LANG.render_feedback("one-formula-is-missing-no-feedback", f'No. Your set is missing at least one well-formed formula.'), "red", ["bold"])
if ENV["feedback"] == "yes_no":
    exit(0)

missing='empty'
def answer():
    if ENV["feedback"] == "give_a_missing_sol":
        TAc.print(LANG.render_feedback("give-missing-formula", f'Consider for example:'), "red", ["bold"])
        TAc.print(missing, "yellow", ["bold"])
    elif ENV["feedback"] == "tell_minimal_missing_prefix" or ENV['feedback'] == "dispell_longest_seen_prefix_of_a_missing_sol":
        min_len1 = 0
        if rank > 0:
            while missing[min_len1] == input_solution_list[rank-1][min_len1]:
                min_len1 += 1
        min_len2 = 0
        if rank < len(input_solution_list):
            while missing[min_len2] == input_solution_list[rank][min_len2]:
                min_len2 += 1
        if ENV["feedback"] == "tell_minimal_missing_prefix":
            minimal_missing_prefix = missing[0:1+max(min_len1,min_len2)]
            TAc.print(LANG.render_feedback("first-missing-prefix", f'As a strong hint, here is the prefix of a well-formed formula and no formula in your list has this prefix:'), "red", ["bold"])
            TAc.print(minimal_missing_prefix, "yellow", ["bold"])
            exit(0)
        elif ENV['feedback'] == "dispell_longest_seen_prefix_of_a_missing_sol":
            #print(min_len1, min_len2)
            #print(input_solution_list[rank-1], input_solution_list[rank])
            if rank==len(input_solution_list)-1 and not case:
                TAc.print(LANG.render_feedback("not-consecutive(last)", f'In green you find the longest prefix that a solution you are missing has in common with a solution you have given:'), "red", ["bold"], end=" ")
            else:
                TAc.print(LANG.render_feedback("first-missing-till-already-present", f"In green you find the longest prefix that a solution you are missing has in common with a solution you have given:"), "red", ["bold"], end=" ")
            if min_len1>=min_len2:
                missing_prefix=input_solution_list[rank-1][:min_len1]
                suffix=input_solution_list[rank-1][min_len1:]
            else:
                missing_prefix=input_solution_list[rank][:min_len2]
                suffix=input_solution_list[rank][min_len2:]
            TAc.print(missing_prefix, "green", ["bold"], end='')
            TAc.print(suffix, "red", ["bold"])
    else:
        assert ENV['feedback'][0:29] == "tell_a_missing_prefix_of_len_"
        length = int(ENV['feedback'][29:])
        missing_prefix = missing[0:length]
        TAc.print(LANG.render_feedback("one-missing-prefix-length", f"\nHere is the prefix of length {length} of a well-formed formula that is missing from the set you entered:"), "red", ["bold"])
        TAc.print(missing_prefix, "yellow", ["bold"])

case=True
for rank in range(len(input_solution_list)):
    rank_g=p.num_sol(n_pairs)-rank-1
    #print(f"rank={rank}, input={input_solution_list[rank]}, giusta={p.unrank(n_pairs, rank_g)}")
    if input_solution_list[rank] != p.unrank(n_pairs, rank_g):
        missing = p.unrank(n_pairs, rank_g)
        answer()
        #print(f"\nmissing={missing}\n")
        exit(0)

if missing=='empty' and len(input_solution_list) < p.num_sol(n_pairs):
    case=False
    rank_g=p.num_sol(n_pairs)-rank-2
    missing = p.unrank(n_pairs, rank_g)
    #print(f"\nmissing={missing}\n")
    answer()
    exit(0)
