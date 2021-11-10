#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

import asteroid_lib as al
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


# START MATH_MODELING:
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
        input_str = mph.get_file_str_from_id(ENV['instance_id'], format=(txt_style+'.txt'))
    if ENV['check_solution']:
        instance = al.get_instance_from_txt(input_str, style=txt_style)
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
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
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
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
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
 
# Extract GPLSOL solution
try:
    # Get raw solution
    raw_sol = [line for line in mph.get_raw_solution() if len(line.strip()) > 0 ]
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'read-error':
        TAc.print(LANG.render_feedback('solution-read-error', "Fail to read the solution file of GPLSOL"), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
    exit(1)

# print GPLSOL solution.txt
if ENV['display_solution']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    for line in raw_sol:
        print(line)

# check GPLSOL solution
if ENV['check_solution']:
    m = len(instance)
    n = len(instance[0])
    # Parse the raw solution
    gplsol_sol = al.process_user_sol(ENV, TAc, LANG, raw_sol, m=m, n=n)
    TAc.print(LANG.render_feedback("sol-title", "The GPLSOL solution is:"), "yellow", ["BOLD"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("out_sol", f"{al.seq_to_str(gplsol_sol)}"), "white", ["reverse"])
        gplsol_sol = al.seq_to_subset(gplsol_sol, m, n)
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("out_sol", f"{al.subset_to_str(gplsol_sol)}"), "white", ["reverse"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    
    # START CODING YOUR SERVICE:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Get optimal solution
    opt_sol_subset = al.min_cover(m,n,instance)
    print(f"opt_sol_subset={opt_sol_subset}")

    # Print instance
    TAc.print(LANG.render_feedback("instance-title", f"The matrix {m}x{n} is:"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance", f"{al.instance_to_str(instance)}"), "white", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

    # Print optimal solution
    TAc.print(LANG.render_feedback("in-title", "The ServiceLib solution is:"), "yellow", ["reverse"])
    if ENV['sol_style'] == 'seq':
        TAc.print(LANG.render_feedback("in-sol", f"{al.seq_to_str(al.subset_to_seq(opt_sol_subset))}"), "green", ["bold"])
    elif ENV['sol_style'] == 'subset':
        TAc.print(LANG.render_feedback("in-sol", f"{al.subset_to_str(opt_sol_subset)}"), "green", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])


    # Check the correctness of the user solution
    # Init
    opt_sol_seq = al.subset_to_seq(opt_sol_subset)
    if ENV['sol_style'] == 'seq':
        user_sol_subset = al.seq_to_subset(gplsol_sol, ENV['m'], ENV['n'])
        user_sol_seq = gplsol_sol
    else:
        user_sol_seq = al.subset_to_seq(gplsol_sol)
        user_sol_subset = gplsol_sol
    # check if is correct
    # is_correct, certificate_of_no = al.check_sol(instance, user_sol_subset)
    # if is_correct:
    #     TAc.OK()
    #     TAc.print(LANG.render_feedback('correct', "The solution is correct."), "green", ["bold"])
    # else:
    #     TAc.NO()
    #     TAc.print(LANG.render_feedback('error', f"The solution is not correct. The pirellone cell in row={certificate_of_no[0]} and col={certificate_of_no[1]} stays on."), "red", ["bold"])
    #     exit(0)
    # # check if is minimal
    # if ENV['sol_style'] == 'seq':
    #     if len(opt_sol_seq) != len(user_sol_seq):
    #         TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
    #         exit(0)
    # elif ENV['sol_style'] == 'subset':
    #     if not al.is_optimal(user_sol_subset):
    #         TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
    #         exit(0)
    # TAc.print(LANG.render_feedback('minimal', "The solution is minimal!"), "green", ["bold"])


exit(0)
