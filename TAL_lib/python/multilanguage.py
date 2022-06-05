#!/usr/bin/env python3

import sys
from sys import stdout, stderr, exit
from importlib import import_module
from os import environ, path
import random

err_ruamel = None
yaml_is_installed = True
try:
    import ruamel.yaml
except Exception as e:
    yaml_is_installed = False
    err_ruamel = e

class TALcolors:
    def __init__(self, ENV, color_implementation ="ANSI"):
        if color_implementation=="None":
           self.color_implementation = None
        else:
            if environ["TAL_META_TTY"]=='1' or color_implementation=="html":
                try:
                    self.termcolor = import_module('termcolor')
                except Exception as e:
                    self.color_implementation = None
                    for out in ['stderr','stdout']:
                        print(f"# Recoverable Error: {e}", file=out)
                        print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor on the machine where rtald is running.)", file=out)
                    return
            if 'termcolor' in sys.modules:
                if color_implementation=="ANSI":
                    self.color_implementation = 'ANSI'
                elif color_implementation=="html":
                    self.color_implementation = 'html'
                    try:
                        from ansi2html import Ansi2HTMLConverter
                        self.ansi2html = Ansi2HTMLConverter(inline = True)
                    except Exception as e:
                        self.color_implementation = None
                        for out in ['stderr','stdout']:
                            print(f"# Recoverable Error: {e}", file=out)
                            print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package ansi2html on the machine where rtald is running.)", file=out)
                else:
                    print(f"# Unrecoverable Error: no implementation is currently offered for managing colors as {color_implementation}.)", file=stderr)
                    exit(0)

        self.numNO = 0
        self.numOK = 0
        self.goals = {}

    def colored(self, msg_text, *msg_rendering):
        if self.color_implementation == None:
            return msg_text
        if len(msg_rendering) == 0:
            ANSI_msg = msg_text
        else:
            if type(msg_rendering[-1]) == list:
                msg_style = msg_rendering[-1]
                msg_colors = msg_rendering[:-1]
            else:
                msg_style = []
                msg_colors = msg_rendering
            ANSI_msg = self.termcolor.colored(msg_text, *msg_colors, attrs=msg_style)
        if self.color_implementation == 'ANSI':
            colored_msg = ANSI_msg
        elif self.color_implementation == 'html':
            colored_msg = self.ansi2html.convert(ANSI_msg.replace(">", "&gt;").replace("<", "&lt;"), full=False).replace("\n", "\n<br/>")
        else:
            assert self.color_implementation == None
        return colored_msg

    def print(self, msg_text, *msg_rendering, **kwargs):
        print(self.colored(msg_text, *msg_rendering), **kwargs)
          
                
# The following last methods should next be moved to the TAL_lib bot_lib.py
# At the same time, the part concerning accountings on the correct/out-of-time/non correct answers of an evaluated bot (usually in a service eval_*) has been expanded whithin the library TAL_DAGs, taking as example:
#   triangle/services/eval_feasible_solution_server.py
    def NO(self, goal = None):
        if goal == None:
            self.numNO += 1
        else:
            if goal not in self.goals:
                self.goals[goal] = {'numNo': 1, 'numOK': 0}
            else:
                self.goals[goal]['numNo'] += 1
        self.print("# ", "yellow", end="")
        self.print("No! ", "red", ["bold"], end="")

    def OK(self, goal = None):
        if goal == None:
            self.numOK += 1
        else:
            if goal not in self.goals:
                self.goals[goal] = {'numNo': 0, 'numOK': 1}
            else:
                self.goals[goal]['numOK'] += 1
        self.print("# ", "yellow", end="")
        self.print("OK! ", "green", ["bold"], end="")

    def GotBored(self):
        self.print("# I got bored (too much load on the server)", "white")

    def Finished(self,only_term_signal=False):
        if not only_term_signal:
            self.print(f"\n# SUMMARY OF RESULTS\n#    Correct answers: {self.numOK}/{self.numOK+self.numNO}", "white")
        self.print(f"\n# WE HAVE FINISHED", "white")

    def stop_bot(self):
        self.print(f"\n# WE HAVE FINISHED", "white")

    def stop_bot_and_exit(self):
        self.print(f"\n# WE HAVE FINISHED", "white")
        exit(0)

        
