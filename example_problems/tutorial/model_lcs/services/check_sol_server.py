#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import model_lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_format',str),
    ('sol_format',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

if not TALf.exists_input_file('instance'):
    TAc.print(LANG.render_feedback("missing-instance", f'This service requires that the handle to a local file containing the instance is passed. Call example:\n    rtal connect lcs check_sol -asol_format=annotated_subseq -finstance=instances_catalogue/all_instances/instance_003.only_strings.txt -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
instance = ll.get_instance_from_txt(TALf.input_file_as_str('instance'), instance_format_name=ENV['instance_format'])
print(instance)
TAc.print(LANG.render_feedback("instance-successfully-loaded", f'Your `instance` file has been successfully loaded.'), "white", ["bold"])
TAc.print(LANG.render_feedback("this-is-the-instance", "The instance is:"), "white", ["bold"])
TAc.print(ll.instance_to_str(instance), "yellow", ["bold"])
m=len(instance[0])
n=len(instance[1])
print()

if not TALf.exists_input_file('solution'):
    TAc.print(LANG.render_feedback("missing-solution", f'This service requires that the handle to a local file containing your solution is passed. Call example:\n    rtal connect lcs check_sol /asols_format=annotated_subseq -finstance=instances_catalogue/all_instances/instance_003.only_strings.txt -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
if ENV['sol_format'] == 'subseq':
    solution_subseq_as_string = TALf.input_file_as_str('solution')[:-1]
    solution_as_subseq = ll.str_to_sequence(solution_subseq_as_string)
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-subseq", f'Your solution is:\n{solution_subseq_as_string}'), "yellow", ["bold"])
if ENV['sol_format'] == 'annotated_subseq':
    solution_annotated_subseq = ll.read_annotated_subseq(TALf.input_file_as_str('solution'))
    solution_annotated_subseq_as_string = ll.render_annotated_subseq_as_str(solution_annotated_subseq)
    solution_as_subseq = ll.annotated_subseq_to_sequence(solution_annotated_subseq)
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-in-file", f'Your solution, as we have read it, is:'), "white", ["bold"])
    TAc.print(LANG.render_feedback("legend-annotated_subseq", f"(LCS Character - First string index - Second string index)"), "yellow", ["bold"])
    TAc.print(solution_annotated_subseq_as_string, "yellow", ["bold"])
    for line in solution_annotated_subseq_as_string.split('\n'):
        ll.check_input(TAc, LANG, line.split(), m, n)
        
if ll.check_sol_feas_and_opt(TAc, LANG, solution_as_subseq, 'subseq', instance[0], instance[1]):
    TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done! You have found the Longest Common Subsequence.'), "green", ["bold"]) 
exit(0)

