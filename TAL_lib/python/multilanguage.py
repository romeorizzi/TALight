#!/usr/bin/env python3

from sys import stdout, stderr, exit, argv
from os import environ
from os.path import join, split

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor on your local machine.)", file=stderr)

err_ruamel = None
yaml_is_installed = True
try:
    import ruamel.yaml
except Exception as e:
    yaml_is_installed = False
    err_ruamel = e

            
class Env:
    def __init__(self, problem, service, args_list):
        self.exe_path = split(argv[0])[0]
        self.META_DIR = environ["TAL_META_DIR"]
        self.problem = problem
        self.service = service
        self.args_list = args_list
        self.arg = {}
        for name, val_type in args_list:
            if not f"TAL_{name}" in environ:
                for out in [stdout, stderr]:
                    print(f"# Unrecoverable Error: the environment variable TAL_{name} for the argument {name} has not been set. Check out if this argument is indeed present in the meta.yaml file of the problem for this service {service}. If not, consider adding it to the meta.yaml file or removing it from the service server code.", file=out)
                exit(1)                
            if val_type == str:
                self.arg[name] = environ[f"TAL_{name}"]
            elif val_type == bool:
                self.arg[name] = (environ[f"TAL_{name}"] == "1")
            elif val_type == int:
                self.arg[name] = int(environ[f"TAL_{name}"])
            elif val_type == float:
                self.arg[name] = float(environ[f"TAL_{name}"])
            else:
                for out in [stdout, stderr]:
                    print(f"# Unrecoverable Error: type {val_type} not yet supported in args list (the set of supported types can be extended by communities of problem makers adding further elif clauses here above). Used to interpret arg {name}.", file=out)
                exit(1)
    def __getitem__(self, key):
        return self.arg.get(key)


class Lang:
    def __init__(self, ENV, TAc, service_server_eval, book_strictly_required=False):
        self.service_server_eval = service_server_eval
        self.ENV=ENV
        self.TAc=TAc
        self.messages_book = None
        self.messages_book_file = None
        self.to_be_printed_opening_msg = True
        if "lang" in ENV.arg.keys() and ENV["lang"] != "hardcoded":
            self.messages_book_file = join(ENV.META_DIR, "lang", ENV["lang"], ENV.service + "_feedbackBook." + ENV["lang"] + ".yaml")
            # BEGIN: try to load the message book
            if not yaml_is_installed:
                if book_strictly_required:
                    for out in [stdout, stderr]:
                        TAc.print("Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine):", "red", ["bold"])
                        print(f" the service {ENV.service} you required strongly relies on a .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated. I close the channel.", file=out)
                    exit(1)
                else:
                    TAc.print("# Recoverable Error: ", "red", ["bold"], end="", file=stderr)
                    print(err_ruamel, file=stderr)
                    print("# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue (as long as you can understand the little needed English).\n# (To enjoy a feedback in a supported language install the python package 'ruamel'. The languages supported by a problem service appear as the options for the lang parameter listed by the command `rtal list`)", file=stderr)
            else:
                try:
                  with open(self.messages_book_file, 'r') as stream:
                    try:
                        self.messages_book = ruamel.yaml.safe_load(stream)
                    except BaseException as exc:
                        if book_strictly_required:
                            for out in [stdout, stderr]:
                                TAc.print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted; otherwise, install the python package 'ruamel' on your machine):", "red", ["bold"])
                                TAc.print(f" the messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file).", "red", ["bold"])
                                print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires this .yaml file. As long as the 'ruamel' package is not installed in the environment where the 'rtald' daemon runs, this service can not be operated.", file=out)
                                print(exc, file=out)
                            exit(1)
                        else:
                            TAc.print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file).", "red", ["bold"], file=stderr)
                            #print(exc, file=stderr)
                            print(f"# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
                except IOError as ioe:
                    if book_strictly_required:
                        for out in [stdout, stderr]:
                            TAc.print(f"Internal error (please, report it to those responsible): The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.", "red", ["bold"])
                            print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires to have access to this .yaml file.", file=out)
                            print(ioe, file=out)
                        exit(1)
                    else:
                        TAc.print(f"# Recoverable Error: The messages_book file `{self.messages_book_file}` for multilingual feedback could not be accessed.", "red", ["bold"], file=stderr)
                        print(ioe, file=stderr)
                        print(f"# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
        #END:  try_to_load_the_message_book():
        
    def print_opening_msg(self):
        self.to_be_printed_opening_msg = False
        self.opening_msg = self.render_feedback("open-channel",f"# I will serve: problem={self.ENV.problem}, service={self.ENV.service}\n#  with arguments: ")
        for arg_name, arg_type in self.ENV.args_list:
            arg_val = self.ENV[arg_name]
            if arg_type == bool:
                self.opening_msg += f"{arg_name}={'1' if arg_val else '0'} (i.e., {arg_val}), "
            else:
                self.opening_msg += f"{arg_name}={arg_val}, "
        self.opening_msg = self.opening_msg[:-2] + ".\n"
        if self.messages_book == None:
            self.opening_msg += f"# The feedback_source is the one hardcoded in the service server ({argv[0]})"
        else:
            self.opening_msg += self.render_feedback("feedback_source",f".\n# The feedback_source is the dictionary of phrases yaml file ({self.messages_book_file}) in the service server folder.", {"problem":self.ENV.problem, "service":self.ENV.service, "messages_book_file":self.messages_book_file})
        self.TAc.print(self.opening_msg, "green")

    def render_feedback(self, msg_code, rendition_of_the_hardcoded_msg, trans_dictionay=None):
        """If a message_book is open and contains a rule for <msg_code>, then return the server evaluation of the production of that rule. Otherwise, return the rendition of the harcoded message received with parameter <rendition_of_the_hardcoded_msg>"""
        if self.to_be_printed_opening_msg:
            self.print_opening_msg()
        if self.messages_book != None and msg_code not in self.messages_book:
            self.TAc.print(f"Warning to the problem maker: the msg_code={msg_code} is not present in the selected messages_book","red", file=stderr)
        if self.messages_book == None or msg_code not in self.messages_book:
            return rendition_of_the_hardcoded_msg
        if trans_dictionay != None:
            return self.messages_book[msg_code].format(**trans_dictionay)
        msg_encoded = self.messages_book[msg_code]
        return self.service_server_eval(msg_encoded)
    
    def suppress_opening_msg(self):
        self.to_be_printed_opening_msg = False


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

    def colored(self, msg_text, *msg_rendering):
      if type(msg_rendering[-1]) == list:
          msg_style = msg_rendering[-1]
          msg_colors = msg_rendering[:-1]
      else:
          msg_style = []
          msg_colors = msg_rendering
      if self.colored_print:
          return colored(msg_text, *msg_colors, attrs=msg_style)
      else:
          return msg_text
          
                
    def NO(self):
        self.numNO += 1
        self.print("# ", "yellow", end="")
        self.print("No! ", "red", ["blink", "bold"], end="")

    def OK(self):
        self.numOK += 1
        self.print("# ", "yellow", end="")
        self.print("OK! ", "green", ["bold"], end="")

    def GotBored(self):
        self.print("# I got bored (too much load on the server)", "white")

    def Finished(self):
        self.print(f"# WE HAVE FINISHED\n#    Correct answers: {self.numOK}/{self.numOK+self.numNO}", "white")
