#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import pirellone_lib as pl
from math_modeling import ModellingProblemHelper

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_format',str),
    ('instance_id', int),
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
        TALf.str2log_file(content=f'No. Bad solution for Instance {ENV["instance_id"]}.', filename=f'No_{ENV["instance_id"]}_{log_file_tag}', timestamped = False)
        TALf.str2log_file(content=sourcecode_as_string, filename=f"source_code.{TALf.lang_extension(TALf.input_filename('sourcecode'))}", timestamped = False)
    exit(0)

def check_passed(log_file_tag):
    TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done!'), "green", ["bold"])
    if ENV.LOG_FILES != None:
        TALf.str2log_file(content=f'OK. Instance {ENV["instance_id"]}. Service check_sol. Problem pirellone. The submitted solution is feasible and optimum.', filename=f'OK_{ENV["instance_id"]}_{log_file_tag}', timestamped = False)
        TALf.str2log_file(content=sourcecode_as_string, filename=f"source_code.{TALf.lang_extension(TALf.input_filename('sourcecode'))}", timestamped = False)
        TALf.str2output_file(content=f'OK. Instance {ENV["instance_id"]}. Service check_sol. Problem pirellone. The submitted solution is feasible and optimum.\n\n   In the future we might consider to RSA-sign this message (the codebase is ready for this, but the general setup of the server will have to be done on the server, nor we have the infrastructure for the managing clear in mind). Moreover, as for now we do not need to give value to these certificates.', filename=f'OK_{ENV["instance_id"]}', timestamped = False)
        TAc.print(LANG.render_feedback('positive-submission-recorded', "The positive result of your submission has been successfully recorded."), "green", ["bold"])
    exit(0)

        
if ENV.LOG_FILES != None:
    if ENV["instance_id"] == 0:
        TAc.print(LANG.render_feedback("missing-instance_id", f'When this service is used to act a submission (i.e., when you provide a valid token) then it is required that you set a non-zero `instance_id` argument in order to specify an instance belonging to the catalogue. Call the service as follows:\n    rtal connect -x <MY_TOKEN> model_pirellone check_sol -fsourcecode=./my_pirellone_solver.py -asol_format=subset -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.subset.txt'), "red", ["bold"])
        exit(0)
    if TALf.exists_input_file('sourcecode'):
        sourcecode_as_string = TALf.input_file_as_str('sourcecode')
    else:
        TAc.print(LANG.render_feedback("missing-sourcecode", f'When this service is used to act a submission (i.e., when you provide a valid token) then it is required that at the service call you supply also the source code implementing your solving algorithm. To associate this file to the `sourcecode` filehandler call the service as follows:\n    rtal connect -x <MY_TOKEN> model_pirellone check_sol -fsourcecode=./my_pirellone_solver.py -asol_format=subset -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.subset.txt'), "red", ["bold"])
        exit(0)
if ENV["instance_id"] == 0:
    if not TALf.exists_input_file('instance'):
        TAc.print(LANG.render_feedback("missing-instance", f'This service requires that either the `instance_id` argument is different than 0 so that the intended instance can be taken from the catalogue, or that the handle to a local file containing the instance is passed through the `instance` filehandler. Two call examples:\n    1.   rtal connect model_pirellone check_sol -asol_format=subset -finstance=instances_catalogue/all_instances/instance_003.only_matrix.txt -fsolution=my_sols/all_instances/solution_003.subset.txt\n    2.   rtal connect model_pirellone check_sol -asol_format=subset -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.subset.txt'), "red", ["bold"])
        exit(0)
    instance = None
else: # take instance from catalogue
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    instance_str = mph.get_file_str_from_id(ENV["instance_id"], format_name=pl.format_name_to_file_extension(ENV["instance_format"], 'instance'))
    instance = pl.get_instance_from_str(instance_str, instance_format=ENV["instance_format"])
    TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])
if TALf.exists_input_file('instance'):
    instance2 = pl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format=ENV["instance_format"])
    TAc.print(LANG.render_feedback("instance-successfully-loaded", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])
    if instance2 == instance:
        TAc.print(LANG.render_feedback("same-instance", f'The instance contained in the loaded file is indeed the same as the instance from the catalogue with instance_id={ENV["instance_id"]}.'), "yellow", ["bold"])
    elif instance == None:
        instance = instance2
    else:
        TAc.print(LANG.render_feedback("different-instances", f'The instance contained in the loaded instance file differs from the one in the catalogue with instance_id={ENV["instance_id"]}.'), "red", ["bold"])
        
