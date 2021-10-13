#!/usr/bin/env python3
import subprocess
import os
#import turingarena as ta

from sys import exit
import re
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="validate_GMPL_model"
args_list = [
    ('goal',str),
    ('seed',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 



# evaluator for TuringArena
# to launch this evaluator, use this command:
#     turingarena-dev evaluate --store-files sol/soluzione_triangolo_gmpl.mod


def evaluate_solution(mod, dat):
    
    # here I start a subprocess to evaluate the submission
    # glpsol writes the result in output.txt

    try:
        subprocess.run([
            "glpsol", 
            "-m", mod, 
            "-d", dat
        ], cwd=ta.get_temp_dir(), timeout=5.0)
    except subprocess.TimeoutExpired:
        print("Too much computing time! Deadline exceeded.")
        return None
    except subprocess.CalledProcessError as e: 
        print ("The call to glpsol on your .dat file returned error")
        return None
    except Exception as e:
        print ("Processing returned with error")
        print(f" error: {e}")
        return None

    # here I read the result file and return it
    try:
        with open(os.path.join(ta.get_temp_dir(), "output.txt")) as output:
            actual_output_file = output.readlines()
            actual_row_vals = tuple(map(int,actual_output_file[0].split()))
            actual_col_vals = tuple(map(int,actual_output_file[1].split()))
    except os.error as e:
        print(f" error: {e}")
        print("... sembra che glpsol non sia riuscito a creare il file output.txt")
        return None
    return (actual_row_vals, actual_col_vals)

# get the number of test cases
try:
    N = len(os.listdir("inputs-suite.dat/"))
    print(f"We are going to validate your model on {N} different testcases.")
except os.error as e:
    print(f" error: {e}")
    print("... sembra che non si trovi la cartella con gli input.\nHai lanciato -/makeInputs.py per allestire il problema?")
    exit(1)

testcases = {}
goals = [
    "example_of_statement",
    "m_n_at_most_5_solvable",
    "m_n_at_most_5_unsolvable",
    "m=n=10",
    "m=n=20",
    "m=n=30",
    "m=n=50",
    "m=n=100",
    "m=n=200",
    "m=n=300",
]

n_instances = [1,3,3,2,2,2,2,2,2,2]
ps_n_instances = [0]
for num in n_instances:
    ps_n_instances.append(num+ps_n_instances[-1])
#print(f"ps_n_instances = {ps_n_instances}")
n_goal = 0
for i in range(1,N+1):
    input = os.path.join(os.getcwd(), f"inputs-suite.dat/input_{i}.dat")
    try:
        output = os.path.join(os.getcwd(), f"outputs-suite.txt/output_{i}.txt")
    except os.error as e:
        print(f" error: {e}")
        print("... sembra che non si trovi un file di output.\nHai lanciato -/makeOutputs.sh per allestire il problema?")
        exit(1)

    # read the expected result
    with open(output) as out:
        expected_output_file = out.readlines()
        expected_row_vals = tuple(map(int,expected_output_file[0].split()))
        expected_col_vals = tuple(map(int,expected_output_file[1].split()))
        expected_result = (expected_row_vals, expected_col_vals)
        
    # evaluate the test case
    print(f"\nEvaluting your model on Testcase_{i} (for goal {goals[n_goal]}):")
    result = evaluate_solution(os.path.join(os.getcwd(), ta.submission.source), input)
    def are_equiv(result,expected_result):
        if result == expected_result:
            return True
        if (tuple(1-v for v in result[0]),tuple(1-v for v in result[1])) == expected_result:
            return True
        print(((1-v for v in result[0]),(1-v for v in result[1])))
        return False
    if result is not None and are_equiv(result,expected_result):
        print(f"Testcase_{i}: Correct!")
        testcases[f"case_{i}"] = "correct"
        if ps_n_instances[n_goal+1] == i:
            ta.goals.setdefault(goals[n_goal], True)
            n_goal += 1
    else:
        print(((1-v for v in result[0]),(1-v for v in result[1])))
        for g in goals[n_goal:]:
            ta.goals[g] = False
        ta.send_file(input, filename=f"input_where_your_sol_goes_bad.dat")
        print(f"Testcase_{i}: Wrong!")
        testcases[f"case_{i}"] = "wrong"
        print(f"Ti ho messo il file .dat con l'input su cui il tuo modello perde colpi nel file  generated-files/input_where_your_sol_goes_bad.dat")
        print(f"{((1-v for v in result[0]),(1-v for v in result[1]))}")
        if result is None:
            print("\nThe .dat file that glpsol has received in input together with your model is the file  generated-files/input_where_your_sol_goes_bad.dat")
        else:
            print(f"According to your model the optimum maximum value is {result}, but we think it is {expected_result}. The instance on which we disagree is in the file  generated-files/input_where_your_sol_goes_bad.dat")
        if n_goal <= 4:
            print("\nSince it is actually small, we can display here below the .dat file on which your model goes bad:\n")
            with open(os.path.join(ta.get_temp_dir(), input)) as testcase_input:
                print(testcase_input.read())
        break

for i,val in testcases.items():
    print(i,": ",val)

print(ta.goals)

if ta.goals["m=n=100"] == True:
    ta.send_file(os.path.join(os.getcwd(), "models/gallery_of_models/pirellone_LP-model-gmpl.mod"), filename="pirellone_LP-model-gmpl.mod")
    ta.send_file(os.path.join(os.getcwd(), "models/gallery_of_models/discussion2.md"), filename="discussion2.md")
    print(f"In base ai goals che hai raggiunto, ti ho messo dei file con delle considerazioni e soluzioni di riferimento nella cartella generated-files.")

if ta.goals["m=n=20"] and not ta.goals["m=n=100"] :
    ta.send_file(os.path.join(os.getcwd(), "models/gallery_of_models/pirellone_ILP-model-gmpl.mod"), filename="pirellone_ILP-model-gmpl.mod")
    ta.send_file(os.path.join(os.getcwd(), "pirellone_ILP-model-ampl.mod"), filename="model_PLIpirellone_ampl.mod")
    ta.send_file(os.path.join(os.getcwd(), "models/gallery_of_models/discussion1.md"), filename="discussion1.md")
    print("In base ai goals che hai raggiunto, ti ho messo dei file con delle considerazioni e soluzioni di riferimento nella cartella generated-files. Sono inoltre presenti suggerimenti su come raggiungere i goal superiori.")
        
