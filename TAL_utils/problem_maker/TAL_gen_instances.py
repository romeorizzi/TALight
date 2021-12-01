#!/usr/bin/env python3
from os import path, makedirs, system
from sys import argv, stderr, exit
import shutil, json


### Conventions #############################
COMMANDS_FILENAME = "GEN"
INSTANCES_DIRNAME = "instances"
GENERATOR_FILENAME = "instance_generator.py"
GENDICT_FILENAME = "gen_dictionary.json"
#############################################


# Get gen directory and generate utils path
GEN_FULLPATH = argv[1]
COMMANDS_FULLPATH = path.join(GEN_FULLPATH, COMMANDS_FILENAME)
INSTANCES_DIRNAME_PATH = path.join(GEN_FULLPATH, "..", INSTANCES_DIRNAME)
GENDICT_FULLPATH = path.join(INSTANCES_DIRNAME_PATH, GENDICT_FILENAME)
GENERATOR_PATH = path.join(GEN_FULLPATH, GENERATOR_FILENAME)
if not path.exists(INSTANCES_DIRNAME_PATH):
    makedirs(INSTANCES_DIRNAME_PATH)

# Create GEN_DICT
with open(COMMANDS_FULLPATH, "r") as file:
    gen_lines = file.readlines()

# Init gendict:
gendict = dict()
instance_id = 1

# copy name associations: (instance_name, instance_id)
copy_name_id = dict()

# Parsing gen lines
formats_availables = list()
for line in gen_lines:
    if line[0] == "#" or line.strip()=="":
        continue
    line_recognized = False
    #CASE1:
    keyword = "add_format:"
    if line[:len(keyword)] == keyword:
        line_recognized = True
        new_format = line[len(keyword):].strip()
        if new_format in formats_availables:
            print(f"Error in your GEN file: the format {new_format} has been added more than once")
            exit(1)
        formats_availables.append(new_format)
            
    # CASE2:
    keyword = "suite:"
    if line[:len(keyword)] == keyword:
        line_recognized = True
        cur_suite = line[len(keyword):].strip()
        cur_suite_path = path.join(INSTANCES_DIRNAME_PATH, cur_suite)
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
        line_recognized = True
        source_rel_path = line[len(keyword):].strip()
        source_file_path = path.join(GEN_FULLPATH, source_rel_path)
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
        target_filename = f"instance{cur_id}.{format}"
        target_abs_fullpath = path.join(cur_suite_path, target_filename)
        shutil.copy(source_file_path, target_abs_fullpath)
        gendict[cur_id][format] = target_filename

    # CASE4:
    keyword = "GEN:"
    if line[:len(keyword)] == keyword:
        assert cur_suite_path != None, "GEN command before suit command"
        line_recognized = True
        args = line[len(keyword):][:-1] # removed \n
        # Prepere gen-dictionary
        gendict[instance_id] = {'suite' : cur_suite}
        # Create file for each format
        for format in formats_availables:
            target_filename = f"instance{instance_id}.{format}"
            target_abs_fullpath = path.join(cur_suite_path, target_filename)
            system(f"{GENERATOR_PATH} {args} {format} > {target_abs_fullpath}")
            gendict[instance_id][format] = target_filename
        print(f"generated instance with instance_id={instance_id}")
        instance_id += 1

    if not line_recognized:
        print(f"Error: an uncommented line of your GEN file has not been recognized\n   line={line}")
        exit(1)


# save gen-dictionary:
with open(GENDICT_FULLPATH, "w") as file:
    json.dump(gendict, file)

exit(0)
