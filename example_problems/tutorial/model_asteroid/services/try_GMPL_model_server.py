#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors

import model_asteroid_lib as al
from math_modeling import ModellingProblemHelper


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
mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES)

if ENV['check_solution']:
    input_str = mph.get_input_str()
    instance = al.get_instance_from_txt(input_str, style=ENV['txt_style'])
    print(instance)
    m = len(instance)
    n = len(instance[0])


# Perform solution with GPLSOL and get raw solution
mph.run_GLPSOL()
glpsol_output = mph.get_out_str()

# print GPLSOL stdout
if ENV['display_output']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("out-title", "The GPLSOL stdout is: "), "yellow", ["bold"])  
    TAc.print(LANG.render_feedback("stdout", f"{glpsol_output}"), "white", ["reverse"])

if glpsol_output.find("NO PRIMAL") != -1:
    TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
    exit(0)

# print GPLSOL stderr
if ENV['display_error']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    gplsol_error = mph.get_err_str()
    TAc.print(LANG.render_feedback("err-title", "The GPLSOL stderr is: "), "yellow", ["bold"])  
    TAc.print(LANG.render_feedback("stderr", f"{gplsol_error}"), "white", ["reverse"])

raw_sol = mph.get_raw_sol()
# print GPLSOL solution.txt
if ENV['display_solution']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("sol-title", "The raw GPLSOL solution is: "), "yellow", ["bold"])  
    for line in raw_sol:
        print(line)


# check GPLSOL solution
if ENV['check_solution']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("start-check", f"Now start the check of the GPLSOL solution..."), "yellow", ["bold"])

    # Print instance
    TAc.print(LANG.render_feedback("instance-title", f"The matrix {m}x{n} is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{al.instance_to_str(instance)}"), "white", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Parse the raw solution
    gplsol_sol = al.process_user_sol(ENV, TAc, LANG, raw_sol, m=m, n=n)

    # Print processed GPLSOL solution
    TAc.print(LANG.render_feedback("sol-title", "The GPLSOL solution is:"), "yellow", ["bold"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("out_sol", f"{al.seq_to_str(gplsol_sol)}"), "white", ["reverse"])
        gplsol_sol = al.seq_to_subset(gplsol_sol, m, n)
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("out_sol", f"{al.subset_to_str(gplsol_sol)}"), "white", ["reverse"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    
    # Get an optimal solution
    opt_sol_subset = al.min_cover(m,n,instance)
    opt_val = len(opt_sol_subset)
    print(f"opt_sol_subset={opt_sol_subset}, opt_val={opt_val}")

    # Check the correctness of the user solution
    if ENV['sol_style'] == 'seq':
        user_sol_subset = al.seq_to_subset(gplsol_sol, ENV['m'], ENV['n'])
        user_sol_seq = gplsol_sol
    else:
        user_sol_seq = al.subset_to_seq(gplsol_sol)
        user_sol_subset = gplsol_sol
    # check feasibility of the user solution
    print(f"user_sol_seq={user_sol_seq}, user_sol_subset={user_sol_subset}")
    if al.is_feasible_shooting(m,n,instance,beams=user_sol_seq,silent=False,TAc=TAc,LANG=LANG):
        TAc.OK()
        TAc.print(LANG.render_feedback('feasible', "Therefore, the solution to your instance produced by your modelel is correct."), "green", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback('error', f"The solution is not correct. The pirellone cell in row={certificate_of_no[0]} and col={certificate_of_no[1]} stays on."), "red", ["bold"])
        exit(0)
    # check optimlity of the user solution
    if ENV['sol_style'] == 'seq':
        if len(opt_sol_seq) != len(user_sol_seq):
            TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
            exit(0)
    elif ENV['sol_style'] == 'subset':
        if not al.is_optimal(user_sol_subset):
            TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
            exit(0)
    TAc.print(LANG.render_feedback('minimal', "The solution is minimal!"), "green", ["bold"])


exit(0)
