#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper, get_problem_path_from

import lcs_lib as ll


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('sol_format',str),
    ('dat_format',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START MATH_MODELING:

tests_dirname_list = ["public_examples", "at_most_10_DNA", "at_most_20_DNA", "at_most_30_uppercase", "at_most_40_lowercase", "at_most_50_lowercase_uppercase", "at_most_70_uppercase", "at_most_80_lowercase", "at_most_100_DNA"]

for test in reversed(tests_dirname_list):
    if test == ENV['goal']:
        break
    tests_dirname_list.remove(test)

dat_format = ''
txt_format = 'only_strings'

mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))

TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (your_mod_file.mod)."), "yellow")

mph.receive_mod_file(single_file_passed_to_the_bot=True)

total_passed_tests = 0
total_tests = 0
tests = {}

for test_dir in tests_dirname_list:
    tests[test_dir] = {}
    passed_dir_tests = 0
    total_dir_tests = 0

    TAc.print(LANG.render_feedback('test_dir', f"[TEST]: {test_dir}"), "green", ["bold"])

    for instance_id, paths in mph.get_instances_paths_in(test_dir).items():
                
        total_dir_tests += 1

        TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
        TAc.print(LANG.render_feedback('instance-id', f"Check instance id={instance_id}:"), "green", ["bold"])

        dat_file_path = paths[dat_format + 'dat']
        input_file_path = paths[txt_format + '.txt']

        input_str = mph.get_file_str_from_path(input_file_path)
        instance = ll.get_instance_from_txt(input_str, format=txt_format)
        m = len(instance[0])
        n = len(instance[1])

        mph.run_GLPSOL(dat_file_path)
        
        total_tests += 1

        glpsol_output = mph.get_out_str()

        if glpsol_output.find("NO PRIMAL") != -1:
            TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
            tests[test_dir][instance_id] = "NO!"
        else:
            raw_sol = mph.get_raw_sol()
            glpsol_sol = ll.read_annotated_subseq_sol(raw_sol)

            user_sol_subsequence = ll.annotated_subseq_to_sequence(glpsol_sol)
            user_sol_annotated_subseq = glpsol_sol

            if ENV['sol_format'] == 'subsequence':
                if ll.check_sol_feas_and_opt(TAc, LANG, ENV, user_sol_subsequence, instance[0], instance[1]):
                    total_passed_tests += 1
                    passed_dir_tests += 1
                    TAc.print(LANG.render_feedback('correct', "OK!"), "green", ["bold"])
                    tests[test_dir][instance_id] = "YES!"
                else:                    
                    tests[test_dir][instance_id] = "NO!"
                TAc.print(LANG.render_feedback("out_sol", f"Your solution:\n{ll.sequence_to_str(user_sol_subsequence)}"), "white", ["reverse"])
            elif ENV['sol_format'] == 'annotated_subseq':
                if ll.check_sol_feas_and_opt(TAc, LANG, ENV, user_sol_annotated_subseq, instance[0], instance[1]):
                    total_passed_tests += 1
                    passed_dir_tests += 1
                    TAc.print(LANG.render_feedback('correct', "OK!"), "green", ["bold"])
                    tests[test_dir][instance_id] = "YES!"
                else:
                    tests[test_dir][instance_id] = "NO!"
                TAc.print(LANG.render_feedback("out_sol", f"Your solution:\n{ll.render_annotated_subseq_as_str(user_sol_annotated_subseq)}"), "white", ["reverse"])

    
    TAc.print(LANG.render_feedback('dir-passed-tests', f'Your model has passed {passed_dir_tests} tests over {total_dir_tests} total tests in {test_dir} directory.'), "green", ["bold"])

TAc.print(LANG.render_feedback("separator", "\n<================>SUMMARY<================>"), "yellow", ["reverse"])
for test_dir in tests_dirname_list:
    TAc.print(LANG.render_feedback('test-dir', f'{test_dir}:'), "green", ["bold"])
    for test in tests[test_dir]:
        TAc.print(LANG.render_feedback('test-summary', f'instance_id: {test}\t\t passed: {tests[test_dir][test]}'), "green", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

TAc.print(LANG.render_feedback('passed-tests', f'Your model has passed {total_passed_tests} tests over {total_tests} total tests.'), "green", ["bold"])
exit(0)
