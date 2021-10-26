#!/usr/bin/env python3
from sys import exit
from itertools import zip_longest
import subprocess
import insert_sort_lib
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from sys import exit

# METADATA OF THIS TAL_SERVICE:
problem = "insert_sort"
service = "log_debug_your_insertion_sort_bot_server"
args_list = [
    ('feedback', str),
    ('lang', str),
]

# ENV = Env(problem, service, args_list)
# TAc = TALcolors(ENV)
# LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# TODO: convertire tutto in versione TAlight

def check_if_insert_sort(our_log, student_log, feedback):
    for e1, e2 in zip_longest(our_log, student_log):
        try:
            if "#LOG" in e2:
                if e1 != e2 and feedback == "tell_whats_right_instead":
                    print(f"YOURS: {e2} WRONG \u2718")
                    if "flush" in e1 and "flush" in e2:
                        trail = f"Ops! Flush operation from buffer is right, but {e2[-1]} is not the right array element."
                    elif "load" in e1 and "load" in e2:
                        trail = f"Ops! Load of the next element in buffer is right, but the value {e2[-1]} is not right."
                    elif "clone" in e1 and "clone" in e2:
                        trail = f"Ops! Cloning operation is right, but you are cloning the wrong element."
                    elif "compare" in e1 and "compare" in e2:
                        if e1[-3] != e2[-3]:
                            trail = f"Ops! You are comparing the wrong array element to the buffer."
                        else:
                            trail = f"Ops! Your comparison outcome is not right."
                    elif "output" in e1 and "output" in e2:
                        trail = f"Ops! Your final array is not right."
                    else:
                        trail = f"Ops! This is not the right operation."

                    print(trail + f" The right operation from the server should be: {e1}.")
                    exit(1)

                elif e1 != e2 and feedback == "just_signal_first_error":
                    print(f"YOURS: {e2} WRONG \u2718")
                    exit(1)

                print(f"YOURS: {e2} SERVER: {e1} OK \u2714")
        except TypeError:
            if len(our_log) > len(student_log):
                print("Ops! Your solution ends here, but not server's. \u2718")
                if feedback == "tell_whats_right_instead":
                    print(f"The next operation you should show is: {e1}.")
                    exit(1)
            else:
                print(
                    "Ops! So far so good, but server's solution ends here. Yours not. \u2718")
                exit(1)

    print("CONGRATS! Your bot is right. \u2714")


feedback = "tell_whats_right_instead"
try:
    student_output = subprocess.check_output("../bots/test_bot.py").decode("utf-8")
    student_log = list(student_output.split("\n")[:-1])

    input_array = []
    f = open("../public/input_examples/example_array_of_ints.encoded.txt", "r")

    for line in f.readlines():
        input_array.append(int(line.strip()))

    if input_array[0] != len(input_array) - 1:
        print("Ops! The first element of the array in the .txt file should be the total length of the array.")
        exit(1)

    our_insert_sort = insert_sort_lib.InsertSort(input_array[1:])
    our_log = our_insert_sort.generate_log_when_sorting()
    (check_if_insert_sort(our_log, student_log, feedback))

except subprocess.CalledProcessError as e:
    if "EOFError" in e.output.decode("utf-8"):
        print("Ops! The first element of the array in the .txt file should be the total length of the array.")
    elif "ValueError" in e.output.decode("utf-8"):
        print("Ops! You must enter only and at least 1 integer numbers in the .txt sample file.")
    else:
        print("Other error")
        exit(1)
