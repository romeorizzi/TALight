#!/usr/bin/env python3

from sys import stderr, exit, argv
from os import environ
from os.path import join, split

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor.)", file=stderr)

err_ruamel = None
yaml_is_installed = True
try:
    import ruamel.yaml
except Exception as e:
    yaml_is_installed = False
    err_ruamel = e

            
class Env:
    def __init__(self, args_list, problem, service, service_server_fullname):
        self.base_path = environ["TAL_META_DIR"]
        self.exe_path = split(argv[0])[0]
        self.problem = problem
        self.service = service
        self.args_list = args_list
        self.service_server_fullname = service_server_fullname
        self.arg = {}
        for name, val_type in args_list:
            if val_type == str:
                self.arg[name] = environ[f"TAL_{name}"]
            elif val_type == int:
                self.arg[name] = int(environ[f"TAL_{name}"])
            elif val_type == bool:
                self.arg[name] = environ[f"TAL_{name}"] == "1"
            else:
                print(f"# Unrecoverable Error: type {val_type} not yet supported in args list. Used to interpret arg {name}.", file=stderr)
                exit(1)
    def __getitem__(self, key):
        return self.arg.get(key)


class Lang:
    def __init__(self, ENV, TAc, myfeval, book_required=False):
        self.myfeval = myfeval
        self.ENV=ENV
        self.TAc=TAc
        self.messages_book = None
        self.messages_book_file = join(ENV.base_path, ENV.exe_path, ENV.service + "_feedbackBook." + ENV["lang"] + ".yaml")
        if not yaml_is_installed:
            if book_required:
                print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine): the service {ENV.service} you required strongly relies on a .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated.", file=stderr)
                exit(1)
            else:
                print("# Recoverable Error: ", end="", file=stderr)
                print(err_ruamel, file=stderr)
                print("# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue (as long as you can understand the little needed English).\n# (To enjoy a feedback in a supported language install the python package 'ruamel'. The languages supported by a problem service appear as the options for the lang parameter listed by the command `rtal list`)", file=stderr)
        else:
            try:
              with open(self.messages_book_file, 'r') as stream:
                try:
                    yaml_book = ruamel.yaml.safe_load(stream)
                    self.messages_book = yaml_book
                except yaml.YAMLError as exc:
                    if book_required:
                        print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine): the messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file). The service {ENV.service} you required for problem {ENV.problem} strictly requires this .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated.", file=stderr)
                        print(exc, file=stderr)
                        exit(1)
                    else:
                        print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file)\n# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
                        print(exc, file=stderr)
            except IOError as ioe:
                if book_required:
                    print(f"Internal error (please, report it to those responsible): The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.\n The service {ENV.service} you required for problem {ENV.problem} strictly requires to have access to this .yaml file.", file=stderr)
                    print(ioe, file=stderr)
                    exit(1)
                else:
                    print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.\n# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
                    print(ioe, file=stderr)
        self.opening_msg = self.render_feedback("open-channel",f"# I will serve: problem={ENV.problem}, service={ENV.service}")
        for arg_name, _ in ENV.args_list:
            arg_val = ENV[arg_name]
            self.opening_msg += f", {arg_name}={arg_val}"
        if self.messages_book == None:
            self.opening_msg += f".\n# The feedback_source is code of the service server ({ENV.service_server_fullname})"
        else:
            self.opening_msg += f".\n# The feedback_source is the dictionary of phrases yaml file ({self.messages_book_file}) in the service server folder."
        TAc.print(self.opening_msg, "yellow", ["underline"], file=stderr)


    def render_feedback(self, msg_code, msg_English_rendition):
        if self.messages_book == None:
            return msg_English_rendition
        return self.myfeval(self.messages_book[msg_code])



class TALcolors:
    def __init__(self, ENV):
        self.numNO = 0
        self.numOK = 0
        self.colored_print = ENV["ISATTY"] and termcolor_is_installed

    def print(self, msg_text, *msg_rendering, **kwargs):
      if type(msg_rendering[-1]) == list:
          msg_style = msg_rendering[-1]
          msg_colors = msg_rendering[:-1]
      else:
          msg_style = []
          msg_colors = msg_rendering
      if self.colored_print:
          print(colored(msg_text, *msg_colors, attrs=msg_style), **kwargs)
      else:
          print(msg_text, **kwargs)

    def NO(self):
        self.numNO += 1
        self.print("No! ", "red", ["blink", "bold"], end="")

    def OK(self):
        self.numOK += 1
        self.print("OK! ", "green", ["bold"], end="")

    def GotBored(self):
        self.print("! (I got bored)", "white")

    def Finished(self):
        self.print(f"! (We have finished) Correct answers: {self.numOK}/{self.numOK+self.numNO}", "white")
