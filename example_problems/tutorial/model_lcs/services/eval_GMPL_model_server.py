#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

import model_pirellone_lib as pl
from model_utils import ModellingProblemHelper, get_problem_path_from
from services_utils import process_user_sol, print_separator, check_sol_with_feedback


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('type_of_check',str),
    ('sol_style',str),
    ('only_solvable_instances',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Create list of test directory names to be test from the goal
tests_dirname_list = [  "public_examples",    \
                        "m_and_n_at_most_5",  \
                        "m_and_n_at_10",      \
                        "m_and_n_at_20",      \
                        "m_and_n_at_30",      \
                        "m_and_n_at_50",      \
                        "m_and_n_at_100",     \
                        "m_and_n_at_200",     \
                        "m_and_n_at_300"      ]
for test in reversed(tests_dirname_list):
    if test == ENV['goal']:
        break
    tests_dirname_list.remove(test)

# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(get_problem_path_from(__file__))

# Get only model file
try:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod)."), "yellow")
    # Get mod
    mph.receive_mod_file()
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'write-error':
        TAc.print(LANG.render_feedback('write-error', f"Fail to create {err.args[1]} file"), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
    exit(0)

# Test all instance until the goal selected.
for test_dir in tests_dirname_list:
    mph.get_paths_in(test_dir)
    exit(0)


    for instances_files in mph.get_paths_in(test_dir):
        pass

    # Get input
    try:
        input_str = mph.get_input_from_archive(test_dir)
        instance = pl.get_pirellone_from_str(input_str)
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'input-read-error':
            TAc.print(LANG.render_feedback('input-read-error', f"Fail to read {err.args[1]} file"), "red", ["bold"])
        elif err_name == 'dir-not-exist':
            TAc.print(LANG.render_feedback('dir-not-exist', f"This directory not exist: {err.args[1]}"), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
        exit(0)

    # Perform optimal solution with model_pirellone_lib
    opt_sol_subset = pl.get_opt_sol(instance)
    m = len(opt_sol_subset[0])
    n = len(opt_sol_subset[1])
    
    # Get all dat_path in this test directory
    for dat_path in mph.get_dat_paths_from_archive(test):
        instance_name = dat_path.split("/")[-1][:-4]
        TAc.print(LANG.render_feedback('instance_title', f"CHECK: {instance_name}"), "red", ["bold"])

        # Perform solution with GPLSOL
        try:
            mph.run_GPLSOL(file_dat_path=dat_path)
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
                TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
            exit(0)

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
                TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
            exit(0)
        
        # Check the correctness of the user solution
        opt_sol = pl.subset_to_seq(opt_sol_subset) if ENV['sol_style'] == 'seq' else opt_sol_subset
        if opt_sol_subset == gplsol_sol:
            pass
        # ALTERNATIVE:
        # check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, gplsol_sol)

exit(0)
