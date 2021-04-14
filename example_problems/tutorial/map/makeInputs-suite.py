#!/usr/bin/env python3
from sys import argv, exit, stderr
import os

INPUT_FOLDER = argv[1]
INPUT_FORMAT = argv[2]
if INPUT_FORMAT == "dat":
    GENERATOR="./instance-generators/dat-generator.sh"
if INPUT_FORMAT == "txt":
    GENERATOR="./instance-generators/txt-generator.sh"

os.system(f"rm -rf {INPUT_FOLDER}")
os.system(f"mkdir {INPUT_FOLDER}")

def my_system_run(command_string):
    print("makeInputs.py:"+command_string)
    if os.system(command_string) != 0:
        print("\nIl seguente comando lanciato da makeInputs.py ha avuto qualche problema.\nmakeInputs.py:"+command_string+"\nEsecuzione di makeInputs.py interrotta a questo punto.")
        exit(1)

# Goal 1 instances:
# A few inputs hard-coded in the generator (could have been in separated files and here we could simply copy them):
my_system_run(f"cat examples/input_1.{INPUT_FORMAT} > {INPUT_FOLDER}/input_1.{INPUT_FORMAT}")

#parameters for generator.cpp:
# <N> <no_mines> <seed>

# Goal 2 instances:
for i in range(2,5):
    my_system_run(f"{GENERATOR} {i} 1 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal2-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

# Goal 3 instances:
for i in range(5,11):
    my_system_run(f"{GENERATOR} {i//2} 0 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal3-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

# Goal 4 instances:
for i in range(11,13):
    my_system_run(f"{GENERATOR} 10 0 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal4-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

# Goal 5 instances:
for i in range(13,16):
    my_system_run(f"{GENERATOR} 20 0 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal5-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

# Goal 6 instances:
for i in range(16,20):
    my_system_run(f"{GENERATOR} 30 0 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal6-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

# Goal 7 instances:
for i in range(20,21):
    my_system_run(f"{GENERATOR} 50 0 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal7-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

# Goal 8 instances:
for i in range(21,22):
    my_system_run(f"{GENERATOR} 100 0 {777+i} > {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")
#    my_system_run(f"./instance-generators/check_is_goal8-instance.py < {INPUT_FOLDER}/input_{i}.{INPUT_FORMAT}")

