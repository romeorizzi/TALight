#!/usr/bin/env python3
from sys import exit
from typing import Optional, List, Dict, Tuple

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_problems_lib as RO
import lcs_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('s','str'),
    ('t','str'),
    ('start_with','str'),
    ('end_with','str'),
    ('forbidden_s_interval_first_pos','int'),
    ('forbidden_s_interval_last_pos','int'),
    ('initDPtable_prefix','matrix_of_int'),
    ('initDPtable_suffix','matrix_of_int'),
    ('sol_type',str),
    ('opt_sol','yaml'),
    ('opt_val','yaml'),
    ('DPtable','yaml'),
    ('name_of_opt_val',str),
    ('name_of_opt_sol',str),
    ('name_of_DPtable_prefix',str),
    ('name_of_DPtable_suffix',str),
    ('color_implementation',str),
    ('as_yaml_with_points',bool),
    ('yield_certificate_in_output_file',bool),
    ('recall_input',bool),
    ('with_opening_message',bool),
    ('pt_formato_OK',int),
    ('pt_feasibility_OK',int),
    ('pt_tot',int),
    ('esercizio',int),
    ('task',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
SEF = RO.std_eval_feedback(TAc.color_implementation)

LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

TOKEN_REQUIRED = False
RO.check_access_rights(ENV,TALf, require_pwd = False, TOKEN_REQUIRED = TOKEN_REQUIRED)
lcs_lib.check_request_consistency(ENV)

def verif_lcs(task_number:int,pt_tot:int,pt_formato_OK:int,pt_feasibility_OK:int, s:str,t:str,start_with:str,end_with:str,forbidden_s_interval_first_pos:int,forbidden_s_interval_last_pos:int,initDPtable_prefix:List[List[int]],initDPtable_suffix:List[List[int]], answer:Dict):
    feedback_summary = ""
    elementi=[]
    pesi=[]
    valori=[]
    for ele,peso,val in zip(elements,weights,vals):
        if ele not in elementi_proibiti:
            elementi.append(ele)
            pesi.append(peso)
            valori.append(val)
    if answer['sol_type'] in ["opt_val","opt_sol_with_val"]:
        if type(answer['opt_val']) != int:
            feedback_summary += f"formato di `{answer['name_of_opt_val']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{answer['name_of_opt_val']}` hai immesso `{answer['opt_val']}` dove era invece richiesto di immettere un intero.", pt_tot,pt_safe=None,pt_out=pt_tot)
        if answer['sol_type'] == "opt_val":
            feedback_summary += f"formato di `{answer['name_of_opt_val']}`: "+SEF.colored(f"OK [{pt_formato_OK} safe pt]{SEF.new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{answer['name_of_opt_val']}` hai immesso un intero come richiesto."+SEF.colored(f"{SEF.new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.", pt_tot,pt_safe=pt_formato_OK,pt_out=0)
        else:
            feedback_summary += f"formato di `{answer['name_of_opt_val']}`: "+SEF.colored(f"OK{SEF.new_line}", "green", ["bold"])

    if answer['sol_type'] in ["opt_sol","opt_sol_with_val"]:
        if type(answer['opt_sol']) != list:
            feedback_summary += f"formato di `{answer['name_of_opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{answer['name_of_opt_sol']}` è richiesto si inserisca una lista di oggetti (esempio ['{elementi[0]}','{elementi[2]}']). Hai invece immesso `{answer['opt_sol']}`.", pt_tot,pt_safe=None,pt_out=pt_tot)
        sum_valori=0
        sum_pesi=0
        for ele in answer['opt_sol']:
            if ele not in elementi:
                feedback_summary += f"formato di `{answer['name_of_opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Ogni elemento che collochi nella lista `{answer['name_of_opt_sol']}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {elementi}.", pt_tot,pt_safe=None,pt_out=pt_tot)
            index_of_ele = elementi.index(ele)
            sum_valori += valori[index_of_ele]
            sum_pesi += pesi[index_of_ele]
        feedback_summary += f"formato di `{answer['name_of_opt_sol']}`: "+SEF.colored(f"OK [{pt_formato_OK} safe pt]{SEF.new_line}", "green", ["bold"])
        for ele in elementi_obbligati:
            if ele not in answer['opt_sol']:
                feedback_summary += f"ammissibilità della soluzione in `{answer['name_of_opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Nella lista `{answer['name_of_opt_sol']}` hai dimenticato di inserire l'elemento `{ele}` che è uno degli elementi_obbligati. La tua soluzione è tenuta a contenerlo!", pt_tot,pt_safe=None,pt_out=pt_tot)
        for ele in answer['opt_sol']:
            if ele in elementi_proibiti:
                feedback_summary += f"ammissibilità della soluzione in `{answer['name_of_opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Nella lista `{answer['name_of_opt_sol']}` hai inserire l'elemento `{ele}` che è uno degli elementi proibiti. La tua soluzione non deve contenerlo!", pt_tot,pt_safe=None,pt_out=pt_tot)
        if sum_pesi > Capacity:
            feedback_summary += f"ammissibilità della soluzione in `{answer['name_of_opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda).", pt_tot,pt_safe=None,pt_out=pt_tot)
        if answer['sol_type'] == "opt_sol":
            feedback_summary += f"ammissibilità della soluzione in {answer['name_of_opt_sol']}: "+SEF.colored(f"OK [{pt_feasibility_OK} safe pt]{SEF.new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{answer['name_of_opt_sol']}` è ammissibile."+SEF.colored(f"{SEF.new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo o meno.)", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)
        assert answer['sol_type'] == "opt_sol_with_val"
        feedback_summary += f"ammissibilità della soluzione in {answer['name_of_opt_sol']}: "+SEF.colored(f"OK{SEF.new_line}", "green", ["bold"])
        if sum_valori != answer['opt_val']:
            feedback_summary += f"autoconsistenza: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il valore della soluzione immessa in `{answer['name_of_opt_sol']}` è {sum_valori}, non {answer['opt_val']} come hai immesso in `{answer['name_of_opt_val']}`. La soluzione (ammissibile) che hai immesso è {answer['opt_sol']}", pt_tot,pt_safe=pt_formato_OK,pt_out=pt_tot - pt_formato_OK)
        else:
            feedback_summary += f"{answer['name_of_opt_val']}={answer['opt_val']} = somma dei valori su {answer['name_of_opt_sol']}: "+SEF.colored(f"OK [{pt_feasibility_OK} safe pt]{SEF.new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{answer['name_of_opt_sol']}` è ammissibile ed il suo valore corrisponde a quanto in `{answer['name_of_opt_val']}`."+SEF.colored(f"{SEF.new_line}Nota:", "cyan", ["bold"])+" Ovviamente in sede di esame non posso dirti se sia anche ottimo o meno.", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)

            

