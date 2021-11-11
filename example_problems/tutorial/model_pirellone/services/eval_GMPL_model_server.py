#!/usr/bin/env python3
from sys import exit, path
from multilanguage import Env, Lang, TALcolors

import model_pirellone_lib as pl
from math_modeling import ModellingProblemHelper, get_problem_path_from
from services_utils import process_user_sol, print_separator


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('type_of_check',str),
    ('only_solvable_instances',bool),
    ('sol_style',str),
    ('dat_style',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
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

# Add real folders name
for test in tmp_tests_list:
    tests_dirname_list.append(test + '_solvable')
    if not ENV['only_solvable_instances']:
        tests_dirname_list.append(test + '_unsolvable')


# Get formats
dat_style = ''                # default
txt_style = 'only_matrix'     # default


# Initialize ModellingProblemHelper
mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))


# Receive only model file
TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (your_mod_file.mod)."), "yellow")
# Get mod
mph.receive_mod_file(single_file_passed_to_the_bot=True)


# Test all instance until the goal selected.
for test_dir in tests_dirname_list:
    # Print test_dir:
    TAc.print(LANG.render_feedback('test_dir', f"[TEST]: {test_dir}"), "green", ["bold"])

    # For each instance in test_dir
    for instance_id, paths in mph.get_instances_paths_in(test_dir).items():
        # Print instance_id:
        print_separator(TAc, LANG)
        TAc.print(LANG.render_feedback('instance-id', f"Check instance id={instance_id}:"), "green", ["bold"])

        # Extract paths
        dat_file_path = paths[dat_style + 'dat']
        input_file_path = paths[txt_style + '.txt']

        # Get input
        input_str = mph.get_file_str_from_path(input_file_path)
        instance = pl.get_instance_from_txt(input_str, style=txt_style)
        m = len(instance)
        n = len(instance[0])

        # Perform optimal solution
        opt_sol_subset = pl.get_opt_sol(instance)

        # Check if skip
        if ENV['only_solvable_instances'] and \
           test_dir == 'public_examples' and \
           opt_sol_subset == pl.NO_SOL:
           print("skipped")
           continue
        
        # Perform solution with GPLSOL
        mph.run_GLPSOL(dat_file_path)

        # Get raw solution and parse it
        raw_sol = mph.get_raw_sol()
        gplsol_sol = process_user_sol(ENV, TAc, LANG, raw_sol, m=m, n=n)

        # DEBUG:
        # print(f'opt_sol_subset: {opt_sol_subset}')
        # print(f'gplsol_sol:     {gplsol_sol}')

        # Check the correctness of the user solution
        if (opt_sol_subset == pl.NO_SOL and gplsol_sol != pl.NO_SOL) or \
           (opt_sol_subset != pl.NO_SOL and gplsol_sol == pl.NO_SOL):
            # case: not both NO_SOL or not both SOL
            TAc.print(LANG.render_feedback('wrong', f">> Wrong!!!"), "green", ["bold"])
            exit(0)
        if opt_sol_subset == pl.NO_SOL and gplsol_sol == pl.NO_SOL:
            # case: both NO_SOL
            TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])
        else:
            # case: both SOL
            if ENV['type_of_check'] == 'no':
                TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])
            elif ENV['type_of_check'] == 'yes':
                is_correct, certificate_of_no = pl.check_sol(instance, gplsol_sol)
                if not is_correct:
                    TAc.print(LANG.render_feedback('wrong', f">> Wrong!!!"), "green", ["bold"])
                    exit(0)
                else:
                    TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])
            elif ENV['type_of_check'] == 'min':
                opt_sol = pl.subset_to_seq(opt_sol_subset) if ENV['sol_style'] == 'seq' else opt_sol_subset
                if opt_sol != gplsol_sol:
                    TAc.print(LANG.render_feedback('wrong', f">> Wrong!!!"), "green", ["bold"])
                    exit(0)
                else:
                    TAc.print(LANG.render_feedback('correct', f">> Correct"), "green", ["bold"])
        # ALTERNATIVE:
        # check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, gplsol_sol)

exit(0)
