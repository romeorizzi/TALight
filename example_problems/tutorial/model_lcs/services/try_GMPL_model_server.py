#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

import model_lcs_lib as ll
from math_modeling import ModellingProblemHelper, get_problem_path_from


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('display_output',bool),
    ('display_error',bool),
    ('display_solution',bool),
    ('check_solution',bool),
    ('txt_style',str),
    ('sol_style',str),
    ('instance_id',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:

# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))


# Receive files and get instance
if not ENV['check_solution']:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat)."), "yellow")
    # Receive mod file from bot
    mph.receive_mod_file()
    # Receive dat file from bot or from the archive folder
    if ENV['instance_id'] != -1: #case: use instance_id
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=('dat'))
    else:
        mph.receive_dat_file()
        dat_file_path = None
else:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat input=your_input_file.txt)."), "yellow")
    # Receive mod file from bot
    mph.receive_mod_file()
    # Receive dat and input files from bot or from the archive folder
    if ENV['instance_id'] != -1: #case: use instance_id
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=('dat'))
        input_str = mph.get_file_str_from_id(ENV['instance_id'], format=(ENV['txt_style'] + '.txt'))
    else:
        mph.receive_dat_file()
        dat_file_path = None
        mph.receive_input_file()
        input_str = mph.get_input_str()
    instance = ll.get_instance_from_txt(input_str, style=ENV['txt_style'])    
    print(instance)
    
    # numero righe e colonne pirellone
    m = len(instance[0])
    n = len(instance[1])

mph.run_GLPSOL(dat_file_path)

# print GPLSOL stdout
gplsol_output = mph.get_out_str()
if ENV['display_output']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("out-title", "The GPLSOL stdout is: "), "yellow", ["BOLD"])  
    TAc.print(LANG.render_feedback("stdout", f"{gplsol_output}"), "white", ["reverse"])

if gplsol_output.find("NO PRIMAL") != -1:
    TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
    exit(0)

raw_sol = mph.get_raw_sol()

# print GPLSOL stderr
if ENV['display_error']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    gplsol_error = mph.get_err_str()
    TAc.print(LANG.render_feedback("err-title", "The GPLSOL stderr is: "), "yellow", ["BOLD"])  
    TAc.print(LANG.render_feedback("stderr", f"{gplsol_error}"), "white", ["reverse"])


# print GPLSOL solution.txt
if ENV['display_solution']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("sol-title", "The raw GPLSOL solution is: "), "yellow", ["BOLD"])  
    for line in raw_sol:
        print(line)


# check GPLSOL solution
if ENV['check_solution']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("start-check", f"Now start the check of the GPLSOL solution..."), "yellow", ["bold"])

    # Print instance
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {m} character and the second string of {n} character are:'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{ll.instance_to_str(instance)}"), "white", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Parse the raw solution
    gplsol_sol = ll.process_user_sol(TAc, LANG, raw_sol, instance)

    # Print processed GPLSOL solution
    TAc.print(LANG.render_feedback("sol-title", "The GPLSOL solution is:"), "yellow", ["BOLD"])    
    if ENV['sol_style'] == 'subsequence':
        TAc.print(LANG.render_feedback("out_sol", f"{ll.sequence_to_str(ll.annotated_subseq_to_sequence(gplsol_sol))}"), "white", ["reverse"])
    elif ENV['sol_style'] == 'annotated_subseq':
        TAc.print(LANG.render_feedback("out_sol", f"{ll.annotated_subseq_to_str(gplsol_sol)}"), "white", ["reverse"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    
    annotated_subseq_sol = ll.get_sol(instance[0], instance[1], m, n)
    subsequence_sol = ll.annotated_subseq_to_sequence(annotated_subseq_sol)
    print(f"The annotated solution = {annotated_subseq_sol}, the subsequence solution = {subsequence_sol}")

    user_sol_subsequence = ll.annotated_subseq_to_sequence(gplsol_sol)
    user_sol_annotated_subseq = gplsol_sol

    # check feasibility of the user solution
    print(f"Your annotated solution = {user_sol_annotated_subseq}, you subsequence solution = {user_sol_subsequence}")

    if ENV['sol_style'] == 'subsequence':
        if ll.check_sol(TAc, LANG, ENV, user_sol_subsequence, instance[0], instance[1]):
            TAc.OK()
            TAc.print(LANG.render_feedback('correct', "Therefore, the solution to your instance produced by your model is correct."), "green", ["bold"])
    elif ENV['sol_style'] == 'annotated_subseq':
        if ll.check_sol(TAc, LANG, ENV, user_sol_annotated_subseq, instance[0], instance[1]):
            TAc.OK()
            TAc.print(LANG.render_feedback('correct', "Therefore, the solution to your instance produced by your model is correct."), "green", ["bold"])

exit(0)
