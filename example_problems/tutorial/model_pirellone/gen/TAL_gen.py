#!/usr/bin/env python3
from os import path, makedirs, system
from sys import argv, stderr, exit
import shutil


### Conventions #############################
GEN_FILE = "GEN"
INPUTS_DIR = "../inputs/"
GENERATOR_NAME = "instance_generator.py"
#############################################


# Get gen directory and generate utils path
GEN_DIR = argv[1]
GEN_FILE_PATH = path.join(GEN_DIR, GEN_FILE)
INPUTS_DIR_PATH = path.join(GEN_DIR, INPUTS_DIR)
GENERATOR_PATH = path.join(GEN_DIR, GENERATOR_NAME)
if not path.exists(INPUTS_DIR_PATH):
    makedirs(INPUTS_DIR_PATH)

# Get list of lines of GEN file to be parsed.
with open(GEN_FILE_PATH, "r") as GEN_file:
    gen_lines = GEN_file.readlines()

# Init vars
formats_availables = list()
cur_suite_path = None
instance_n_for_suit = dict()

# Parsing gen lines
for line in gen_lines:
    #CASE1:
    keyword = "add_format:"
    if line[:len(keyword)] == keyword:
        new_format = line[len(keyword):].strip()
        if new_format in formats_availables:
            print(f"Error in your GEN file: the format {new_format} has been added more than once")
            exit(1)
        formats_availables.append(new_format)
            
    # CASE2:
    keyword = "suite:"
    if line[:len(keyword)] == keyword:
        cur_suite = line[len(keyword):].strip()
        cur_suite_path = path.join(INPUTS_DIR_PATH, cur_suite)
        # Check if suite has already been seen
        if cur_suite in instance_n_for_suit:
            print(f"Error in your GEN file: the suite {cur_suite} is declared more than once")
            exit(1)
        else:
            instance_n_for_suit[cur_suite] = 1
        # Check if this suite folder already exists
        if path.exists(cur_suite_path):
            print(f"Error {cur_suite_path} already exists")
            exit(1)
        else:
            makedirs(cur_suite_path)

    # CASE3:
    keyword = "COPY:"
    if line[:len(keyword)] == keyword:
        assert cur_suite_path != None, "COPY command before suit command"
        hardcode_file = line[len(keyword):].strip()
        source_file_path = path.join(GEN_DIR, "hardcoded", hardcode_file)
        # Check if this file path exists
        if not path.exists(source_file_path):
            print(f"{source_file_path} Not exists!")
            exit(1)
        target_file_path = path.join(cur_suite_path, hardcode_file)
        shutil.copy(source_file_path, target_file_path)
        
    # CASE4:
    keyword = "GEN:"
    if line[:len(keyword)] == keyword:
        assert cur_suite_path != None, "GEN command before suit command"
        args = line[len(keyword):][:-1] # removed \n
        # Create file for each format
        for format in formats_availables:
            target_file_path = path.join(cur_suite_path, \
                f"input{instance_n_for_suit[cur_suite]}.{format}")
            system(f"{GENERATOR_PATH} {args} {format} > {target_file_path}")
        instance_n_for_suit[cur_suite] += 1

exit(0)
