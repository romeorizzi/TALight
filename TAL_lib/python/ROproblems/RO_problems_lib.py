#!/usr/bin/env python3
from typing import Optional, List
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
    def __init__(self, COLOR_IMPLEMENTATION ="ANSI"):
        self.COLOR_IMPLEMENTATION = COLOR_IMPLEMENTATION
    
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
            colored_msg = ansi2html.convert(ANSI_msg.replace(">", "&gt;").replace("<", "&lt;"), full=False).replace("\n", "\n<br/>")
        else:
            assert self.COLOR_IMPLEMENTATION == None
        return colored_msg

    def evaluation_format(self, task_number, feedback_summary,feedback_message, pt_tot:int,pt_safe:Optional[int] = None,pt_out:Optional[int] = None):
        pt_maybe = pt_tot-(pt_safe if pt_safe != None else 0)-(pt_out if pt_out != None else 0)
        index_pt=task_number-1
        new_line = '\n'
        ret_str = feedback_summary + "Totalizzi "
        ret_str += self.colored(f"[punti sicuri: {pt_safe}]", "green", ["bold"]) + ", "
        ret_str += self.colored(f"[punti aggiuntivi possibili: {pt_maybe}]", "blue", ["bold"]) + ", " 
        ret_str += self.colored(f"[punti fuori portata: {pt_out}]", "red", ["bold"]) + self.colored(f"{new_line}Spiegazione: ", "cyan", ["bold"]) + feedback_message + self.colored(f"{new_line}")
        if pt_safe == None:
            pt_safe = 0
        if pt_out == None:
            pt_out = 0
        return {'pt_safe':pt_safe,'pt_maybe':pt_maybe,'pt_out':pt_out,'feedback_string':ret_str}


def display_dict(dict):
    for key,val in dict.items():
        print(f"{key}: {val}")
        
def oracle_output(ENV, call_data):
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

    
