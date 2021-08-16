#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
from os import environ
import os.path

from multilanguage import Env, Lang, TALcolors

problem=environ["TAL_META_DIR"].split("/")[-1]
service="synopsis"
args_list = [
    ('lang',str),
    ('service',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

def load_meta_yaml_file(meta_yaml_file, succeed_or_die):
    try:
        import ruamel.yaml
    except Exception as e:
        print(e)
        for out in [stdout, stderr]:
            TAc.print(LANG.render_feedback("ruamel-missing", 'Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package \'ruamel\' on your machine).'), "red", ["bold"], file=out)
            print(LANG.render_feedback("ruamel-required", ' the service \'synopsis\' needs to read the .yaml files of the problem in order to provide you with the information required. If \'ruamel\' is not installed in the environment where the \'rtald\' daemon runs, the service \'synopsis\' can not perform.'), file=out)
            print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
        exit(1)
    environ["TAL_META_DIR"] + "/meta.yaml"
    try:
      with open(meta_yaml_file, 'r') as stream:
        try:
            meta_yaml_book = ruamel.yaml.safe_load(stream)
        except:
            for out in [stdout, stderr]:
                TAc.print(LANG.render_feedback("metafile-unparsable", f'Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, signal it to the problem maker unless you have altered the file yourself): The file \'{meta_yaml_file}\' could not be loaded as a .yaml file.', {'problem':problem,'meta_yaml_file':meta_yaml_file}), "red", ["bold"], file=out)
            if succeed_or_die:
                print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
                exit(1)
            else:
                print(LANG.render_feedback("operation-not-necessary", ' We overcome this problem by resorting on the information hardcoded within the meta.yaml file of the problem. Hope that getting this updated information in English is good enough for you.'), file=out)
                return None
    except IOError as ioe:
        for out in [stdout, stderr]:
            TAc.print(LANG.render_feedback("metafile-missing", f'Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, signal it to the problem maker unless you have altered the file yourself): The required yaml file of problem "{problem}" could not be accessed for the required information. File not found: \'{meta_yaml_file}\'', {'problem':problem,'meta_yaml_file':meta_yaml_file}), "red", ["bold"], file=out)
            print(ioe, file=out)
        if succeed_or_die:
            print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
            exit(1)
        else:
            print(LANG.render_feedback("operation-not-necessary", ' We overcome this problem by resorting on the information hardcoded within the meta.yaml file of the problem. Hope that getting this updated information in English is good enough for you.'), file=out)
            return None
    return meta_yaml_book


meta_yaml_book = None
if environ["TAL_lang"] != "hardcoded":
    meta_yaml_book = load_meta_yaml_file(meta_yaml_file=os.path.join(environ["TAL_META_DIR"],"lang",environ["TAL_lang"],"meta","meta_"+ENV["service"]+"_"+environ["TAL_lang"]+".yaml"), succeed_or_die = False)
if meta_yaml_book == None:
    meta_yaml_book = load_meta_yaml_file(meta_yaml_file=os.path.join(environ["TAL_META_DIR"],"meta.yaml"), succeed_or_die = True)
    
if ENV['service'] not in meta_yaml_book['services'].keys():
    TAc.print(LANG.render_feedback("wrong-service-name", f'\nSorry, you asked information about {ENV["service"]} which however does not appear among the services currently supported for problem "{problem}".'), "red", ["bold"])
    TAc.print('\n\nList of all Services:', "red", ["bold", "underline"], end="  ")
    print(", ".join(meta_yaml_book['services'].keys()),end="\n\n")
    exit(0)

TAc.print("\n"+ENV['service'], "yellow", ["bold"], end="")
TAc.print(LANG.render_feedback("service-of", f'   (service of the "{problem}" problem)'), "yellow")

if "description" in meta_yaml_book['services'][ENV['service']].keys():
    TAc.print('\nDescription:', "green", ["bold"])
    for line in meta_yaml_book['services'][ENV['service']]['description'].split('\n'):
        print("   "+eval(f"f'{line}'"))
if "example" in meta_yaml_book['services'][ENV['service']].keys():
    TAc.print('   Example: ', ["bold"], end="")
    print(eval(f"f'{meta_yaml_book['services'][ENV['service']]['example']}'"))
    i = 1
    while ("example"+str(i)) in meta_yaml_book['services'][ENV['service']].keys():
      print(" "*6, end="")
      print(eval(f"f'{meta_yaml_book['services'][ENV['service']]['example'+str(i)]}'"))
      i += 1
if len(meta_yaml_book['services'][ENV['service']]['args']) > 0:
    TAc.print(LANG.render_feedback("the-num-arguments", f'\nThe service {ENV["service"]} has {len(meta_yaml_book["services"][ENV["service"]]["args"])} arguments:'), "green", ["bold"])
    for a,i in zip(meta_yaml_book['services'][ENV['service']]['args'],range(1,1+len(meta_yaml_book['services'][ENV['service']]['args']))):
        TAc.print(str(i)+". ", "white", ["bold"], end="")
        TAc.print(a, "yellow", ["bold"])
        TAc.print('   regex: ', ["bold"], end="")
        print(meta_yaml_book['services'][ENV['service']]['args'][a]['regex'])
        if "explain" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print('   Explanation: ', ["bold"], end="")
            print(eval(f"f'{meta_yaml_book['services'][ENV['service']]['args'][a]['explain']}'"))
            i = 1
            while ("explain"+str(i)) in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
              print(" "*6, end="")
              print(eval(f"f'{meta_yaml_book['services'][ENV['service']]['args'][a]['explain'+str(i)]}'"))
              i += 1
        if "example" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print('   Example: ', ["bold"], end="")
            print(eval(f"f'{meta_yaml_book['services'][ENV['service']]['args'][a]['example']}'"))
            i = 1
            while ("example"+str(i)) in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
              print(" "*6, end="")
              print(eval(f"f'{meta_yaml_book['services'][ENV['service']]['args'][a]['example'+str(i)]}'"))
              i += 1
        if "default" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print('   Default Value: ', ["bold"], end="")
            print(meta_yaml_book['services'][ENV['service']]['args'][a]['default'])
        else:
            TAc.print(f'   The argument {a} is mandatory.', ["bold"])

print(LANG.render_feedback("regex-cloud-resource", '\nThe arguments of all TALight services take in as possible values only simple strings that can be streamed from the \'rtal\' client to the \'rtald\' daemon (and finally acquired as environment variables). For each argument, the family of allowed string values is described by means of a regex. If the correct interpretation of the regex confuses you, then take profit of the online support at \'https://extendsclass.com/regex-tester.html\'.\n'))

# Now printing the footing lines:
if "help" in meta_yaml_book['services'].keys():
    TAc.print(LANG.render_feedback("index-help-pages", 'Index of the Help Pages:'), "red", ["bold", "underline"], end="  ")
    print(meta_yaml_book['services']['help']['args']['page']['regex'][2:-2])
TAc.print(LANG.render_feedback("list-services", f'List of all services for problem "{problem}":'), "red", ["bold", "underline"], end="  ")
print(",  ".join(TAc.colored(_, "yellow", ["bold"]) for _ in meta_yaml_book['services'].keys()))
    
exit(0)




