#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_sol_list"
args_list = [
    ('sorting_criterion',str),
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

stopping_command_set={"#end"}
print("# waiting for your ordered list of feasible treatments.\nPlease, each treatment should go on a different line and each line should have the same length and comprise only 'I' or 'H' characters.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

p = Flask(20)      

line = None
while line == None:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(I|H)*$", regex_explained="any string of 'I' and 'H' characters.", TAc=TAc)
    if line == "#end":
        TAc.print(LANG.render_feedback("at-least-one-line", f'No. You are required to enter at least one feasible treatment (possibly even the empty one) before closing.'), "yellow")
    
input_solution_list = [line]
if not recognize(input_solution_list[-1], TAc, LANG):
    TAc.print(LANG.render_feedback("first-line-not-feasible", f'No. Your very first treatment is NOT feasible.'), "red", ["bold"])
    exit(0)
len_lines = len(line)
n_pills = len_lines//2

if ENV["sorting_criterion"]=="lovesI":
    first='I' * n_pills + 'H' * n_pills
else:
    first='IH' * n_pills
if input_solution_list[-1] != first:
    TAc.print(LANG.render_feedback("wrong-first", f'No. The very first treatment you have introduced is feasible but it is not the first feasible treatment according to the order that has been set.'), "red", ["bold"], end=" ")
    print(LANG.render_feedback("called-with", '(service called with'), end=" ")
    TAc.print('sorting_criterion=', "red", end="")
    TAc.print(ENV["sorting_criterion"], "yellow", end="")
    print(').')
    exit(0)

while True:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(I|H)+$", regex_explained="any string of 'I' and 'H' characters.", TAc=TAc)
    if line in stopping_command_set:
        break
    if not len(line) == len_lines:
        TAc.print(LANG.render_feedback("different_lengths", f'No. The treatment you have just introduced in your line {len(input_solution_list)+1} has different length than the previous ones.'), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if (ENV["sorting_criterion"]=="lovesI" and line > input_solution_list[-1]) or (ENV["sorting_criterion"]=="lovesH" and line < input_solution_list[-1]):
        TAc.print(LANG.render_feedback("order-violation", f'No. The treatment you have just introduced in position {len(input_solution_list)+1} does not come after but rather before than the previous one according to the order set.'), "red", ["bold"], end=" ")
        print(LANG.render_feedback("called-with", '(service called with'), end=" ")
        TAc.print('sorting_criterion=', "red", end="")
        TAc.print(ENV["sorting_criterion"], "yellow", end="")
        print(').')
        exit(0)
    if line == input_solution_list[-1]:
        TAc.print(LANG.render_feedback("repeated", f'No. The treatment you have just introduced in your line {len(input_solution_list)+1} is the same as your {input_solution_list.index(line)+1}th one. But nothing is lost: this repetition will be ignored. You can go on.'), "red", ["bold"])
    else:
        input_solution_list.append(line)

print("# FILE GOT")
TAc.print(LANG.render_feedback("your-treatments-all-ok", f'All the treatments you have introduced are feasible and correctly ordered.'), "green")

#print(input_solution_list)

if len(input_solution_list) == p.num_sol(n_pills):
    TAc.OK()
    TAc.print(LANG.render_feedback("list-ok", f'You have listed all feasible treatments with {n_pills} pills. Also their order is the intended one.'), "green")
    exit(0)
else:
    TAc.print(LANG.render_feedback("one-treatment-is-missing-no-feedback", f'No. Your list is missing at least one feasible treatment.'), "red", ["bold"])
if ENV["feedback"] == "yes_no":
    exit(0)

for pos in range(p.num_sol(n_pills)):
    print(f"pos={pos}, input_solution_list[pos]={input_solution_list[pos]}, p.unrank(n_pills, pos)={p.unrank(n_pills, pos)}")
    if input_solution_list[pos] != p.unrank(n_pills, pos):
        missing = p.unrank(n_pills, pos)
        #print(f"missing={missing}")
        if ENV["feedback"] == "give_first_missing":
            TAc.print(LANG.render_feedback("give-missing-treatment", f'Consider for example:'), "red", ["bold"])
            TAc.print(missing, "yellow", ["bold"])
        if ENV["feedback"] == "spot_first_wrong_consec":
            assert pos > 0
            TAc.print(LANG.render_feedback("not-consecutive", f'In fact, the two feasible treatments:\n {input_solution_list[pos-1]}\n {input_solution_list[pos]}\nthat appear consecutive in your list are NOT consecutive in the intended order'), "red", ["bold"], end=" ")
            print(LANG.render_feedback("called-with", f'(servizio chiamato con'), end=" ")
            TAc.print('sorting_criterion=', "red", end="")
            TAc.print(ENV["sorting_criterion"], "yellow", end="")
            print(").")
        if ENV["feedback"] == "tell_first_minimal_missing_prefix":
            min_len1 = 0
            if pos > 0:
                while missing[min_len1] == input_solution_list[pos-1][min_len1]:
                    min_len1 += 1

            min_len2 = 0
            if pos < len(input_solution_list):
                while missing[min_len2] == input_solution_list[pos][min_len2]:
                    min_len2 += 1
            minimal_missing_prefix = missing[0:1+max(min_len1,min_len2)]
            TAc.print(LANG.render_feedback("first-missing-prefix", f'As a strong hint, here is the prefix of a feasible treatment and no treatment in your list has this prefix:'), "red", ["bold"])
            TAc.print(minimal_missing_prefix, "yellow", ["bold"])
        exit(0)
