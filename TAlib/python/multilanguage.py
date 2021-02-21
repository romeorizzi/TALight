#!/usr/bin/env python3

from sys import stderr, exit
from os import environ
from pathlib import Path

yaml_is_installed = True
try:
    import yaml
except Exception as e:
    yaml_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.\n# (To enjoy a feedback in a supported language install the python package yaml. The languages supported by a problem service appear as the options for the lang parameter listed by the command `rtal list`)", file=stderr)

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor.)", file=stderr)


class Env:
    def __init__(self, args_list, problem, service, service_server_fullname):
        self.problem = problem
        self.service = service
        self.args_list = args_list
        #self.args = { key : val for key, val in args_list }
        self.service_server_fullname = service_server_fullname
        for name, val_type in args_list:
            if val_type == str:
                exec(f'self.{name} = environ["TAL_{name}"]')
            elif val_type == int:
                exec(f'self.{name} = int(environ["TAL_{name}"])')
            elif val_type == bool:
                exec(f'self.{name} = (environ["TAL_{name}"] == "1")')
            else:
                print(f"# Unrecoverable Error: type {val_type} not yet supported in args list. Used to interpret arg {name}.", file=stderr)
                exit(1)

class Lang:
    def __init__(self, ENV, myfeval):
        self.myfeval = myfeval
        self.messages_book = None
        self.service_name = Path(ENV.service_server_fullname).stem
        self.messages_book_file = self.service_name + "." + ENV.lang + ".yaml"
        if yaml_is_installed:
            try:
              with open(self.messages_book_file, 'r') as stream:
                try:
                    yaml_book = yaml.safe_load(stream)
                    self.messages_book = yaml_book
                except yaml.YAMLError as exc:
                    print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file)\n# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
                    print(exc, file=stderr)
            except IOError as ioe:
                print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.\n# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
                print(ioe, file=stderr)
        self.opening_msg = self.render_feedback("open-channel",f"# I will serve: problem={ENV.problem}, service={ENV.service}")
        for arg_name, _ in ENV.args_list:
            arg_val = eval(f"ENV.{arg_name}")
            self.opening_msg += f", {arg_name}={arg_val}"
        if self.messages_book == None:
            self.opening_msg += f".\n# The feedback_source is code of the service server ({service_server_fullname})"
        else:
            self.opening_msg += f".\n# The feedback_source is the dictionary of phrases yaml file ({self.messages_book_file}) in the service server folder."   


    def render_feedback(self, msg_code, msg_English_rendition):
        if self.messages_book == None:
            return msg_English_rendition
        return self.myfeval(self.messages_book[msg_code])


                
class TALcolors:                
    def __init__(self, ENV):
        self.colored_print = ENV.ISATTY and termcolor_is_installed
        self.numNO = 0
        self.numOK = 0

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
        self.print(f"! (We have finished) Correct answers: {numOK}/{numOK+numNO}", "white")

