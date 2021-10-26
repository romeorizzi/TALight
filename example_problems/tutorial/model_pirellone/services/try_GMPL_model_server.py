#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

import model_pirellone_lib as pl
from math_modeling import ModellingProblemHelper, get_problem_path_from
from services_utils import process_user_sol, print_separator, check_sol_with_feedback


# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="try_GMPL_model"
args_list = [
    ('display_output',bool),
    ('display_error',bool),
    ('check_solution',bool),
    ('txt_style',str),
    ('sol_style',str),
    ('instance_id',int),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get formats
dat_style = ''  # default
txt_style = ENV['txt_style']


# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(get_problem_path_from(__file__))

# Get files
try:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod dat=your_dat_file.dat input=your_input_file.txt)."), "yellow")
    # Get mod
    mph.receive_mod_file()
    # Get dat and input
    if ENV['instance_id'] == -1:
        # Get dat file
        mph.receive_dat_file()
        dat_file_path = None
        # Get input file
        if ENV['check_solution']:
            input_str = mph.receive_input_file()
    else:
        # Get dat file
        dat_file_path = mph.get_path_from_id(ENV['instance_id'], format=(dat_style+'dat'))
        # Get input file
        if ENV['check_solution']:
            input_str = mph.get_file_str_from_id(ENV['instance_id'], format=(txt_style+'.txt'))
    instance = pl.get_instance_from_txt(input_str, style=txt_style)
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'write-error':
        TAc.print(LANG.render_feedback('write-error', f"Fail to create {err.args[1]} file"), "red", ["bold"])
    elif err_name == 'invalid-id':
        TAc.print(LANG.render_feedback('invalid-id', f"id={err.args[1]} is invalid."), "red", ["bold"])
    else:
         TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
    exit(1)

# Perform solution with GPLSOL
try:
    mph.run_GLPSOL(dat_file_path)
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'process-timeout':
        TAc.print(LANG.render_feedback('process-timeout', "Too much computing time! Deadline exceeded."), "red", ["bold"])
    elif err_name == 'process-call':
        TAc.print(LANG.render_feedback('process-call', "The call to glpsol on your .dat file returned error."), "red", ["bold"])
    elif err_name == 'process-exception':
        TAc.print(LANG.render_feedback('process-exception', f"Processing returned with error:\n{err.args[1]}"), "red", ["bold"])
    else:
         TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
    exit(1)

# print GPLSOL stdout
if ENV['display_output']:
    print_separator(TAc, LANG)
    try:
        gplsol_output = mph.get_out_str()
        TAc.print(LANG.render_feedback("out-title", "The GPLSOL stdout is: "), "yellow", ["BOLD"])  
        TAc.print(LANG.render_feedback("stdout", f"{gplsol_output}"), "white", ["reverse"])
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'read-error':
            TAc.print(LANG.render_feedback('stdout-read-error', "Fail to read the stdout file of GPLSOL"), "red", ["bold"])
        else:
             TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
        exit(1)

# print GPLSOL stderr
if ENV['display_error']:
    print_separator(TAc, LANG)
    try:
        gplsol_error = mph.get_err_str()
        TAc.print(LANG.render_feedback("err-title", "The GPLSOL stderr is: "), "yellow", ["BOLD"])  
        TAc.print(LANG.render_feedback("stderr", f"{gplsol_error}"), "white", ["reverse"])
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'read-error':
            TAc.print(LANG.render_feedback('stderr-read-error', "Fail to read the stderr file of GPLSOL"), "red", ["bold"])
        else:
             TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
        exit(1)

# check GPLSOL solution
if ENV['check_solution']:
    print_separator(TAc, LANG)

    # Perform optimal solution with model_pirellone_lib
    opt_sol_subset = pl.get_opt_sol(instance)
    m = len(instance)
    n = len(instance[0])

    # Print instance
    TAc.print(LANG.render_feedback("instance-title", f"The matrix {m}x{n} is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{pl.instance_to_str(instance)}"), "white", ["bold"])
    print_separator(TAc, LANG)

    # Extract GPLSOL solution
    try:
        # Get raw solution
        raw_sol = mph.get_raw_solution()
        # Parse the raw solution
        gplsol_sol = process_user_sol(ENV, TAc, LANG, raw_sol, m=m, n=n)
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'read-error':
            TAc.print(LANG.render_feedback('solution-read-error', "Fail to read the solution file of GPLSOL"), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
        exit(1)

    # Print GPLSOL solution
    TAc.print(LANG.render_feedback("sol-title", "The GPLSOL solution is:"), "yellow", ["BOLD"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("out_sol", f"{pl.seq_to_str(gplsol_sol)}"), "white", ["reverse"])
        gplsol_sol = pl.seq_to_subset(gplsol_sol, m, n)
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("out_sol", f"{pl.subset_to_str(gplsol_sol)}"), "white", ["reverse"])
    print_separator(TAc, LANG)

    # Print optimal solution
    TAc.print(LANG.render_feedback("in-title", "The PirelloneLib solution is:"), "yellow", ["reverse"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("in-sol", f"{pl.seq_to_str(pl.subset_to_seq(opt_sol_subset))}"), "green", ["bold"])
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("in-sol", f"{pl.subset_to_str(opt_sol_subset)}"), "green", ["bold"])
    print_separator(TAc, LANG)

    # Check the correctness of the user solution
    check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, gplsol_sol)

exit(0)
