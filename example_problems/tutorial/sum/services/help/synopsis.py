#!/usr/bin/env python3
from sys import stderr, exit, argv
from os import environ

try:
    import ruamel.yaml
except Exception as e:
    print(e)
    print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine): the problem service 'synopsis' needs to access the 'meta.yaml' file in order to provide you with the information required. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated. I close the channel.", file=stderr)
    exit(1)

problem=environ["TAL_META_DIR"].split("/")[-1]
service="synopsis"
args_list = [
    ('service',str),
    ('ISATTY',bool),
]

from multilanguage import Env, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
TAc.print("Synopsis for the use of the service {service} of the problem {problem}:", "green")

print(f"Env.meta_dir={Env.meta_dir}")
exit(0)

try:
  with open(self.messages_book_file, 'r') as stream:
    try:
        yaml_book = ruamel.yaml.safe_load(stream)
        self.messages_book = yaml_book
    except yaml.YAMLError as exc:
        if book_required:
            for out in [stdout, stderr]:
                print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine): the messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file). The service {ENV.service} you required for problem {ENV.problem} strictly requires this .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated.", file=out)
                print(exc, file=out)
            exit(1)
        else:
            print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file).", file=stderr)
            print(exc, file=stderr)
            print(f"# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
except IOError as ioe:
    if book_required:
        for out in [stdout, stderr]:
            print(f"Internal error (please, report it to those responsible): The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.\n The service {ENV.service} you required for problem {ENV.problem} strictly requires to have access to this .yaml file.", file=out)
            print(ioe, file=out)
        exit(1)
    else:
        print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.", file=stderr)
        print(ioe, file=stderr)
        print(f"# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)


print()

exit(0)
