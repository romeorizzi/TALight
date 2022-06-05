#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable
import termcolor 
from ansi2html import Ansi2HTMLConverter
ansi2html = Ansi2HTMLConverter(inline = True)

from multilanguage import enforce_type_of_yaml_var

def check_access_rights(ENV,TALf, require_pwd = False, TOKEN_REQUIRED = True):
    if require_pwd and ENV["pwd"] != 'tmppwd':
        print(f'Password di accesso non corretta (password immessa: `{ENV["pwd"]}`)')
        exit(0)    
    if TOKEN_REQUIRED and ENV.LOG_FILES == None:
        print("Il servizio è stato chiamato senza access token. Modalità attualmente non consentita.")
        exit(0)    


class std_eval_feedback:
    def __init__(self, COLOR_IMPLEMENTATION ="ANSI", new_line='\n'):
        self.COLOR_IMPLEMENTATION = COLOR_IMPLEMENTATION
        self.new_line = new_line
    
    def colored(self, msg_text, *msg_rendering):
        if self.COLOR_IMPLEMENTATION == None:
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
            ANSI_msg = termcolor.colored(msg_text, *msg_colors, attrs=msg_style)
        if self.COLOR_IMPLEMENTATION == 'ANSI':
            colored_msg = ANSI_msg
        elif self.COLOR_IMPLEMENTATION == 'html':
            colored_msg = ansi2html.convert(ANSI_msg.replace(">", "&gt;").replace("<", "&lt;"), full=False).replace(self.new_line, "\n<br/>")
        else:
            assert self.COLOR_IMPLEMENTATION == None
        return colored_msg

    def evaluation_format(self, task_number, feedback_summary,feedback_message, pt_tot:int,pt_safe:Optional[int] = None,pt_out:Optional[int] = None):
        pt_maybe = pt_tot-(pt_safe if pt_safe != None else 0)-(pt_out if pt_out != None else 0)
        index_pt=task_number-1
        ret_str = feedback_summary + "Totalizzi "
        ret_str += self.colored(f"[punti sicuri: {pt_safe}]", "green", ["bold"]) + ", "
        ret_str += self.colored(f"[punti aggiuntivi possibili: {pt_maybe}]", "blue", ["bold"]) + ", " 
        ret_str += self.colored(f"[punti fuori portata: {pt_out}]", "red", ["bold"]) + self.colored(f"{self.new_line}Spiegazione: ", "cyan", ["bold"]) + feedback_message + self.colored(f"{self.new_line}")
        if pt_safe == None:
            pt_safe = 0
        if pt_out == None:
            pt_out = 0
        return {'pt_safe':pt_safe,'pt_maybe':pt_maybe,'pt_out':pt_out,'pt_available':pt_tot,'feedback_string':ret_str}


    
def dict_of_instance(instance_objects,args_list,ENV):
    if len(ENV["instance_dict"]) == 0:
        return {var_name:ENV[var_name] for var_name in instance_objects}
    #print("CASE: the instance objects have been passed one by one, NOT through the `instance_dict` dictionary"):
    instance_dict = {}
    args_dict = { obj_name:obj_type  for obj_name,obj_type in args_list }
    for obj_name in instance_objects:
        obj_type = args_dict[obj_name] 
        if obj_name in ENV["instance_dict"]:
            obj_val = ENV["instance_dict"][obj_name]
        elif obj_type == str:
            obj_val = ""
        elif obj_type[:len('matrix_of_')] == 'matrix_of_' or obj_type[:len('list_of_')] == 'list_of_':
            obj_val = []
        elif obj_type in [bool, int]:
            obj_val = 0
        instance_dict[obj_name] = enforce_type_of_yaml_var(obj_val,obj_type, varname=obj_name)
    return instance_dict


def check_request(request_dict, implemented):
    for std_name, ad_hoc_name in request_dict.items():
        if std_name not in implemented:
            print(f'Error: the solution object type {std_name} is not available at present (not yet implemented or turned off). The value `{std_name}` appeared in the `request_dict` dictionary passed as argument to the TALight service.')    
            exit(0)
        

def check_and_standardization_of_request_answer_consistency(answer_dict:Dict, names_dict:dict, answer_object_type_spec:Dict, implemented:List[str]):
    """
    arguments:
      answer_dict               ad-hoc name --> answ_obj
      names_dict                ad-hoc name --> std_name
      answer_object_type_spec   answer object type --> its type as python data-structure
      implemented  contains the std_names of available answer object types
    returns:
       request_dict             ad-hoc name --> std_name
       answ_dict                ad-hoc name --> answ_obj
       name_of                  std_name --> ad-hoc name
       answ_obj                 std_name --> answ_obj
       long_answer_dict         std_name --> (answ_obj, ad-hoc name)
       goals  is the list of the std_names of the answ_objects that have been submitted by the student/problem solver (they are precisely those requested by the exercise evaluated)
    """
    for std_name in names_dict.values():
        if std_name not in implemented:
            print(f'Error: the solution object type {std_name} is not available at present (not yet implemented or turned off). The value `{std_name}` appeared in the `names_dict` dictionary passed as argument to the TALight service.')    
            exit(0)
    request_dict = {}
    answ_dict = {}    
    name_of = {}    
    answ_obj = {}    
    long_answer_dict = {}
    for ad_hoc_name in answer_dict:
        if ad_hoc_name in names_dict:
            std_name = names_dict[ad_hoc_name]
        else:
            std_name = ad_hoc_name
            if std_name not in implemented:
                print(f'Error: the key `{ad_hoc_name}` in the `answer_dict` dictionary passed as argument to the service is neither a standard name nor has been remapped through the `names_dict` dictionary.')    
                exit(0)
        #print(f"now checking variable of ad_hoc_name={ad_hoc_name} and value={answer_dict[ad_hoc_name]}. Its std_name={std_name} deserves a format {answer_object_type_spec[std_name]}, while it actually is {type(answer_dict[ad_hoc_name])}",file=stderr)
        answer_dict[ad_hoc_name] = enforce_type_of_yaml_var(answer_dict[ad_hoc_name],answer_object_type_spec[std_name], varname=ad_hoc_name)
        request_dict[ad_hoc_name] = std_name 
        answ_dict[ad_hoc_name] = answer_dict[ad_hoc_name]
        name_of[std_name] = ad_hoc_name    
        answ_obj[std_name] = answer_dict[ad_hoc_name]    
        long_answer_dict[std_name] = (answer_dict[ad_hoc_name], ad_hoc_name)
    return request_dict, answ_dict, name_of, answ_obj, long_answer_dict, answ_obj.keys()


