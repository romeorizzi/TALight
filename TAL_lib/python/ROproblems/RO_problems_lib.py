#!/usr/bin/env python3
from typing import Optional, List, Dict, Callable
import termcolor 
from ansi2html import Ansi2HTMLConverter
ansi2html = Ansi2HTMLConverter(inline = True)
  
def check_access_rights(ENV,TALf, ask_pwd = False, ask_token = True):
    if ask_pwd and ENV["pwd"] != 'tmppwd':
        print(f'Password di accesso non corretta (password immessa: `{ENV["pwd"]}`)')
        exit(0)    

    if ask_token and ENV.LOG_FILES == None:
        print("Il servizio è stato chiamato senza access token. Modalità attualmente non consentita.")
        exit(0)    
    else:
        TALf.str2log_file(content="Questo log file intende consentire il tracciamento dell'utente che ha chiamato il servizio.", filename='ORACLE_CALL', timestamped = False)


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
        return {'pt_safe':pt_safe,'pt_maybe':pt_maybe,'pt_out':pt_out,'feedback_string':ret_str}

    
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
        
def oracle_outputs(ENV, call_data):
    if not ENV['recall_input']:
        call_data = call_data['oracle']
    if ENV['as_yaml']:
        print(call_data)
    else:
        if ENV['recall_input']:
            display_dict(call_data['oracle'])
            print()
            display_dict(call_data['input'])
        else:
            display_dict(call_data)

def checker_reply(input_dict,feedback_dict,ENV):
    if ENV['recall_input']:
        feedback_dict['input'] = input_dict
    if ENV['as_yaml_with_points']:
        print(feedback_dict)
    else:
        print(feedback_dict['feedback_string'])
    feedback_dict['input'] = input_dict
    
def checker_logs(oracle_dict,feedback_dict,submission_dict,ENV,TALf):
    pt_safe = feedback_dict['pt_safe']
    pt_maybe = feedback_dict['pt_maybe']
    pt_true = ENV['pt_tot']
    for key in oracle_dict:
        if ENV[key] != oracle_dict[key]:
            pt_true = pt_safe
    content_LOG_file = "FEEDBACK: "+repr(feedback_dict)+"\nSTUDENT_SUBMISSION: "+repr(submission_dict)+"\nORACLE: "+repr(oracle_dict)
    #print(f"content_LOG_file =`{content_LOG_file}`")
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'safe_{pt_safe}_maybe_{pt_maybe}_true_{pt_true}'
    TALf.str2log_file(content=content_LOG_file, filename=filename_spec, timestamped = False)
    
def checker_certificates(feedback_dict,submission_dict,ENV,TALf):
    pt_safe = feedback_dict['pt_safe']
    pt_maybe = feedback_dict['pt_maybe']
    content_receipt_file  = "FEEDBACK: "+repr(feedback_dict)+"\nSTUDENT_SUBMISSION: "+repr(submission_dict)
    #print("content_receipt_file =`{content_receipt_file}`")
    filename_spec = f'problem_{ENV["esercizio"]}_' if ENV["esercizio"] != -1 else ''
    if ENV["task"] != -1:
        filename_spec += f'task_{ENV["task"]}_'
    filename_spec += f'safe_{pt_safe}_maybe_{pt_maybe}'
    TALf.str2output_file(content=content_receipt_file, filename=filename_spec, timestamped = False)

        
