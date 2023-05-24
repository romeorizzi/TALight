#!/usr/bin/env python3
from sys import exit, stderr, stdout
import os
from os import environ

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('problem',str),
    ('service',str),
    ('exclude_services','list_of_str'),
    ('output_on',str),
    ('with_description',bool),
    ('with_evaluator',bool),
    ('with_files',bool),
    ('exclude_arguments','list_of_str'),
    ('with_regex',bool),
    ('with_default',bool),
    ('with_explain',bool),
    ('with_example',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now' if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

try:
    import ruamel.yaml
except Exception as e:
    print(e)
    for out in [stdout, stderr]:
        TAc.print(LANG.render_feedback("ruamel-missing", 'Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package \'ruamel\' on your machine).'), "red", ["bold"], file=out)
        print(LANG.render_feedback("ruamel-required", ' the service \'get_info\' needs to read the .yaml files of the problem in order to provide you with the information required. If \'ruamel\' is not installed in the environment where the \'rtald\' daemon runs, the service \'get_info\' can not perform.'), file=out)
        print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
    exit(1)

path_tokens = os.path.split(environ["TAL_META_DIR"])[:-1]
problem_folder = path_tokens[0]
for token in path_tokens[1:]:
    problem_folder = os.path.join(problem_folder,token)
problem_folder = os.path.join(problem_folder,ENV['problem'])
meta_yaml_file = os.path.join(problem_folder,'meta.yaml')
if not os.path.isdir(problem_folder):
    TAc.print(LANG.render_feedback("problem-folder-missing", f'Error: problem folder not found in the directory currently deployed by the rtald server invocated. I was searching for problem folder: {problem_folder}'), "red", ["bold"])
    exit(1)
if not os.path.exists(meta_yaml_file):
    TAc.print(LANG.render_feedback("metafile-missing", f'Error: problem folder found but it does not contain the required meta.yaml file. I was searching for the file: {meta_yaml_file}'), "red", ["bold"])
    exit(1)
with open(meta_yaml_file, 'r') as stream:
    try:
        meta_yaml_book = ruamel.yaml.safe_load(stream)
    except:
        TAc.print(LANG.render_feedback("metafile-unparsable", f'Error: the file \'{meta_yaml_file}\' could not be loaded as a .yaml file.'), "red", ["bold"], file=out)
        exit(1)

def prune_service_subtree(service_yaml_subtree):
    for voice in ['description','evaluator','files']:
        if not ENV['with_'+voice] and voice in service_yaml_subtree:
            del service_yaml_subtree[voice]
    for arg in ENV['exclude_arguments']:
        if arg in service_yaml_subtree['args']:
            del service_yaml_subtree['args'][arg]
    for arg in service_yaml_subtree['args']:
        if not ENV['with_regex'] and 'regex' in service_yaml_subtree['args'][arg]:
            del service_yaml_subtree['args'][arg]['regex']
        if not ENV['with_default'] and 'default' in service_yaml_subtree['args'][arg]:
            del service_yaml_subtree['args'][arg]['default']
        for voice in ['explain','example','note']:
            if not ENV['with_'+voice]:
                if voice in service_yaml_subtree['args'][arg]:
                    del service_yaml_subtree['args'][arg][voice]
                i = 1
                while voice+str(i) in service_yaml_subtree['args'][arg]:
                    del service_yaml_subtree['args'][arg][voice+str(i)]
                    i += 1
                      
                      
if ENV['service'] == 'all_services':
    del meta_yaml_book['public_folder']
    for service in ENV['exclude_services']:
        if 'service' in meta_yaml_book['services']:
            del meta_yaml_book['services'][service]
    for service in meta_yaml_book['services']:
        prune_service_subtree(meta_yaml_book['services'][service])
else:
    if ENV['service'] in meta_yaml_book['services']:
        meta_yaml_book = meta_yaml_book['services'][ENV['service']]
    else:
        TAc.print(LANG.render_feedback("service-missing", f"Error: the service {ENV['service']} is not among the services of problem {ENV['problem']}."), "red", ["bold"])
        exit(1)
    prune_service_subtree(meta_yaml_book)
    
if ENV['output_on'] == 'stdout':
    print(meta_yaml_book)
else:
    assert ENV['output_on'] == 'file'
    TALf.str2output_file(meta_yaml_book,f'filtered_meta_yaml.txt')
exit(0)
