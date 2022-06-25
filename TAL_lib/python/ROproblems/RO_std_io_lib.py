#!/usr/bin/env python3
from sys import stderr, stdout
from typing import Optional, List, Dict, Callable
import termcolor 
from ansi2html import Ansi2HTMLConverter
ansi2html = Ansi2HTMLConverter(inline = True)

from multilanguage import enforce_type_of_yaml_var

def check_access_rights(ENV,TALf, require_pwd = False, TOKEN_REQUIRED = True):
    if require_pwd and ENV["pwd"] != 'tmppwd':
        for error_stream in [stdout,stderr]:
            print(f'Errore (RO_std_io_lib): Password di accesso non corretta (password immessa: `{ENV["pwd"]}`)', file=error_stream)
        exit(0)    
    if TOKEN_REQUIRED and ENV.LOG_FILES == None:
        for error_stream in [stdout,stderr]:
            print("Errore (RO_std_io_lib): Il servizio è stato chiamato senza access token. Modalità attualmente non consentita.", file=error_stream)
        exit(0)    

            
def dict_of_instance(instance_objects,args_list,ENV):
    if len(ENV["input_data_assigned"]) == 0:
        #print('CASE: the instance objects have been passed one by one', file=stderr)
        return {obj_name:ENV[obj_name] for obj_name,obj_type in instance_objects}
    #print('CASE: the instance objects have been passed as a dictionary, through the `ENV["input_data_assigned"]` variable', file=stderr)
    input_data_assigned = {}
    for obj_name,obj_type in instance_objects:
        #print(f"obj_name={obj_name}, obj_type={obj_type}", file=stderr)
        if obj_name in ENV["input_data_assigned"]:
            obj_val = ENV["input_data_assigned"][obj_name]
            #print(f"TROVATO: obj_name={obj_name}, obj_type={obj_type}", file=stderr)
            input_data_assigned[obj_name] = enforce_type_of_yaml_var(obj_val,obj_type, varname=obj_name)
        else:
            input_data_assigned[obj_name] = ENV[obj_name] # each instance object left unspecified within the dictionary passed on the input_data_assigned argument is set to its value on its single object argument (ultimately, its default value in case neither this had been explicitly set with the call)
#        elif obj_type == str:
#            obj_val = ""
#        elif obj_type in [bool, int]:
#            pass
#            for error_stream in [stdout,stderr]:
#                print(f"Error (RO_std_io_lib): the value for the service argument {obj_name} has not been specified within the non-empty dictionary passed on the input_data_assigned argument", file=error_stream)
#            exit(0)
#        elif obj_type[:len('matrix_of_')] == 'matrix_of_' or obj_type[:len('list_of_')] == 'list_of_':
#            obj_val = []
    return input_data_assigned


def check_request(request_dict, implemented):
    for std_name, ad_hoc_name in request_dict.items():
        if std_name not in implemented:
            for error_stream in [stdout,stderr]:
                print(f'Error (RO_std_io_lib): the solution object type {std_name} is not available at present (not yet implemented or turned off). The value `{std_name}` appeared in the `request_dict` dictionary passed as argument to the TALight service.', file=error_stream)    
            exit(0)
        

