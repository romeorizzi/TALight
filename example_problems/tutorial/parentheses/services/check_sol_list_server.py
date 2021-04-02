#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
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
print("# waiting for your ordered list of well-formed formulas of parentheses.\nPlease, each formula should go on a different line and each line should have the same length and comprise only '(' or ')' characters.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

p = Par(20)      

line = None
while line == None:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters.", TAc=TAc)
    if line == "#end":
        TAc.print(LANG.render_feedback("at-least-one-line", f'No. You are required to enter at least one valid formula before closing.'), "yellow")
    
input_solution_list = [line]
if not recognize(input_solution_list[-1], TAc, LANG):
    TAc.print(LANG.render_feedback("first-line-not-well-formed", f'No. Your very first formula of parentheses is not well formed.'), "red", ["bold"])
    exit(0)
len_lines = len(line)
n_pairs = len_lines//2

if ENV["sorting_criterion"]=="loves_opening_par":
    first='(' * n_pairs + ')' * n_pairs
else:
    first='()' * n_pairs
if input_solution_list[-1] != first:
    TAc.print(LANG.render_feedback("wrong-first", f'No. La primissima formula di parentesi ben formata cha hai introdotto non è però la prima secondo l\'ordinamento impostato'), "red", ["bold"], end=" ")
    print(LANG.render_feedback("called-with", '(servizio chiamato con'), end=" ")
    TAc.print('sorting_criterion=', "red", end="")
    TAc.print(ENV["sorting_criterion"], "yellow", end="")
    print(').')
    exit(0)

while True:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters.", TAc=TAc)
    if line in stopping_command_set:
        break
    if not len(line) == len_lines:
        TAc.print(LANG.render_feedback("different_lengths", f'No. La formula di parentesi che hai appena introdotto (tua riga {len(input_solution_list)+1}) è di lunghezza diversa dalle precedenti.'), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if (line < input_solution_list[-1]) == (ENV["sorting_criterion"]=="loves_opening_par"):
        TAc.print(LANG.render_feedback("order-violation", f'No. La formula di parentesi ben formata che hai introdotto in posizione {len(input_solution_list)+1} non viene dopo ma prima della precedente secondo l\'ordinamento impostato'), "red", ["bold"], end=" ")
        print(LANG.render_feedback("called-with", '(servizio chiamato con'), end=" ")
        TAc.print('sorting_criterion=', "red", end="")
        TAc.print(ENV["sorting_criterion"], "yellow", end="")
        print(').')
        exit(0)
    if line == input_solution_list[-1]:
        TAc.print(LANG.render_feedback("repeated", f'No. La formula di parentesi ben formata che hai appena introdotto (tua riga {len(input_solution_list)+1}) è la stessa dell\'inserimento in riga immediatamente precedente. Nulla è perduto: questo doppio inserimento verrà ignorato. Puoi procedere.'), "red", ["bold"])
    else:
        input_solution_list.append(line)

print("# FILE GOT")
TAc.print(LANG.render_feedback("your-formulas-all-ok", f'All the formulas you have introduced are ok (well formed) and correctly ordered.'), "green")

#print(input_solution_list)

if len(input_solution_list) < p.num_sol(n_pairs) and ENV["feedback"] == "yes_no":
    TAc.print(LANG.render_feedback("one-formula-is-missing-no-feedback", f'No. Your list is missing at least one well-formed formula.'), "red", ["bold"])
    exit(0)

for pos in range(p.num_sol(n_pairs)):
    #print(f"pos={pos}, input_solution_list[pos]={input_solution_list[pos]}, p.unrank(n_pairs, pos)={p.unrank(n_pairs, pos)}")
    if input_solution_list[pos] != p.unrank(n_pairs, pos):
        missing = p.unrank(n_pairs, pos)
        #print(f"missing={missing}")
        if ENV["feedback"] == "give_first_missing":
            TAc.print(LANG.render_feedback("give-missing-formula", f'No. Your list is missing at least one well-formed formula.\nConsider for example:'), "red", ["bold"])
            TAc.print(missing, "yellow", ["bold"])
        if ENV["feedback"] == "spot_first_wrong_consec":
            assert pos > 0
            TAc.print(LANG.render_feedback("not-consecutive", f'No. The two well-formed formulas:\n {input_solution_list[pos-1]}\n {input_solution_list[pos]}\nthat appear consecutive in your list are NOT consecutive in the intended order'), "red", ["bold"], end=" ")
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
            TAc.print(LANG.render_feedback("first-missing-prefix", f'No. Your list is missing at least one well-formed formula.\nHere is the prefix of a well-formed formula and no formula in your list has this prefix:'), "red", ["bold"])
            TAc.print(minimal_missing_prefix, "yellow", ["bold"])
        exit(0)
TAc.OK()
TAc.print(LANG.render_feedback("list-ok", f'Ok! You have listed all well-formed formulas with {n_pairs} pairs of parentheses. Also their order is the intended one.'), "green")
exit(0)
