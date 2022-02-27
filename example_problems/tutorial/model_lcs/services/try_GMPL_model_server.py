#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper

import model_lcs_lib as ll


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('display_output',bool),
    ('display_error',bool),
    ('display_raw_solution',bool),
    ('display_explicit_formulation',bool),
    ('explicit_formulation_format',str),
    ('check_solution',bool),
    ('instance_format',str),
    ('sol_format',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR )

if ENV['display_explicit_formulation']:
    mph.run_GLPSOL_with_ef(ENV['explicit_formulation_format'])

    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    glpsol_ef = mph.get_ef_str()
    TAc.print(LANG.render_feedback("formulation-title", "The explicit formulation is: "), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("formulation", f"{glpsol_ef}"), "white", ["reverse"])
else:
    mph.run_GLPSOL()

glpsol_output = mph.get_out_str()

if ENV['display_output']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("out-title", "The GLPSOL stdout is: "), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("stdout", f"{glpsol_output}"), "white", ["reverse"])

if glpsol_output.find("NO PRIMAL") != -1:
    TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
    exit(0)

if ENV['display_error']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    glpsol_error = mph.get_err_str()
    TAc.print(LANG.render_feedback("err-title", "The GLPSOL stderr is: "), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("stderr", f"{glpsol_error}"), "white", ["reverse"])

raw_sol = mph.get_raw_sol()

if ENV['display_raw_solution']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("sol-title", "The raw GLPSOL solution is: "), "yellow", ["bold"])
    for line in raw_sol:
        print(line)
        

if ENV['check_solution'] or ENV.LOG_FILES != None:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("start-check", f"Now start the check of the GLPSOL solution..."), "yellow", ["bold"])
    input_str = mph.get_input_str()
    instance = ll.get_instance_from_txt(input_str, instance_format_name=ENV['instance_format'])
    print(LANG.render_feedback("instance-title", f'The first string (of length {len(instance[0])}) and the second string (of length {len(instance[1])}) comprising the instance are:'))
    TAc.print(ll.instance_to_str(instance), "white", ["bold"])
    max_val, an_opt_sol_annotated_subseq = ll.opt_val_and_sol(instance[0], instance[1])
    an_opt_sol_subseq = ll.annotated_subseq_to_sequence(an_opt_sol_annotated_subseq)
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("sol-title", "The solution obtained by GLPSOL on your model:"), "yellow", ["bold"])
    if ENV['sol_format'] == 'subseq':
        user_sol = raw_sol
        TAc.print(ll.sequence_to_str(user_sol), "white", ["reverse"])
        TAc.print(LANG.render_feedback("print-opt-sol-subseq", f"An optimal solution:\n   {an_opt_sol_subseq}"), "white", ["reverse"])
    if ENV['sol_format'] == 'annotated_subseq':
        user_sol = user_sol_annotated_subseq = ll.read_annotated_subseq("\n".join(raw_sol)+"\n")
        TAc.print(ll.render_annotated_subseq_as_str(user_sol_annotated_subseq), "white", ["reverse"])
        TAc.print(LANG.render_feedback("print-opt-sol-anotated-subseq", f"An optimal solution:\n   {an_opt_sol_annotated_subseq}"), "white", ["reverse"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    if ll.check_sol_feas_and_opt(TAc, LANG, user_sol, ENV['sol_format'], instance[0], instance[1]):
        TAc.OK()
        TAc.print(LANG.render_feedback('correct', "Therefore, the solution to your instance produced by your model is correct."), "green", ["bold"])

if ENV.LOG_FILES != None:
    if solution_is_correct:
        print(f"ENV.LOG_FILES={ENV.LOG_FILES}")
        log_file = open(os.path.join(ENV.LOG_FILES,'score'), 'w')
        print("certificate of positive submission", file=log_file)
        log_file.close()
        TAc.print(LANG.render_feedback('positive-submission-recorded', "The positive result of your submission has been successfully recorded."), "green", ["bold"])

exit(0)