def check_and_standardization_of_request_answer_consistency(ENV:dict, answer_object_type_spec:Dict, implemented:List[str]):
    """
    main arguments:
      ENV['answer_dict']        ad-hoc name --> answ_obj
      ENV['alias_dict']         ad-hoc name --> std_name
      answer_object_type_spec   std_name --> type_spec of the object (e.g., 'list_of_list_of_int')
      implemented  contains the std_names of available answer object types
    returns:
       request_dict             ad-hoc name --> std_name
       answ_dict                ad-hoc name --> answ_obj
       name_of                  std_name --> ad-hoc name
       answ_obj                 std_name --> answ_obj
       long_answer_dict         std_name --> (answ_obj, ad-hoc name, type_spec)
       goals  is the list of the std_names of the answ_objects that have been submitted by the student/problem solver (they are precisely those requested by the exercise evaluated)
    """
    #print(f"answer_dict={answer_dict}, alias_dict={alias_dict}, answer_object_type_spec={answer_object_type_spec}, implemented={implemented}",file=stderr)
    if len(ENV["answer_dict"]) != 0:
        #print("CASE: the instance objects have been passed as a dictionary, through the `ENV["input_data_assigned"]` variable", file=stderr)
        answer_dict = ENV['answer_dict']
        alias_dict = ENV['alias_dict']
    else:
        #print("CASE: the instance objects have been passed one by one", file=stderr)
        answer_dict={}; alias_dict={}
        for std_name in implemented:
            #print(f"type(ENV[{std_name}])={type(ENV[std_name])}, answer_object_type_spec[{std_name}]={answer_object_type_spec[std_name]}, ENV[{std_name}]={ENV[std_name]}", file=stderr)
            type_spec = answer_object_type_spec[std_name]
            if type(type_spec) != str or ( (type_spec[:len('list_of_')] != 'list_of_' or len(ENV[std_name]) != 0) and (type_spec[:len('matrix_of_')] != 'matrix_of_' or len(ENV[std_name]) != 0) ):
                answer_dict[std_name] = ENV[std_name]
                alias_dict[std_name] = std_name
    for std_name in alias_dict.values():
        if std_name not in implemented:
            for error_stream in [stdout,stderr]:
                print(f'Error (RO_std_io_lib): the solution object type {std_name} is not available at present (not yet implemented or turned off). The value `{std_name}` appeared in the `alias_dict` dictionary passed as argument to the TALight service.', file=error_stream)    
            exit(0)
    request_dict = {}
    answ_dict = {}    
    name_of = {}    
    answ_obj = {}    
    long_answer_dict = {}
    for ad_hoc_name in answer_dict:
        if ad_hoc_name in alias_dict:
            std_name = alias_dict[ad_hoc_name]
        else:
            std_name = ad_hoc_name
        if std_name not in implemented:
            for error_stream in [stdout,stderr]:
                print(f'Error (RO_std_io_lib): the key `{ad_hoc_name}` in the `answer_dict` dictionary passed as argument to the service is neither a standard name nor has been remapped through the `alias_dict` dictionary.', file=error_stream)    
            exit(0)
        #print(f"now checking variable of ad_hoc_name={ad_hoc_name} and value={answer_dict[ad_hoc_name]}. Its std_name={std_name} deserves a format {answer_object_type_spec[std_name]}, while it actually is {type(answer_dict[ad_hoc_name])}",file=stderr)
        answer_dict[ad_hoc_name] = enforce_type_of_yaml_var(answer_dict[ad_hoc_name],answer_object_type_spec[std_name], varname=ad_hoc_name)
        request_dict[ad_hoc_name] = std_name 
        answ_dict[ad_hoc_name] = answer_dict[ad_hoc_name]
        name_of[std_name] = ad_hoc_name    
        answ_obj[std_name] = answer_dict[ad_hoc_name]    
        long_answer_dict[std_name] = (answer_dict[ad_hoc_name], ad_hoc_name, answer_object_type_spec[std_name])
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
        if not (ENV["recall_data_assigned"] or ENV["recall_request"]):
            print(call_data['oracle'])
        else:
            if not ENV["recall_data_assigned"]:
                call_data.pop("input_data_assigned", None)
            if not ENV["recall_request"]:
                call_data.pop("request", None)
            print(call_data)
    else:
        display_dict(call_data['oracle'])
        if ENV['recall_request']:
            print(call_data['oracle'])
            display_dict(call_data['request'])
        if ENV['recall_data_assigned']:
            print(call_data['oracle'])
            display_dict(call_data['input_data_assigned'])

