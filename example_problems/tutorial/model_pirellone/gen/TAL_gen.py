#!/usr/bin/env python3
from os import path, makedirs, system
from sys import argv, stderr, exit
import shutil, json


### Conventions #############################
GEN_FILE = "GEN"
INPUTS_DIR = "../inputs/"
GENERATOR_FILE = "instance_generator.py"
GENDICT_FILE = "gen_dictionary.json"
#############################################


# Get gen directory and generate utils path
GEN_DIR = argv[1]
GENDICT_FILE_PATH = path.join(GEN_DIR, GENDICT_FILE)
GEN_FILE_PATH = path.join(GEN_DIR, GEN_FILE)
INPUTS_DIR_PATH = path.join(GEN_DIR, INPUTS_DIR)
GENERATOR_PATH = path.join(GEN_DIR, GENERATOR_FILE)
if not path.exists(INPUTS_DIR_PATH):
    makedirs(INPUTS_DIR_PATH)

# Create GEN_DICT
with open(GEN_FILE_PATH, "r") as GEN_file:
    gen_lines = GEN_file.readlines()

# Init gendict:
gendict = dict()
instance_id = 0

# copy name associations: (instance_name, instance_id)
copy_name_id = dict()

# Parsing gen lines
formats_availables = list()
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
        source_rel_path = line[len(keyword):].strip()
        source_file_path = path.join(GEN_DIR, source_rel_path)
        format = ".".join(source_rel_path.split(".")[1:])
        if not path.exists(source_file_path):
            print(f"{source_file_path} Not exists!")
            exit(1)
        # Get instance and save (instance_name, instance_id)
        source_name = source_rel_path[:-(len(format)+1)] #e.g.: hardcoded/instance1
        if source_name not in copy_name_id:
            copy_name_id[source_name] = instance_id
            gendict[instance_id] = {'suite' : cur_suite}
            instance_id += 1
        cur_id = copy_name_id[source_name]
        # Get target path
        target_rel_path = f"instance{cur_id}.{format}"
        target_file_path = path.join(cur_suite_path, target_rel_path)
        shutil.copy(source_file_path, target_file_path)
        gendict[cur_id][format] = target_rel_path


    # CASE4:
    keyword = "GEN:"
    if line[:len(keyword)] == keyword:
        assert cur_suite_path != None, "GEN command before suit command"
        args = line[len(keyword):][:-1] # removed \n
        # Prepere gen-dictionary
        gendict[instance_id] = {'suite' : cur_suite}
        # Create file for each format
        for format in formats_availables:
            target_rel_path = f"instance{instance_id}.{format}"
            target_abs_path = path.join(cur_suite_path, target_rel_path)
            system(f"{GENERATOR_PATH} {args} {format} > {target_abs_path}")
            gendict[instance_id][format] = target_rel_path
        instance_id += 1

# save gen-dictionary:
with open(GENDICT_FILE_PATH, "w") as file:
    json.dump(gendict, file)

exit(0)
