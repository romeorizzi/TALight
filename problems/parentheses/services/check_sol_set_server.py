#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from get_lines import get_lines_from_stream

from parentheses_lib import recognize, num_sol, unrank

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="check_solutions_set"
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

print("# waiting for your set of well-formed formulas of parentheses. Please, each one of them should go on a different line. All these lines should have the same lenght. Insert a closing line '# END' after the last row of the table. Any other line beggining with the '#' character is ignored. If you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file.")
input_solution_list = [list(TALinput([str], ignore_lines_starting_with='#', regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters."))[0]]
input_solution_set = {input_solution_list[-1]}
if not recognize(input_solution_list[-1], TAc, LANG):
    exit(0)
len_lines = len(input_solution_list[0])
while True:
    line = list(TALinput([str], ignore_lines_starting_with='#', regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters."))[0]
    if line == 'end':
        break
    if not len(line) == len_lines:
        TAc.print(LANG.render_feedback("different_lengths", "No. La formula di parentesi che hai appena introdotto è di lunghezza diversa dalle precedenti."), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if line in input_solution_set:
        TAc.print(LANG.render_feedback("repeated", f"No. La formula di parentesi ben formata che hai appena introdotto è la stessa dell'inserimento numero {input_solution_set.index(line)+1}."), "red", ["bold"])
    input_solution_set.add(line)
    input_solution_list.append(line)

TAc.print(LANG.render_feedback("your-formulas-all-ok", f"All the formulas you have introduced are ok (well formed)."), "green")

input_solution_list.sort()
#print(input_solution_list)

n_pairs = len_lines//2

if len(input_solution_list) < num_sol(n_pairs) and ENV['feedback'] == "yes_no":
    TAc.print(LANG.render_feedback("one-formula-is-missing-no-feedback", f"No. Your set is missing at least one well-formed formula."), "red", ["bold"])
    exit(0)


for pos in range(num_sol(n_pairs)):
    #print(f"pos={pos}, input_solution_list[pos]={input_solution_list[pos]}, unrank(n_pairs, pos)={unrank(n_pairs, pos)}")
    if input_solution_list[pos] != unrank(n_pairs, pos):
        missing = unrank(n_pairs, pos)
        #print(f"missing={missing}")
        if ENV['feedback'] == "give_one_missing":
            TAc.print(LANG.render_feedback("one-formula-is-missing-no-feedback", f"No. Your set is missing at least one well-formed formula.\nConsider for example:"), "red", ["bold"])
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
            TAc.print(LANG.render_feedback("one-missing-minimal-prefix", f"No. Your set is missing at least one well-formed formula.\nHere is the prefix of a well-formed formula and no formula in your set has this prefix:"), "red", ["bold"])
            TAc.print(minimal_missing_prefix, "yellow", ["bold"])
        exit(0)

exit(0)
