#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from get_lines import get_lines_from_stream

from recognize import recognize

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

# def check_entry_integer(row_index_name,col_index_name,entry_val):
#    if type(entry_val) != int:
#        print(f"# Error (in the table format): the entry ({row_index_name},{col_index_name}) in your table represents the floor from which to throw the first of {row_index_name} eggs when the floors are {col_index_name} (numbered from 1 to {col_index_name}). As such entry ({row_index_name},{col_index_name}) should be a natural number. However, the value {entry_val} is a non integer float with decimal part.")
#        exit(1)        

input_solution_list = [list(TALinput([str], ignore_lines_starting_with='#', regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters."))[0]]
input_solution_set = {input_solution_list[-1]}
if not recognize(input_solution_list[-1], TAc, LANG):
    exit(0)
while True:
    line = list(TALinput([str], ignore_lines_starting_with='#', regex="^(\(|\))+$", regex_explained="any string of '(' and ')' characters."))[0]
    if line == 'end':
        break
    if not len(line) == len(input_solution_list[-1]):
        TAc.print(LANG.render_feedback("different_lengths", "No. La formula di parentesi che hai appena introdotto è di lunghezza diversa dalla precedenti."), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if line in input_solution_set:
        TAc.print(LANG.render_feedback("repeated", f"No. La formula di parentesi ben formata che hai appena introdotto è la stessa dell'inserimento numero {input_solution_set.index(line)+1}."), "red", ["bold"])
    input_solution_set.add(line)
    input_solution_list.append(line)

TAc.print(LANG.render_feedback("your-formulas-all-ok", f"Le formule che hai introdotto sono tutte ben fermate."), "green")

input_solution_list.sort()
print(input_solution_list)
   
# regex: ^(yes_no|tell_a_minimal_missing_prefix|give_one_missing)$
   
       
exit(0)
