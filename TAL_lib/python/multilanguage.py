#!/usr/bin/env python3

from sys import stdout, stderr, exit, argv
from os import environ, path
import random

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
    def __getitem__(self, key):
        return self.arg.get(key)
    def __init__(self, args_list):
        self.arg = {}
        args_list.append(("META_TTY",bool))
        if "TAL_lang" in environ:
            args_list.append(("lang",str))
        if "TAL_seed" in environ:
            args_list.append(("seed",int))
            self.seed_generated = False
            if environ["TAL_seed"] in {"random_seed", "000000"}:
                self.arg["seed"] = random.randint(100100,999999)
                self.seed_generated = True 
            else:
                self.arg["seed"] = int(environ["TAL_seed"])
        self.args_list = args_list

        self.exe_fullname = argv[0]
        self.exe_path_from_META_DIR = path.split(self.exe_fullname)[0]
        self.exe_name = path.split(self.exe_fullname)[-1]
        self.META_DIR = environ["TAL_META_DIR"]
        self.CODENAME = environ["TAL_META_CODENAME"]
        self.service = environ["TAL_META_SERVICE"]
        self.problem = path.split(environ["TAL_META_DIR"])[-1]
        assert(self.problem == self.CODENAME)
        
        for name, val_type in args_list:
            if not f"TAL_{name}" in environ:
                for out in [stdout, stderr]:
                    print(f"# Unrecoverable Error: the environment variable TAL_{name} for the argument {name} has not been set. Check out if this argument is indeed present in the meta.yaml file of the problem for this service {self.service}. If not, consider adding it to the meta.yaml file or removing it from the service server code.", file=out)
                exit(1)
            if name == "seed":
                continue
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
                

class Lang:
    def __init__(self, ENV, TAc, service_server_eval, book_strictly_required=False):
        self.service_server_eval = service_server_eval
        self.ENV=ENV
        self.TAc=TAc
        self.to_be_printed_opening_msg = True

        # BEGIN: MESSAGE BOOK LOADING (try to load the message book)
        self.messages_book = None
        self.messages_book_file = None
        if "lang" in ENV.arg.keys() and ENV["lang"] != "hardcoded":
            self.messages_book_file = path.join(ENV.META_DIR, "lang", ENV["lang"], ENV.service + "_feedbackBook." + ENV["lang"] + ".yaml")
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
        # END: MESSAGE BOOK LOADING        
        
    def print_opening_msg(self):
        self.to_be_printed_opening_msg = False
        problem=self.ENV.problem
        service=self.ENV.service
        self.opening_msg = self.render_feedback("open-channel",f"# I will serve: problem={problem}, service={service}\n#  with arguments: ", {"problem":problem, "service":service})
        for arg_name, arg_type in self.ENV.args_list:
            arg_val = self.ENV[arg_name]
            if arg_type == bool:
                self.opening_msg += f"{arg_name}={'1' if arg_val else '0'} (i.e., {arg_val}), "
            elif arg_name=="seed" and self.ENV.seed_generated:
                self.opening_msg += f"{arg_name}={arg_val} (randomly generated, as 'random_seed' was passed), "
            else:
                self.opening_msg += f"{arg_name}={arg_val}, "
        self.opening_msg = self.opening_msg[:-2] + ".\n"
        self.opening_msg += self.render_feedback("feedback_source",f'# The phrases used in this call of the service are the ones hardcoded in the service server (file {self.ENV.exe_fullname}).', {"problem":problem, "service":service, "lang":self.ENV["lang"]})
        self.TAc.print(self.opening_msg, "green")

    def render_feedback(self, msg_code, rendition_of_the_hardcoded_msg, trans_dictionary=None, obj=None):
        """If a message_book is open and contains a rule for <msg_code>, then return the server evaluation of the production of that rule. Otherwise, return the rendition of the hardcoded message received with parameter <rendition_of_the_hardcoded_msg>"""
        #print("render_feedback has received msg_code="+msg_code+"\nrendition_of_the_hardcoded_msg="+rendition_of_the_hardcoded_msg+"\ntrans_dictionary=",end="")
        #print(trans_dictionary)
        if self.to_be_printed_opening_msg:
            self.print_opening_msg()
        if self.messages_book != None and msg_code not in self.messages_book:
            self.TAc.print(f"Warning to the problem maker: the msg_code={msg_code} is not present in the selected messages_book. We overcome this inconvenience by using the hardcoded phrase which follows next.","red", file=stderr)
        if self.messages_book == None or msg_code not in self.messages_book:
            return rendition_of_the_hardcoded_msg
        if trans_dictionary != None:
            #print(self.messages_book[msg_code])
            #print(f"trans_dictionary={trans_dictionary}")
            fstring=self.messages_book[msg_code].format_map(trans_dictionary)
            return eval(f"f'{fstring}'")
        if obj != None:
            fstring=self.messages_book[msg_code].format(obj)
            return eval(f"f'{fstring}'")
        msg_encoded = self.messages_book[msg_code]
        return self.service_server_eval(msg_encoded)
    
    def suppress_opening_msg(self):
        self.to_be_printed_opening_msg = False


class TALcolors:
    def __init__(self, ENV):
        self.numNO = 0
        self.numOK = 0
        self.colored_print = ENV["META_TTY"] and termcolor_is_installed

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