def enforce_type_of_yaml_var(yaml_var, typestr, varname, original_typestr=None):
    """When calling this recursive function from the outside, leave the argument original_typestr to its defaul value of None"""
    #print(f"{varname=}, {yaml_var=}, {type(yaml_var)=}, {original_typestr=}", file=stderr)
    if original_typestr is None:
        original_typestr = typestr
        varname = f"{varname} was meant to be of type {typestr}. Now, {typestr}"
    if typestr in ['yaml','str',str]:
        return yaml_var
    if typestr in ['int',int]:
        try:
            return int(yaml_var)
        except:
            print(f"# Unrecoverable Error: {varname} is not of type int. Here is its actual raw content as a string: {repr(yaml_var)}")
            exit(0)
    if typestr in ['bool',bool]:
        try:
            yaml_var = int(yaml_var)
            return bool(yaml_var)
        except:
            print(f"# Unrecoverable Error: {varname} is not of type bool. Here is its actual raw content as a string: {repr(yaml_var)}")
            exit(0)
    if typestr[:len('matrix_of_')] == 'matrix_of_':
        typestr = 'list_of_list_of_'+typestr[len('matrix_of_'):]
    if typestr[:len('list_of_')] == 'list_of_':
        if type(yaml_var) != list:
            print(f"# Unrecoverable Error: {varname} is not a 'list_of_' something. Here is its actual raw content as a string: {repr(yaml_var)}")
            exit(0)
        enforced_list = []
        for item, i in zip(yaml_var,range(1,1+len(yaml_var))):
            enforced_list.append(enforce_type_of_yaml_var(yaml_var=item,typestr=typestr[len('list_of_'):], varname=varname + f" is indeed a list. Its {i}-th item", original_typestr=original_typestr))
        return enforced_list
    else:
        print(f"I can not parse the typestring {typestr}")
        assert False
    
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
        self.exe_fullname = sys.argv[0]
        self.exe_path_from_META_DIR = path.split(self.exe_fullname)[0]
        self.exe_name = path.split(self.exe_fullname)[-1]
        self.META_DIR = environ["TAL_META_DIR"]
        self.CODENAME = environ["TAL_META_CODENAME"]
        self.OUTPUT_FILES = environ["TAL_META_OUTPUT_FILES"]
        self.INPUT_FILES = environ["TAL_META_INPUT_FILES"]
        self.LOG_FILES = environ.get("TAL_META_LOG_FILES")
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
            elif val_type == 'yaml' or val_type[:len('list_of_')] == 'list_of_' or val_type[:len('matrix_of_')] == 'matrix_of_':
                try:
                    self.arg[name] = ruamel.yaml.safe_load(environ[f"TAL_{name}"])
                except Exception as e:
                    print(f'# Unrecoverable Error: error when parsing the service argument `{name}` as a {val_type}. On the next line is the row string content of the environment variable TAL_{name}:\n{environ[f"TAL_{name}"]}')
                    print(e)
                    exit(1)
                self.arg[name] = enforce_type_of_yaml_var(yaml_var=self.arg[name], typestr=val_type, varname=name)
            else:
                for out in [stdout, stderr]:
                    print(f"# Unrecoverable Error: type {val_type} not yet supported in args list (the set of supported types can be extended by communities of problem makers adding further elif clauses here above). Used to interpret arg {name}.", file=out)
                exit(1)
                

class Lang:
    def __init__(self, ENV, TAc, service_server_eval, book_strictly_required=False, print_opening_msg = 'delayed'):
        assert print_opening_msg in ['delayed','never','now']
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
                                TAc.print(f"Internal error (if you are invoking a cloud service, please, report it to those responsible for the service hosted:", "red", ["bold"])
                                TAc.print(f" the messages_book file `{self.messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file).", "red", ["bold"])
                                print(f" The service {ENV.service} you required for problem {ENV.problem} strictly requires this .yaml file.", file=out)
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
        if print_opening_msg == 'now':
            self.print_opening_msg()
        elif print_opening_msg == 'never':
            self.to_be_printed_opening_msg = False
        
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
        self.opening_msg += self.render_feedback("feedback_source",f'# The phrases used in this call of the service are the ones hardcoded in the service server (file {self.ENV.exe_fullname}).', {"problem":problem, "service":service, "ENV":self.ENV, "lang":self.ENV["lang"]})
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