feedback_dict = verif_lcs(ENV["task"],pt_tot=ENV["pt_tot"],pt_formato_OK=ENV["pt_formato_OK"],pt_feasibility_OK=ENV["pt_feasibility_OK"], \
                          ENV["s"],ENV["t"],ENV["start_with"],ENV["end_with"],ENV["forbidden_s_interval_first_pos"],ENV["forbidden_s_interval_last_pos"],ENV["initDPtable_prefix"],ENV["initDPtable_suffix"], \
                          answer={"sol_type":ENV["sol_type"],"opt_sol":ENV["opt_sol"],"opt_val":ENV["opt_val"],"DPtable_prefix":ENV["DPtable_prefix"],"DPtable_suffix":ENV["DPtable_suffix"], \
                                "name_of_opt_sol":ENV["name_of_opt_sol"], "name_of_opt_val":ENV["name_of_opt_val"], "name_of_DPtable":ENV["name_of_DPtable"]} )

submission_dict = lcs_lib.dict_of_input(ENV)
RO.checker_reply(submission_dict,feedback_dict,ENV)
if ENV.LOG_FILES != None:
    opt_val, opt_sol, DPtable = lcs_lib.solver(ENV)
    oracle_dict = lcs_lib.dict_of_oracle(ENV, opt_val,opt_sol,DPtable)
    RO.checker_logs(oracle_dict,feedback_dict,submission_dict,ENV,TALf)
if ENV["yield_certificate_in_output_file"]:    
    RO.checker_certificates(feedback_dict,submission_dict,ENV,TALf)



