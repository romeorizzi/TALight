#!/usr/bin/env python3
from sys import exit
import os.path
import ruamel

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper, get_problem_path_from

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

service_dir_path = os.path.abspath(os.path.dirname(__file__))
print(f'__file__={__file__}')
print(f'service_dir_path={service_dir_path}')

GEN_file = os.path.join(service_dir_path,'services','GEN.yaml')
try:
  with open(GEN_file, 'r') as stream:
    try:
        self.messages_book = ruamel.yaml.safe_load(stream)
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



if ENV['instance_spec'] == 'catalogue1':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES)
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format=ENV['instance_format'])
    instance = ll.get_instance_from_str(instance_str, format=ENV['instance_format'])
    output_filename = f"instance_catalogue1_{ENV['instance_id']}.{ENV['instance_format']}"

else:
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = ll.gen_instance(ENV['m'], ENV['n'], ENV['alphabet'], ENV['seed'])
    instance_str = ll.instance_to_str(instance, format=ENV['instance_format'])
    output_filename = f"instance_{ENV['m']}_{ENV['n']}_{ENV['seed']}.{ENV['instance_format']}"


# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {len(instance[0])} character and the second string of {len(instance[1])} character are:'), "yellow", ["bold"])
    if ENV['display']:
        TAc.print(instance_str, "white", ["bold"])
        if not ENV['instance_spec'] == 'catalogue1':
            TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
if ENV['download']:
    fout = open(os.path.join(ENV.OUTPUT_FILES,output_filename),'w')
    print(instance_str, file=fout)
    fout.close()

exit(0)
