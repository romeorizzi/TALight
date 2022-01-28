#!/usr/bin/env python3
from os import path, makedirs, symlink, system
from sys import argv, stderr, exit
import shutil, json


### Conventions #############################
CATALOGUE_GENERATION_INSTRUCTIONS_FILENAME = "GEN"
CATALOGUE_NAME = "instances_catalogue"
WHOLECATALOGUE_COLLECTION_NAME = "all_instances"
GENDICT_FILENAME = "gen_dictionary.json"
#############################################


# Get gen directory and generate utils path
GEN_FULLPATH = argv[1]
INSTRUCTIONS_FILE_FULLPATH = path.join(GEN_FULLPATH, CATALOGUE_GENERATION_INSTRUCTIONS_FILENAME)
CATALOGUE_FULLNAME = path.join(GEN_FULLPATH, "..", CATALOGUE_NAME)
WHOLECATALOGUE_SUBFOLDER_FULLNAME = path.join(CATALOGUE_FULLNAME, WHOLECATALOGUE_COLLECTION_NAME)
GENDICT_FULLPATH = path.join(CATALOGUE_FULLNAME, GENDICT_FILENAME)
if not path.exists(CATALOGUE_FULLNAME):
    makedirs(CATALOGUE_FULLNAME)
if not path.exists(WHOLECATALOGUE_SUBFOLDER_FULLNAME):
    makedirs(WHOLECATALOGUE_SUBFOLDER_FULLNAME)

# Create GEN_DICT
with open(INSTRUCTIONS_FILE_FULLPATH, "r") as file:
    gen_lines = file.readlines()

# Init gendict:
gendict = dict()
instance_id = 1
instance_id_as_str = str(instance_id).zfill(3)

# copy name associations: (instance_name, instance_id_as_str)
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
    keyword = "collection:"
    if line[:len(keyword)] == keyword:
        line_recognized = True
        cur_collection = line[len(keyword):].strip()
        cur_collection_path = path.join(CATALOGUE_FULLNAME, cur_collection)
        # Check if this collection folder already exists
        if path.exists(cur_collection_path):
            print(f"Error {cur_collection_path} already exists")
            exit(1)
        else:
            makedirs(cur_collection_path)

    # CASE3:
    keyword = "COPY:"
    if line[:len(keyword)] == keyword:
        assert cur_collection_path != None, "COPY command before suit command"
        line_recognized = True
        source_rel_path = line[len(keyword):].strip()
        source_file_path = path.join(GEN_FULLPATH, source_rel_path)
        file_full_extension = ".".join(source_rel_path.split(".")[1:])
        if not path.exists(source_file_path):
            print(f"{source_file_path} Not exists!")
            exit(1)
        # Get instance and save (instance_name, instance_id_as_str)
        source_name = source_rel_path[:-(len(file_full_extension)+1)] #e.g.: hardcoded/instance1
        if source_name not in copy_name_id:
            print("WARNING overlaps: source_name not in copy_name_id")
            copy_name_id[source_name] = instance_id_as_str
            gendict[instance_id_as_str] = {'collection' : cur_collection}
            instance_id += 1
            instance_id_as_str = str(instance_id).zfill(3)
        cur_id = copy_name_id[source_name]
        print(f"\nGEN instance_id={cur_id}, by COPY")
        print(f"-source_name={source_name}")
        print(f"-copy_name_id={copy_name_id}")
        # Get target path
        target_filename = f"instance{cur_id}.{file_full_extension}"
        print(f"target_filename={target_filename}")
        target_abs_fullpath = path.join(cur_collection_path, target_filename)
        print(f"target_abs_fullpath={target_abs_fullpath}")
        shutil.copy(source_file_path, target_abs_fullpath)
        symlink(target_abs_fullpath, path.join(WHOLECATALOGUE_SUBFOLDER_FULLNAME,target_filename))
        gendict[cur_id][file_full_extension] = target_filename

    # CASE4:
    keyword = "GEN:"
    if line[:len(keyword)] == keyword:
        assert cur_collection_path != None, "GEN command before suit command"
        line_recognized = True
        generator_line = line[len(keyword):][:-1] # removed \n
        generator_executable, args = generator_line.split(maxsplit=1)
        generator_command = path.join(GEN_FULLPATH, generator_executable)
        # Prepere gen-dictionary
        gendict[instance_id_as_str] = {'collection' : cur_collection}
        # Create file for each format to be made available
        for file_full_extension in formats_availables:
            target_filename = f"instance_{instance_id_as_str}.{file_full_extension}"
            target_abs_fullpath = path.join(cur_collection_path, target_filename)
            system(f"{generator_command} {args} {file_full_extension} > {target_abs_fullpath}")
            symlink(target_abs_fullpath, path.join(WHOLECATALOGUE_SUBFOLDER_FULLNAME,target_filename))

            gendict[instance_id_as_str][file_full_extension] = target_filename
        print(f"\nInstance {instance_id_as_str} generated and put in the collection `{cur_collection}`.")
        instance_id += 1
        instance_id_as_str = str(instance_id).zfill(3)

    if not line_recognized:
        print(f"Error: an uncommented line of your GEN file has not been recognized\n   line={line}")
        exit(1)


# save gen-dictionary:
with open(GENDICT_FULLPATH, "w") as file:
    json.dump(gendict, file)

exit(0)
