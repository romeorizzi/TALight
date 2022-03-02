#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

from math_modeling import ModellingProblemHelper

import model_lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_id',int),
    ('instance_format',str),
    ('sol_format',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

def check_failed(log_file_tag):
    TAc.print(LANG.render_feedback("try-again", 'Correct your solution and try again.'), "yellow", ["bold"])
    if ENV.LOG_FILES != None:
        TALf.str2log_file(content='No. Bad solution for Instance {ENV["instance_id"]}.', filename=f'No_{ENV["instance_id"]}_{log_file_tag}', timestamped = False)
        TALf.str2log_file(content=sourcecode_as_string, filename=f"source_code.{TALf.lang_extension(TALf.input_filename('sourcecode'))}", timestamped = False)
    exit(0)

def check_passed(log_file_tag):
    TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done! You have found the Longest Common Subsequence.'), "green", ["bold"])
    if ENV.LOG_FILES != None:
        TALf.str2log_file(content='OK. Instance {ENV["instance_id"]}. Service check_sol. Problem lcs. The submitted solution is feasible and optimum.', filename=f'OK_{ENV["instance_id"]}_{log_file_tag}', timestamped = False)
        TALf.str2log_file(content=sourcecode_as_string, filename=f"source_code.{TALf.lang_extension(TALf.input_filename('sourcecode'))}", timestamped = False)
        TALf.str2output_file(content='OK. Instance {ENV["instance_id"]}. Service check_sol. Problem lcs. The submitted solution is feasible and optimum.\n\n   In the future we might consider to RSA-sign this message (the codebase is ready for this, but the general setup of the server will have to be done on the server, nor we have the infrastructure for the managing clear in mind). Moreover, as for now we do not need to give value to these certificates.', filename=f'OK_{ENV["instance_id"]}', timestamped = False)
        TAc.print(LANG.render_feedback('positive-submission-recorded', "The positive result of your submission has been successfully recorded."), "green", ["bold"])
    exit(0)

        
if ENV.LOG_FILES != None:
    if ENV["instance_id"] == 0:
        TAc.print(LANG.render_feedback("missing-instance_id", f'When this service is used to act a submission (i.e., when you provide a valid token) then it is required that you set a non-zero `instance_id` argument in order to specify an instance belonging to the catalogue. Call the service as follows:\n    rtal connect -x <MY_TOKEN> lcs check_sol -fsourcecode=./my_lcs_solver.py -asol_format=annotated_subseq -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
        exit(0)
    if TALf.exists_input_file('sourcecode'):
        sourcecode_as_string = TALf.input_file_as_str('sourcecode')
    else:
        TAc.print(LANG.render_feedback("missing-sourcecode", f'When this service is used to act a submission (i.e., when you provide a valid token) then it is required that at the service call you supply also the source code implementing your solving algorithm. To associate this file to the `sourcecode` filehandler call the service as follows:\n    rtal connect -x <MY_TOKEN> lcs check_sol -fsourcecode=./my_lcs_solver.py -asol_format=annotated_subseq -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
        exit(0)
if ENV["instance_id"] == 0:
    if not TALf.exists_input_file('instance'):
        TAc.print(LANG.render_feedback("missing-instance", f'This service requires that either the `instance_id` argument is different than 0 so that the intended instance can be taken from the catalogue, or that the handle to a local file containing the instance is passed through the `instance` filehandler. Two call examples:\n    1.   rtal connect lcs check_sol -asol_format=annotated_subseq -finstance=instances_catalogue/all_instances/instance_003.only_strings.txt -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt\n    2.   rtal connect lcs check_sol -asol_format=annotated_subseq -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
        exit(0)
    instance = None
else: # take instance from catalogue
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    instance_str = mph.get_file_str_from_id(ENV["instance_id"], format_name=ll.format_name_to_file_extension(ENV["instance_format"], 'instance'))
    instance = ll.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
    TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])
if TALf.exists_input_file('instance'):
    instance2 = ll.get_instance_from_txt(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
    TAc.print(LANG.render_feedback("instance-successfully-loaded", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])
    if instance2 == instance:
        TAc.print(LANG.render_feedback("same-instance", f'The instance contained in the loaded file is indeed the same as the instance from the catalogue with instance_id={ENV["instance_id"]}.'), "yellow", ["bold"])
    elif instance == None:
        instance = instance2
    else:
        TAc.print(LANG.render_feedback("different-instances", f'The instance contained in the loaded instance file differs from the one in the catalogue with instance_id={ENV["instance_id"]}.'), "red", ["bold"])
        
TAc.print(LANG.render_feedback("this-is-the-instance", "The instance is:"), "yellow", ["bold"])
TAc.print(ll.instance_to_str(instance), "white", ["bold"])
print()

if not TALf.exists_input_file('solution'):
    TAc.print(LANG.render_feedback("missing-solution", f'This service requires that the handle to a local file containing your solution is passed. Call example:\n    rtal connect lcs check_sol /asols_format=annotated_subseq -finstance=instances_catalogue/all_instances/instance_003.only_strings.txt -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
if ENV["sol_format"] == 'only_val':
    opt_val_as_str = TALf.input_file_as_str('solution').split('\n')[0].strip()
    if not opt_val_as_str.isdecimal(): 
        TAc.print(LANG.render_feedback("bad-file-opt-val", f'Your `solution` file does not contain one single decimal number (meant to be the optimal solution value).'), "red", ["bold"])
        exit(0)
    opt_val_as_int = int(opt_val_as_str)
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-opt-val", f'Your solution is:\n{opt_val_as_int}'), "yellow", ["bold"])
    opt_val, opt_sol = ll.opt_val_and_sol(s=instance[0], t=instance[1])
    if opt_val_as_int < opt_val:
        TAc.print(LANG.render_feedback("opt-val-too-small", f'You claimed that {opt_val_as_int} is the maximum length of a common subsequence. A longer subsequence however is `{opt_sol}`'), "red", ["bold"])
        check_failed('opt_val')
    if opt_val_as_int > opt_val:
        TAc.print(LANG.render_feedback("opt-val-too-big", f'The maximum length of a common subsequence is {opt_val}<{opt_val_as_int}'), "red", ["bold"])
        check_failed('opt_val')
    if opt_val_as_int == opt_val:
        TAc.print(LANG.render_feedback("opt-val-correct", f'Yes! The maximum length of a common subsequence is indeed {opt_val_as_int}'), "red", ["bold"])
        check_passed('opt_val')
if ENV["sol_format"] == 'subseq':
    solution_subseq_as_string = TALf.input_file_as_str('solution')[:-1]
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-subseq-as-string", f'Your solution is:\n{solution_subseq_as_string}'), "yellow", ["bold"])
if ENV["sol_format"] == 'annotated_subseq':
    solution_annotated_subseq = ll.read_annotated_subseq(TALf.input_file_as_str('solution'))
    solution_annotated_subseq_as_string = ll.render_annotated_subseq_as_str(solution_annotated_subseq)
    solution_subseq_as_string = ll.sequence_to_str(ll.annotated_subseq_to_sequence(solution_annotated_subseq))
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-in-file", f'Your solution, as we have read it, is:'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("legend-annotated_subseq", f"(LCS Character - First string index - Second string index)"), "yellow", ["bold"])
    TAc.print(solution_annotated_subseq_as_string, "white", ["bold"])
    list_of_triples = solution_annotated_subseq_as_string.split('\n')
    for line, i in zip(list_of_triples,range(len(list_of_triples))):
        ll.check_triple(TAc, LANG, line.split(), triple_num=i, s=instance[0], t=instance[1])
        
if ll.check_sol_feas_and_opt(TAc, LANG, solution_subseq_as_string, 'subseq', instance[0], instance[1]):
    check_passed('opt_sol')
else:
    check_failed()

