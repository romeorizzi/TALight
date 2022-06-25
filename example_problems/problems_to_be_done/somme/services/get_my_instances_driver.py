#!/usr/bin/env python3
from sys import exit,stdout, stderr
import os
import shutil
import ruamel
import random
from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper

import model_lcs_lib as ll


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_format',str),
    ('token',str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

if ENV.LOG_FILES is None:
    TAc.print(LANG.render_feedback("no-token", f"This service requires an access token. Write `rtal connect -x <YOUR_PRIVATE_AUTH_TOKEN> get_my_instances` to get your instances downloaded."), "red", ["bold"])
    exit(0)

service_dir_path = os.path.abspath(os.path.dirname(__file__))

GEN_file = os.path.join(service_dir_path,'GEN.yaml')

try:
  with open(GEN_file, 'r') as stream:
    try:
        GEN = ruamel.yaml.safe_load(stream)
    except BaseException as exc:
        for out in [stdout, stderr]:
            TAc.print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted.", "red", ["bold"])
            TAc.print(f" the GEN.yaml file `{GEN_file}` with the descriptors for the instances is corrupted (not a valid .yaml file).", "red", ["bold"])
            print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires this .yaml file.", file=out)
            print(exc, file=out)
        exit(1)
except IOError as ioe:
    for out in [stdout, stderr]:
        TAc.print(f"Internal error (please, report it to those responsible): the GEN.yaml file `{GEN_file}` with the descriptors for the instances could not be accessed.", "red", ["bold"])
        print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires to have access to this .yaml file.", file=out)
        print(ioe, file=out)
    exit(1)

#########################################

print(f"GEN={GEN}")

for instances_group in GEN:
    if GEN[instances_group]['source']=='random':
        seed=random.sample(range(100000, 999999),GEN[instances_group]['num_instances'])
        for id in seed:
            instance = ll.instance_randgen_1(GEN[instances_group]['m'], GEN[instances_group]['n'], GEN[instances_group]['alphabet'],id)

            instance_str = ll.instance_to_str(instance, format=ENV['instance_format'])

            output_filename = f"instance_{GEN[instances_group]}_{GEN[instances_group]['m']}_{GEN[instances_group]['n']}_{GEN[instances_group]['alphabet']}_{id}.{ENV['instance_format']}"

            fout = open(os.path.join(ENV.LOG_FILES,output_filename),'w')

            print(instance_str, file=fout)
            fout.close()

    elif GEN[instances_group]['source'] != 'random':
        # mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, group_dir)

        #leggo quali file ci sono nella cartella "ENV['group']"
        inst_path=os.listdir(group_dir)

        # scelgo due file random (diversi tra loro)
        file= random.sample(inst_path,GEN[instances_group]['num_instances'])
        # print(file)
        
        # scelgo due seed tra quelli proposti in id:{1,2,3,4,5}
        # seed=random.sample(list(GEN[instances_group]['id']),GEN[instances_group]['num_instances'])
        # print(seed)

        # copio i file nella cartella 'output'
        for instance in file:
            source=os.path.join(group_dir,instance)
            destination=ENV.LOG_FILES
            shutil.copy(source,destination)

      
        # instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['instance_format'])
        # instance = ll.get_instance_from_str(instance_str, format=ENV['instance_format'])
        # output_filename = f"instance_catalogue1_{ENV['instance_id']}.{ENV['instance_format']}"

exit(0)
