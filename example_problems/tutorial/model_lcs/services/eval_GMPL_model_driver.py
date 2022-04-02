#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper

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

goals = ["hardcoded", "DNA_strlen_at_most_10", "DNA_strlen_at_most_20", "uppercase_strlen_at_most_30", "lowercase_strlen_at_most_40", "lowercase_uppercase_strlen_at_most_50", "suppercase_strlen_at_most_80", "DNA_strlen_at_most_100"]
tests_dirname_list = ["instances_" + goal for goal in goals]
#print(f"{tests_dirname_list=}")

for test in reversed(tests_dirname_list):
    if test == "instances_" + ENV['goal']:
        break
    tests_dirname_list.remove(test)
print(f"{tests_dirname_list=}")
    
dat_format = ENV['dat_format']
instance_format = 'only_strings'

mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)

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

        dat_file_path = paths[ll.format_name_to_file_extension(dat_format,'instance')]
        input_file_path = paths[ll.format_name_to_file_extension(instance_format,'instance')]

        input_str = mph.get_file_str_from_path(input_file_path)
        instance = ll.get_instance_from_txt(input_str, instance_format)
        m = len(instance[0])
        n = len(instance[1])

        mph.run_GLPSOL(dat_file_fullpath=dat_file_path)
        
        total_tests += 1

        glpsol_output = mph.get_out_str()

        if glpsol_output.find("NO PRIMAL") != -1:
            TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
            tests[test_dir][instance_id] = "NO!"
        else:
            raw_sol = mph.get_raw_sol()
            if ENV['sol_format'] == 'subseq':
                user_sol = raw_sol
                TAc.print(LANG.render_feedback("print-out-sol-subseq", f"The solution obtained by your model:\n{ll.sequence_to_str(user_sol)}"), "white", ["reverse"])
            if ENV['sol_format'] == 'annotated_subseq':
                user_sol = user_sol_annotated_subseq = ll.read_annotated_subseq("\n".join(raw_sol)+"\n")
                TAc.print(LANG.render_feedback("print-out-sol-annotated-subseq", f"The solution obtained by your model:\n{ll.render_annotated_subseq_as_str(user_sol_annotated_subseq)}"), "white", ["reverse"])

            if ll.check_sol_feas_and_opt(TAc, LANG, user_sol, ENV['sol_format'], instance[0], instance[1]):
                total_passed_tests += 1
                passed_dir_tests += 1
                TAc.print(LANG.render_feedback('correct', "OK!"), "green", ["bold"])
                tests[test_dir][instance_id] = "YES!"
            else:                    
                tests[test_dir][instance_id] = "NO!"
    
    TAc.print(LANG.render_feedback('dir-passed-tests', f'Your model has passed {passed_dir_tests} tests over {total_dir_tests} total tests in {test_dir} directory.'), "green", ["bold"])

TAc.print(LANG.render_feedback("separator", "\n<================>SUMMARY<================>"), "yellow", ["reverse"])
for test_dir in tests_dirname_list:
    TAc.print(LANG.render_feedback('test-dir', f'{test_dir}:'), "green", ["bold"])
    for test in tests[test_dir]:
        TAc.print(LANG.render_feedback('test-summary', f'instance_id: {test}\t\t passed: {tests[test_dir][test]}'), "green", ["bold"])
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])

TAc.print(LANG.render_feedback('passed-tests', f'Your model has passed {total_passed_tests} tests over {total_tests} total tests.'), "green", ["bold"])
exit(0)