def add_ENV_var(var_name:str, d:Dict, ENV, condition:Callable[[str], bool] = lambda x : True):
    if condition(ENV[var_name]):
        d[var_name] = ENV[var_name]

def add_ENV_vars(var_names:List[str], d:Dict, ENV, condition:Callable[[str], bool] = lambda x : True):
    for var_name in var_names:
        if condition(ENV[var_name]):
            d[var_name] = ENV[var_name]

def add_named_ENV_var(var_name:str, d:Dict, ENV, condition:Callable[[str], bool] = lambda x : True):
    if condition(ENV[var_name]):
        d[ENV['name_of_'+var_name]] = ENV[var_name]
    
def display_dict(dict):
    for key,val in dict.items():
        print(f"{key}: {val}")
        
def oracle_outputs(call_data,ENV):
    if ENV['as_yaml']:
        if not (ENV["recall_instance"] or ENV["recall_request"]):
            print(call_data['oracle'])
        else:
            if not ENV["recall_instance"]:
                call_data.pop("instance", None)
            if not ENV["recall_request"]:
                call_data.pop("request", None)
            print(call_data)
    else:
        display_dict(call_data['oracle'])
        if ENV['recall_request']:
            print()
            display_dict(call_data['request'])
        if ENV['recall_instance']:
            print()
            display_dict(call_data['instance'])

def oracle_output_files(call_data,ENV,TALf):
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'oracle_answer'
    TALf.str2output_file(content=repr(call_data), filename=filename_spec, timestamped = False)
    
    if ENV['as_yaml']:
        if not (ENV["recall_instance"] or ENV["recall_request"]):
            print(call_data['oracle'])
        else:
            if not ENV["recall_instance"]:
                call_data.pop("instance", None)
            if not ENV["recall_request"]:
                call_data.pop("request", None)
            print(call_data)
    else:
        display_dict(call_data['oracle'])
        if ENV['recall_request']:
            print()
            display_dict(call_data['request'])
        if ENV['recall_instance']:
            print()
            display_dict(call_data['instance'])

def oracle_logs(call_data,ENV,TALf):
    content_LOG_file = "INSTANCE: "+repr(call_data['instance'])+"\n\nREQUEST: "+repr(call_data['request'])+"\n\nORACLE_ANSWER: "+repr(call_data['oracle'])
    #print(f"content_LOG_file =`{content_LOG_file}`", file=stderr)
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    filename_spec += f'task_{ENV["task"]}' if ENV["task"] != -1 else 'unspecified'
    TALf.str2log_file(content=content_LOG_file, filename=filename_spec, timestamped = False)


def checker_reply(all_data,ENV):
    feedback_dict = all_data["feedback"]
    #print(f"feedback_dict={feedback_dict}", file=stderr)
    if ENV["recall_instance"]:
        feedback_dict["instance"] = all_data["instance"]
    feedback_dict["answer"] = all_data["long_answer"]
    if ENV["as_yaml_with_points"]:
        print(feedback_dict)
    else:
        print(feedback_dict["feedback_string"])
    
def checker_logs(all_data,ENV,TALf):
    feedback_dict = all_data["feedback"]
    oracle_dict = all_data["oracle"]
    pt_safe = feedback_dict['pt_safe']
    pt_maybe = feedback_dict['pt_maybe']
    pt_available = feedback_dict['pt_available']
    for key in oracle_dict:
        if ENV[key] != oracle_dict[key]:
            pt_available = pt_safe
    content_LOG_file = "FEEDBACK: "+repr(feedback_dict)+"\n\nSTUDENT_ANSWER: "+repr(all_data["long_answer"])+"\n\nORACLE: "+repr(oracle_dict)+"\n\nINSTANCE: "+repr(all_data["instance"])
    #print(f"content_LOG_file =`{content_LOG_file}`", file=stderr)
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'safe_{pt_safe}_maybe_{pt_maybe}_true_{pt_available}'
    TALf.str2log_file(content=content_LOG_file, filename=filename_spec, timestamped = False)
    
def checker_certificates(all_data,ENV,TALf):
    feedback_dict = all_data["feedback"]
    pt_safe = feedback_dict['pt_safe']
    pt_maybe = feedback_dict['pt_maybe']
    content_receipt_file  = "FEEDBACK: "+repr(feedback_dict)+"\n\nSTUDENT_ANSWER: "+repr(all_data["long_answer"])+"\n\nINSTANCE: "+repr(all_data["instance"])
    #print("content_receipt_file =`{content_receipt_file}`", file=stderr)
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'safe_{pt_safe}_maybe_{pt_maybe}'
    TALf.str2output_file(content=content_receipt_file, filename=filename_spec, timestamped = False)

        
