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
    ('group',str),
    ('instance_format',str),
    ('token',str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

service_dir_path = os.path.abspath(os.path.dirname(__file__))
#print(f'__file__={__file__}')
#print(f'service_dir_path={service_dir_path}')

GEN_file = os.path.join(service_dir_path,'GEN.yaml')

#cartella in cui ci saranno i cataloghi scritti dal docente
group_dir = os.path.join(ENV.META_DIR,'instances',ENV['group'])

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

for key in GEN.keys():
    if GEN[key]['source']=='random' and ENV['group']=='random':
        seed=random.sample(range(100000, 999999),GEN[key]['num_instances'])
        # random.sample genera una lista di numeri senza ripetizione; random.choices seleziona elementi da una lista con reinserimento (non è detto che siano tutti diversi)
        for id in seed:
            instance = ll.gen_instance(GEN[key]['m'], GEN[key]['n'], GEN[key]['alphabet'],id)

            instance_str = ll.instance_to_str(instance, format=ENV['instance_format'])

            output_filename = f"instance_{GEN[key]['m']}_{GEN[key]['n']}_{id}.{ENV['instance_format']}"

            fout = open(os.path.join(ENV.OUTPUT_FILES,output_filename),'w')

            print(instance_str, file=fout)
            fout.close()

    elif GEN[key]['source']!='random' and ENV['group']!='random':
        # mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, group_dir)

        #leggo quali file ci sono nella cartella "ENV['group']"
        inst_path=os.listdir(group_dir)

        # scelgo due file random (diversi tra loro)
        file= random.sample(inst_path,GEN[key]['num_instances'])
        # print(file)
        
        # scelgo due seed tra quelli proposti in id:{1,2,3,4,5}
        # seed=random.sample(list(GEN[key]['id']),GEN[key]['num_instances'])
        # print(seed)

        # copio i file nella cartella 'output'
        for instance in file:
            source=os.path.join(group_dir,instance)
            destination=ENV.OUTPUT_FILES
            shutil.copy(source,destination)

      
        # instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['instance_format'])
        # instance = ll.get_instance_from_str(instance_str, format=ENV['instance_format'])
        # output_filename = f"instance_catalogue1_{ENV['instance_id']}.{ENV['instance_format']}"

exit(0)
