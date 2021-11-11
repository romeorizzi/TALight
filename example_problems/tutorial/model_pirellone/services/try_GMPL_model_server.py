#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

import model_pirellone_lib as pl
from math_modeling import ModellingProblemHelper, get_problem_path_from
from services_utils import process_user_sol, print_separator, check_sol_with_feedback


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
# Get formats
dat_style = ''  # default
txt_style = ENV['txt_style']


# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))


# Receive files and get instance
if not ENV['check_solution']:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat)."), "yellow")
    # Receive mod file from bot
    mph.receive_mod_file()
    # Receive dat file from bot or from the archive folder
    if ENV['instance_id'] == -1: #case: use instance_id
        mph.receive_dat_file()
        dat_file_path = None
    else:
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=(dat_style+'dat'))
else:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat input=your_input_file.txt)."), "yellow")
    # Receive mod file from bot
    mph.receive_mod_file()
    # Receive dat and input files from bot or from the archive folder
    if ENV['instance_id'] == -1: #case: use instance_id
        mph.receive_dat_file()
        dat_file_path = None
        mph.receive_input_file()
        input_str = mph.get_input_str()
    else:
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=(dat_style+'dat'))
        input_str = mph.get_file_str_from_id(ENV['instance_id'], format=(txt_style+'.txt'))
    instance = pl.get_instance_from_txt(input_str, style=txt_style)
    m = len(instance)
    n = len(instance[0])


# Perform solution with GPLSOL and get raw solution
mph.run_GLPSOL(dat_file_path)
raw_sol = mph.get_raw_sol()


# print GPLSOL stdout
if ENV['display_output']:
    print_separator(TAc, LANG)
    gplsol_output = mph.get_out_str()
    TAc.print(LANG.render_feedback("out-title", "The GPLSOL stdout is: "), "yellow", ["BOLD"])  
    TAc.print(LANG.render_feedback("stdout", f"{gplsol_output}"), "white", ["reverse"])


# print GPLSOL stderr
if ENV['display_error']:
    print_separator(TAc, LANG)
    gplsol_error = mph.get_err_str()
    TAc.print(LANG.render_feedback("err-title", "The GPLSOL stderr is: "), "yellow", ["BOLD"])  
    TAc.print(LANG.render_feedback("stderr", f"{gplsol_error}"), "white", ["reverse"])


# print GPLSOL solution.txt
if ENV['display_solution']:
    print_separator(TAc, LANG)
    TAc.print(LANG.render_feedback("sol-title", "The raw GPLSOL solution is: "), "yellow", ["BOLD"])  
    for line in raw_sol:
        print(line)


# check GPLSOL solution
if ENV['check_solution']:
    print_separator(TAc, LANG)
    TAc.print(LANG.render_feedback("start-check", f"Now start the check of the GPLSOL solution..."), "yellow", ["bold"])

    # Print instance
    TAc.print(LANG.render_feedback("instance-title", f"The matrix {m}x{n} is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{pl.instance_to_str(instance)}"), "white", ["bold"])
    print_separator(TAc, LANG)

    # Parse the raw solution
    gplsol_sol = process_user_sol(ENV, TAc, LANG, raw_sol, m=m, n=n)

    # Print processed GPLSOL solution
    TAc.print(LANG.render_feedback("sol-title", "The processed GPLSOL solution is:"), "yellow", ["BOLD"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("out_sol", f"{pl.seq_to_str(gplsol_sol)}"), "white", ["reverse"])
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("out_sol", f"{pl.subset_to_str(gplsol_sol)}"), "white", ["reverse"])
    print_separator(TAc, LANG)

    # Perform optimal solution
    opt_sol_subset = pl.get_opt_sol(instance)

    # Print optimal solution
    TAc.print(LANG.render_feedback("in-title", "The optimal solution is:"), "yellow", ["reverse"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("in-sol", f"{pl.seq_to_str(pl.subset_to_seq(opt_sol_subset))}"), "green", ["bold"])
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("in-sol", f"{pl.subset_to_str(opt_sol_subset)}"), "green", ["bold"])
    print_separator(TAc, LANG)

    # Check the correctness of the user solution
    check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, gplsol_sol, m=m, n=n)

exit(0)