TAc.print(LANG.render_feedback("this-is-the-instance", "The instance is:"), "yellow", ["bold"])
TAc.print(pl.instance_to_str(instance), "white", ["bold"])
print()

m=len(instance)
n=len(instance[0])
# print('m:',m,' - n:',n)

if not TALf.exists_input_file('solution'):
    TAc.print(LANG.render_feedback("missing-solution", f'This service requires that the handle to a local file containing your solution is passed. Call example:\n    rtal connect model_pirellone check_sol /asol_format=subset -finstance=instances_catalogue/all_instances/instance_003.only_matrix.txt -fsolution=my_sols/all_instances/solution_003.subset.txt'), "red", ["bold"])
if ENV["sol_format"] == 'only_val':
    opt_val_as_str = TALf.input_file_as_str('solution').split('\n')[0].strip()
    opt_val_as_int = int(opt_val_as_str)
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-opt-val", f'Your solution is:\n{opt_val_as_str}'), "yellow", ["bold"])
    opt_val=pl.opt_val(instance)
    if opt_val_as_int < opt_val:
        TAc.print(LANG.render_feedback("opt-val-too-small", f'No, the number of switches you need to push is more than {opt_val_as_int}.'), "red", ["bold"])
        check_failed('opt_val')
    if opt_val_as_int > opt_val:
        TAc.print(LANG.render_feedback("opt-val-too-big", f'No, the number of switches you need to push is less than {opt_val_as_int}.'), "red", ["bold"])
        check_failed('opt_val')
    if opt_val_as_int == opt_val:
        TAc.print(LANG.render_feedback("opt-val-correct", f'Yes! The number of switches you need to push is {opt_val_as_int}.'), "green", ["bold"])
        check_passed('opt_val')
elif ENV["sol_format"] == 'seq':
    solution_seq_as_string = TALf.input_file_as_str('solution').strip('\n').split(' ')
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-subseq-as-string", f'Your solution is:\n{pl.seq_to_str(solution_seq_as_string)}'), "yellow", ["bold"])
    lunghezza=len(solution_seq_as_string)
    solution=pl.seq_to_subset(solution_seq_as_string, m, n)
elif ENV["sol_format"] == 'subset':
    solution_subset_as_string=TALf.input_file_as_str('solution')
    lunghezza=solution_subset_as_string.count('1')
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "yellow", ["bold"])
    solution=[]
    m=len(instance)
    solution.append(list(map(int,solution_subset_as_string[0:(m*2-1)].split())))
    solution.append(list(map(int,solution_subset_as_string[m*2:].split())))
    TAc.print(LANG.render_feedback("user-sol-subset-as-string", f'Your solution is:\n{solution_subset_as_string}'), "yellow", ["bold"])

is_solvable=pl.is_solvable(instance)
opt_val=pl.opt_val(instance)
if solution=='NO SOLUTION':
    if not is_solvable:
        TAc.print(LANG.render_feedback("no_sol-correct", f'Yes! This instance is not solvable.'), "green", ["bold"])
        check_passed('opt_sol')
    else:
        TAc.print(LANG.render_feedback("no_sol-wrong", f'No, this instance is solvable.'), "red", ["bold"])
        check_failed('sol')
elif pl.check_sol(instance,solution)[0]:
    if lunghezza==opt_val:
        TAc.print(LANG.render_feedback("opt-sol-correct", f'Yes! You have found which rows/columns switches you have to push.'), "green", ["bold"])
        check_passed('opt_sol')
    else:
        TAc.print(LANG.render_feedback("sol-correct-but-not-optimal", f'No, you turn off all the lights but you solution is not optimal.'), "red", ["bold"])
        check_failed('opt_val')
elif lunghezza==opt_val and is_solvable:
    TAc.print(LANG.render_feedback("wrong-sol", f'No, you do not turn off all the lights.'), "red", ["bold"])
else:
    TAc.print(LANG.render_feedback("wrong-sol", f'No, you solution is wrong.'), "red", ["bold"])
check_failed('opt_val')
