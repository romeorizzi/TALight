#!/usr/bin/env python3
from sys import exit, path
from multilanguage import Env, Lang, TALcolors

import asteroid_lib as al
from math_modeling import ModellingProblemHelper, get_problem_path_from


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('type_of_check',str),
    ('sol_style',str),
    ('dat_style',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START MATH_MODELING:
# Create list of test directory names to be test from the goal
tests_dirname_list = ["public_examples"]
tmp_tests_list = [  "m_and_n_at_most_5",   \
                    "m_and_n_at_most_10",  \
                    "m_and_n_at_most_20",  \
                    "m_and_n_at_most_30",  \
                    "m_and_n_at_most_50",  \
                    "m_and_n_at_most_100", \
                    "m_and_n_at_most_200", \
                    "m_and_n_at_most_300"  ]
# Remove useless test
for test in reversed(tmp_tests_list):
    if test == ENV['goal']:
        break
    tmp_tests_list.remove(test)

# Get formats
dat_style = ''                # default
txt_style = 'only_matrix'     # default

# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(get_problem_path_from(__file__))

# Get only model file
try:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (mod=your_mod_file.mod)."), "yellow")
    # Get mod
    mph.receive_mod_file(single_file_passed_to_the_bot=True)
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'write-error':
        TAc.print(LANG.render_feedback('write-error', f"Fail to create {err.args[1]} file"), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
    exit(1)

# Test all instance until the goal selected.
for test_dir in tests_dirname_list:
    # Print test_dir:
    TAc.print(LANG.render_feedback('test_dir', f"[TEST]: {test_dir}"), "green", ["bold"])
    try:
        instances_paths = mph.get_instances_paths_in(test_dir)
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'read-error':
            TAc.print(LANG.render_feedback('read-error', f"Fail to read {err.args[1]} file"), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
        exit(1)

    # For each instance
    for instance_id, paths in instances_paths.items():
        # Print instance_id:
        TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
        TAc.print(LANG.render_feedback('instance-id', f"Check instance id={instance_id}"), "green", ["bold"])

        # Extract paths
        dat_file_path = paths[dat_style + 'dat']
        input_file_path = paths[txt_style + '.txt']

        # Get input
        try:
            input_str = mph.get_file_str_from_path(input_file_path)
            instance = al.get_instance_from_txt(input_str, style=txt_style)
        except RuntimeError as err:
            err_name = err.args[0]
            # manage custom exceptions:
            if err_name == 'input-read-error':
                TAc.print(LANG.render_feedback('input-read-error', f"Fail to read {err.args[1]} file"), "red", ["bold"])
            elif err_name == 'dir-not-exist':
                TAc.print(LANG.render_feedback('dir-not-exist', f"This directory not exist: {err.args[1]}"), "red", ["bold"])
            elif err_name == 'invalid-id':
                TAc.print(LANG.render_feedback('invalid-id', f"id={err.args[1]} is invalid."), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
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
            elif err_name == 'invalid-id':
                TAc.print(LANG.render_feedback('invalid-id', f"id={err.args[1]} is invalid."), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name} in:\n{err.args[1]}"), "red", ["bold"])
            exit(1)

        # Perform optimal solution with serviceLib
        opt_sol_subset = "TODO1"# = al.get_opt_sol(instance)
        m = len(instance)
        n = len(instance[0])

        # Extract GPLSOL solution
        try:
            # Get raw solution
            raw_sol = mph.get_raw_solution()
            # Parse the raw solution
            gplsol_sol = "TODO2" #= process_user_sol(ENV, TAc, LANG, raw_sol, m=m, n=n)
        except RuntimeError as err:
            err_name = err.args[0]
            # manage custom exceptions:
            if err_name == 'read-error':
                TAc.print(LANG.render_feedback('solution-read-error', "Fail to read the solution file of GPLSOL"), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
            exit(1)

        # DEBUG:
        # print(input_str)
        # print(f'opt_sol_subset: {opt_sol_subset}')
        # print(f'gplsol_sol:     {gplsol_sol}')
            
        # Check the correctness of the user solution
        # if ENV['type_of_check'] == 'no':
        #     if opt_sol_subset == al.NO_SOL and gplsol_sol != al.NO_SOL:
        #         TAc.print(LANG.render_feedback('wrong', f">> Wrong!!!"), "green", ["bold"])
        #         exit(1)
        #     else:
        #         TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])
            
        # elif ENV['type_of_check'] == 'yes':
        #     if (opt_sol_subset == al.NO_SOL and gplsol_sol != al.NO_SOL) or \
        #         not al.check_sol(instance, gplsol_sol):
        #         TAc.print(LANG.render_feedback('wrong', f">> Wrong!!!"), "green", ["bold"])
        #         exit(1)
        #     else:
        #         TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])
            
        # elif ENV['type_of_check'] == 'min':
        #     opt_sol = al.subset_to_seq(opt_sol_subset) if ENV['sol_style'] == 'seq' else opt_sol_subset
        #     if opt_sol != gplsol_sol:
        #         TAc.print(LANG.render_feedback('wrong', f">> Wrong!!!"), "green", ["bold"])
        #         exit(1)
        #     else:
        #         TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])

exit(0)
