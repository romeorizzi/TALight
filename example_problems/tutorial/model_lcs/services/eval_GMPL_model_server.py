#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors

import model_lcs_lib as ll
from math_modeling import ModellingProblemHelper, get_problem_path_from


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('sol_style',str),
    ('dat_style',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START MATH_MODELING:

tests_dirname_list = ["public_examples", "m_and_n_at_least_5_dna", "m_and_n_at_least_20_lowercase", "m_and_n_at_least_20_lowercase_uppercase"]

for test in reversed(tests_dirname_list):
    if test == ENV['goal']:
        break
    tests_dirname_list.remove(test)

dat_style = ''
txt_style = 'only_strings'

mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))

TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (your_mod_file.mod)."), "yellow")

mph.receive_mod_file(single_file_passed_to_the_bot=True)

passed_tests = 0
total_tests = 0

for test_dir in tests_dirname_list:

    TAc.print(LANG.render_feedback('test_dir', f"[TEST]: {test_dir}"), "green", ["bold"])

    for instance_id, paths in mph.get_instances_paths_in(test_dir).items():

        TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
        TAc.print(LANG.render_feedback('instance-id', f"Check instance id={instance_id}:"), "green", ["bold"])

        dat_file_path = paths[dat_style + 'dat']
        input_file_path = paths[txt_style + '.txt']

        input_str = mph.get_file_str_from_path(input_file_path)
        instance = ll.get_instance_from_txt(input_str, style=txt_style)
        m = len(instance[0])
        n = len(instance[1])

        annotated_subseq_sol = ll.get_sol(instance[0], instance[1], m, n)

        mph.run_GLPSOL(dat_file_path)

        glpsol_output = mph.get_out_str()
        total_tests += 1
        if glpsol_output.find("NO PRIMAL") != -1:
            TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
        else:
            raw_sol = mph.get_raw_sol()
            glpsol_sol = ll.process_user_sol(raw_sol)

            user_sol_subsequence = ll.annotated_subseq_to_sequence(glpsol_sol)
            user_sol_annotated_subseq = glpsol_sol

            if ENV['sol_style'] == 'subsequence':
                if ll.check_sol(TAc, LANG, ENV, user_sol_subsequence, instance[0], instance[1]):
                    passed_tests += 1
                    TAc.print(LANG.render_feedback('correct', "OK!"), "green", ["bold"])
                TAc.print(LANG.render_feedback("out_sol", f"Your solution:\n{ll.sequence_to_str(user_sol_subsequence)}"), "white", ["reverse"])
            elif ENV['sol_style'] == 'annotated_subseq':
                if ll.check_sol(TAc, LANG, ENV, user_sol_annotated_subseq, instance[0], instance[1]):
                    passed_tests += 1
                    TAc.print(LANG.render_feedback('correct', "OK!"), "green", ["bold"])
                TAc.print(LANG.render_feedback("out_sol", f"Your solution:\n{ll.annotated_subseq_to_str(user_sol_annotated_subseq)}"), "white", ["reverse"])


TAc.print(LANG.render_feedback('passed-tests', f'Your model has passed {passed_tests} tests over {total_tests} total tests.'), "green", ["bold"])
exit(0)