def oracle_output_files(call_data,ENV,TALf):
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'oracle_answer'
    TALf.str2output_file(content=repr(call_data), filename=filename_spec, timestamped = False)
    
    if ENV['as_yaml']:
        if not (ENV["recall_data_assigned"] or ENV["recall_request"]):
            print(call_data['oracle'])
        else:
            if not ENV["recall_data_assigned"]:
                call_data.pop("input_data_assigned", None)
            if not ENV["recall_request"]:
                call_data.pop("request", None)
            print(call_data)
    else:
        display_dict(call_data['oracle'])
        if ENV['recall_request']:
            display_dict(call_data['request'])
        if ENV['recall_data_assigned']:
            display_dict(call_data['input_data_assigned'])

def oracle_logs(call_data,ENV,TALf):
    print(f"ENV.LOG_FILES={ENV.LOG_FILES}",file=stderr)
    content_LOG_file = "INSTANCE: "+repr(call_data['input_data_assigned'])+"\n\nREQUEST: "+repr(call_data['request'])+"\n\nORACLE_ANSWER: "+repr(call_data['oracle'])
    #print(f"content_LOG_file =`{content_LOG_file}`", file=stderr)
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    filename_spec += f'task_{ENV["task"]}' if ENV["task"] != -1 else 'unspecified'
    TALf.str2log_file(content=content_LOG_file, filename=filename_spec, timestamped = False)


def checker_reply(all_data,ENV):
    #print(f"all_data={all_data}", file=stderr)
    feedback_dict = all_data["feedback"]
    #print(f"feedback_dict={feedback_dict}", file=stderr)
    if ENV["recall_data_assigned"]:
        feedback_dict["input_data_assigned"] = all_data["input_data_assigned"]
    feedback_dict["answer"] = all_data["long_answer"]
    if ENV["as_yaml_with_points"]:
        print(feedback_dict)
    else:
        print(feedback_dict["feedback_string"])
    
def checker_logs(all_data,ENV,TALf):
    feedback_dict = all_data["feedback"]
    oracle_dict = all_data["oracle"]
    #print(f"feedback_dict={feedback_dict}",file=stderr)
    pt_safe = feedback_dict['pt_safe']
    pt_maybe = feedback_dict['pt_maybe']
    pt_min = pt_safe
    pt_max = feedback_dict['pt_available'] - feedback_dict['pt_out']
    if 'exception' not in oracle_dict: 
        for key in oracle_dict:
            if ENV[key] == oracle_dict[key]: # here, to get a closer approximation, you can allow the use of a function defined by the problem maker within the problem_specific_lib 
                pt_min = pt_max
            #else:   # this cannot be said right now (in general)
            #    pt_max = pt_safe
    content_LOG_file = "FEEDBACK: "+repr(feedback_dict)+"\n\nSTUDENT_ANSWER: "+repr(all_data["long_answer"])+"\n\nORACLE: "+repr(oracle_dict)+"\n\nINSTANCE: "+repr(all_data["input_data_assigned"])
    #print(f"content_LOG_file =`{content_LOG_file}`", file=stderr)
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'safe_{pt_safe}_maybe_{pt_maybe}_min_{pt_min}_max_{pt_max}'
    TALf.str2log_file(content=content_LOG_file, filename=filename_spec, timestamped = False)
    
def checker_certificates(all_data,ENV,TALf):
    feedback_dict = all_data["feedback"]
    pt_safe = feedback_dict['pt_safe']
    pt_maybe = feedback_dict['pt_maybe']
    content_receipt_file  = "FEEDBACK: "+repr(feedback_dict)+"\n\nSTUDENT_ANSWER: "+repr(all_data["long_answer"])+"\n\nINSTANCE: "+repr(all_data["input_data_assigned"])
    #print("content_receipt_file =`{content_receipt_file}`", file=stderr)
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'safe_{pt_safe}_maybe_{pt_maybe}'
    TALf.str2output_file(content=content_receipt_file, filename=filename_spec, timestamped = False)

        
