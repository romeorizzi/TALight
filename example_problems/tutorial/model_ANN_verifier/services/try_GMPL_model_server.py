#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

import model_ANN_lib as annl
from math_modeling import ModellingProblemHelper, get_problem_path_from



# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('display_output',bool),
    ('display_error',bool),
    ('display_solution',bool),
    ('check_solution',bool),
    ('instance_id',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get formats
dat_style = ''  # default



# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))


# Receive files and get instance
if not ENV['check_solution']:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat)."), "yellow")
    # Receive mod file from bot
    mph.receive_mod_file()
    # Receive dat file from bot or from the archive folder
    if ENV['instance_id'] != -1: #case: use instance_id
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=(dat_style+'dat'))
    else:
        mph.receive_dat_file()
        dat_file_path = None
else:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat input=your_input_file.txt)."), "yellow")
    # Receive mod file from bot
    mph.receive_mod_file()
    # Receive dat and input files from bot or from the archive folder
    if ENV['instance_id'] != -1: #case: use instance_id
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=(dat_style+'dat'))
        input_str = mph.get_file_str_from_id(ENV['instance_id'], format=('plain.txt'))
    else:
        mph.receive_dat_file()
        dat_file_path = None
        mph.receive_input_file()
        input_str = mph.get_input_str()
    instance = annl.get_instance_from_txt(input_str, style='plain')


print(instance)
print(dat_file_path)

# Perform solution with GPLSOL and get raw solution
mph.run_GLPSOL(dat_file_path)
raw_sol = mph.get_raw_sol()


# print GPLSOL stdout
if ENV['display_output']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    gplsol_output = mph.get_out_str()
    TAc.print(LANG.render_feedback("out-title", "The GPLSOL stdout is: "), "yellow", ["BOLD"])  
    TAc.print(LANG.render_feedback("stdout", f"{gplsol_output}"), "white", ["reverse"])


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
    TAc.print(LANG.render_feedback("instance-title", f"The ANN instance is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{annl.instance_to_str(instance)}"), "white", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Parse the raw solution
    gplsol_sol = process_user_sol(ENV, TAc, LANG, raw_sol)

    # Print processed GPLSOL solution
    TAc.print(LANG.render_feedback("sol-title", "The processed GPLSOL solution is:"), "yellow", ["BOLD"])
    
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Perform optimal solution
    opt_sol_subset = annl.get_opt_sol(instance)

    # Print optimal solution
    TAc.print(LANG.render_feedback("in-title", "The optimal solution is:"), "yellow", ["reverse"])

    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Check the correctness of the user solution
    check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, gplsol_sol, m=m, n=n)

exit(0)
