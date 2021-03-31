#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
from os import environ

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
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), book_required=False)
TAc.print(LANG.opening_msg, "green")

try:
    import ruamel.yaml
except Exception as e:
    print(e)
    for out in [stdout, stderr]:
        TAc.print(LANG.render_feedback("ruamel-missing", "Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine))."), "red", ["bold"], file=out)
        print(LANG.render_feedback("ruamel-required", " the service 'synopsis' needs to access .yaml files in order to provide you with the information required. As long as 'ruamel' is not installed in the environment where the 'rtald' daemon runs, the service 'synopsis' can not perform."), file=out)
        print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
    exit(1)

meta_yaml_file = environ['TAL_META_DIR'] + "/meta.yaml"
try:
  with open(meta_yaml_file, 'r') as stream:
    try:
        meta_yaml_book = ruamel.yaml.safe_load(stream)
    except:
        for out in [stdout, stderr]:
            TAc.print(LANG.render_feedback("metafile-unparsable", f'Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, signal it to the problem maker): The meta.yaml file "{meta_yaml_file}" could not be loaded as a .yaml file.'), "red", ["bold"], file=out)
            print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
        exit(1)
except IOError as ioe:
    for out in [stdout, stderr]:
        TAc.print(LANG.render_feedback("metafile-missing", f'Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, signal it to the problem maker): The meta.yaml file of the problem {problem} could not be accessed for the required information. The file should have been: {meta_yaml_file}'), "red", ["bold"], file=out)
        print(LANG.render_feedback("operation-necessary", ' This operation is necessary. The synopsis service aborts and drops the channel.'), file=out)
        print(ioe, file=out)
    exit(1)

if ENV['service'] not in meta_yaml_book['services'].keys():
    TAc.print(LANG.render_feedback("wrong-service-name", f'\nSorry, you asked information about {ENV["service"]} which however does not appear among the services currently supported for the problem {problem}.'), "red", ["bold"])
    TAc.print("\n\nList of all Services:", "red", ["bold", "underline"], end="  ")
    print(", ".join(meta_yaml_book['services'].keys()),end="\n\n")
    exit(0)

TAc.print("\n"+ENV['service'], "yellow", ["bold"], end="")
TAc.print(LANG.render_feedback("service-of", f'   (service of the {problem} problem)'), "yellow")

if "explain" in meta_yaml_book['services'][ENV['service']].keys():
    TAc.print("\nDescription:", "green", ["bold"])
    print("   "+eval(f"f'{str(meta_yaml_book['services'][ENV['service']]['explain'])}'"))
if len(meta_yaml_book['services'][ENV['service']]['args']) > 0:
    TAc.print(LANG.render_feedback("the-num-arguments", f'\nThe {len(meta_yaml_book["services"][ENV["service"]]["args"])} arguments of service {ENV["service"]}:'), "green", ["bold"])
    for a,i in zip(meta_yaml_book['services'][ENV['service']]['args'],range(1,1+len(meta_yaml_book['services'][ENV['service']]['args']))):
        TAc.print(str(i)+". ", "white", ["bold"], end="")
        TAc.print(a, "yellow", ["bold"])
        TAc.print("   regex: ", ["bold"], end="")
        print(meta_yaml_book['services'][ENV['service']]['args'][a]['regex'])
        if "explain" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print("   Explanation: ", ["bold"], end="")
            print(eval(f"f'{str(meta_yaml_book['services'][ENV['service']]['args'][a]['explain'])}'"))
        if "example" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print("   Example: ", ["bold"], end="")
            print(eval(f"f'{str(meta_yaml_book['services'][ENV['service']]['args'][a]['example'])}'"))
        if "default" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print("   Default Value: ", ["bold"], end="")
            print(str(meta_yaml_book['services'][ENV['service']]['args'][a]['default']))
        else:
            TAc.print(f"   The argument {a} is mandatory.", ["bold"])

print(LANG.render_feedback("regex-cloud-resource", f"\nAll arguments of all TALight services take in only strings as possible values. As you can see, the family of string values allowed for an argument is described by means of a regex. We refer to the online service 'https://extendsclass.com/regex-tester.html' if in need of help in grasping the intended meaning of the regex.\n"))

# Now printing the footing lines:
if "help" in meta_yaml_book['services'].keys():
    TAc.print(LANG.render_feedback("index-help-pages", 'Index of the Help Pages:'), "red", ["bold", "underline"], end="  ")
    print(meta_yaml_book['services']['help']['args']['page']['regex'][2:-2])
TAc.print(LANG.render_feedback("list-services", 'List of all Services:'), "red", ["bold", "underline"], end="  ")
for s in meta_yaml_book['services'].keys():
    print(TAc.colored(s, "yellow", ["bold"]), end=",  ")
print(",  ".join(TAc.colored(_, "yellow", ["bold"]) for _ in meta_yaml_book['services'].keys()))
    
exit(0)




