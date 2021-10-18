#!/usr/bin/env python3
import os
from sys import argv, stderr, exit
import shutil

GEN_filename = argv[1]
with open(GEN_filename, "r") as GEN_file:
    lines = GEN_file.readlines()

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
INPUTS_DIR = os.path.join(CUR_DIR, "inputs")
cur_suite = None
cur_suite_dir = None
num_instances_in_the_suit = {}
formats = []
for line in lines:
    if line[:len("add_format:")] == "add_format:":
        new_format = line[len("add_format:"):].strip())
        if new_format in formats:
            print(f"Error in your GEN file: the format {new_format} has been added more than once")
            exit(1)
        formats.append(new_format)
            
    if line[:6] == "suite:":
        cur_suite = line[6:].strip())
        cur_suite_dir = os.path.join(INPUTS_DIR, cur_suite)
        if cur_suite_dir in num_instances_in_the_suit:
            print(f"Error in your GEN file: the suite {cur_suite_dir} is declared more than once")
            exit(1)
        num_instances_in_the_suit[cur_suite_dir] = 0
        if not os.path.exists(cur_suite_dir):
            os.makedirs(cur_suite_dir)
        
    if line[:5] == "COPY:":
        source_file = os.path.join(CUR_DIR,line[5:].strip())
        assert cur_suite_dir != None and os.path.exists(cur_suite_dir)
        extended_extension = ".".join(source_file.split(".")[1:])
        target_file = os.path.join(cur_suite_dir,f"input{num_instances_in_the_suit[cur_suite]}.{extended_extension}"))
        shutil.copyfile(source_file, target_file)
        
    if line[:4] == "GEN:":
        line_of_args = line[4:]
        assert cur_suite_dir != None and os.path.exists(cur_suite_dir)
        for extended_extension in formats:
            target_file = os.path.join(cur_suite_dir,f"input{num_instances_in_the_suit[cur_suite]}.{extended_extension}"))
            sys.exec(f"./instance_generator.py {line_of_args} {extended_extension} > {target_file}")

exit(0)
