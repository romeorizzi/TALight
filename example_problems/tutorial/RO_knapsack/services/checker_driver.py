#!/usr/bin/env python3
from sys import exit
from typing import Optional, List

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_problems_lib as RO
import knapsack_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('elementi','list_of_str'),
    ('pesi','list_of_int'),
    ('valori','list_of_int'),
    ('Knapsack_Capacity',int),
    ('elementi_proibiti','list_of_str'),
    ('elementi_obbligati','list_of_str'),
    ('sol_type',str),
    ('opt_sol','yaml'),
    ('opt_val','yaml'),
    ('DPtable','yaml'),
    ('pt_formato_OK',int),
    ('pt_feasibility_OK',int),
    ('pt_tot',int),
    ('esercizio',int),
    ('task',int),
    ('name_of_opt_val',str),
    ('name_of_opt_sol',str),
    ('name_of_DPtable',str),
    ('color_implementation',str),
    ('as_yaml_with_points',bool),
    ('with_output_files',bool),
    ('recall_input',bool),
    ('with_opening_message',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
SEF = RO.std_eval_feedback(TAc.color_implementation)

LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

RO.check_access_rights(ENV,TALf, ask_pwd = False, ask_token = False)
knapsack_lib.check_request_consistency(ENV)

def verif_knapsack(task_number,elements:List[str],weights:List[int],vals:List[int],Capacity:int, answ, pt_tot=None,pt_formato_OK=None,pt_feasibility_OK=None,elementi_proibiti:List[str]=[],elementi_obbligati:List[str]=[]):
    new_line = '\n'
    feedback_summary = ""
    elementi=[]
    pesi=[]
    valori=[]
    for ele,peso,val in zip(elements,weights,vals):
        if ele not in elementi_proibiti:
            elementi.append(ele)
            pesi.append(peso)
            valori.append(val)
    if answ['sol_type'] in ["opt_val","opt_sol_with_val"]:
        if type(answ['opt_val']) != int:
            feedback_summary += f"formato di `{answ['name_of_opt_val']}`: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{answ['name_of_opt_val']}` hai immesso `{answ['opt_val']}` dove era invece richiesto di immettere un intero.", pt_tot,pt_safe=None,pt_out=pt_tot)
        if answ['sol_type'] == "opt_val":
            feedback_summary += f"formato di `{answ['name_of_opt_val']}`: "+SEF.colored(f"OK [{pt_formato_OK} safe pt]{new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{answ['name_of_opt_val']}` hai immesso un intero come richiesto."+SEF.colored(f"{new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.", pt_tot,pt_safe=pt_formato_OK,pt_out=0)
        else:
            feedback_summary += f"formato di `{answ['name_of_opt_val']}`: "+SEF.colored(f"OK{new_line}", "green", ["bold"])

    if answ['sol_type'] in ["opt_sol","opt_sol_with_val"]:
        if type(answ['opt_sol']) != list:
            feedback_summary += f"formato di `{answ['name_of_opt_sol']}`: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{answ['name_of_opt_sol']}` è richiesto si inserisca una lista di oggetti (esempio ['{elementi[0]}','{elementi[2]}']). Hai invece immesso `{answ['opt_sol']}`.", pt_tot,pt_safe=None,pt_out=pt_tot)
        sum_valori=0
        sum_pesi=0
        for ele in answ['opt_sol']:
            if ele not in elementi:
                feedback_summary += f"formato di `{answ['name_of_opt_sol']}`: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Ogni elemento che collochi nella lista `{answ['name_of_opt_sol']}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {elementi}.", pt_tot,pt_safe=None,pt_out=pt_tot)
            index_of_ele = elementi.index(ele)
            sum_valori += valori[index_of_ele]
            sum_pesi += pesi[index_of_ele]
        feedback_summary += f"formato di `{answ['name_of_opt_sol']}`: "+SEF.colored(f"OK [{pt_formato_OK} safe pt]{new_line}", "green", ["bold"])
        for ele in elementi_obbligati:
            if ele not in answ['opt_sol']:
                feedback_summary += f"ammissibilità della soluzione in `{answ['name_of_opt_sol']}`: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Nella lista `{answ['name_of_opt_sol']}` hai dimenticato di inserire l'elemento `{ele}` che è uno degli elementi_obbligati. La tua soluzione è tenuta a contenerlo!", pt_tot,pt_safe=None,pt_out=pt_tot)
        for ele in answ['opt_sol']:
            if ele in elementi_proibiti:
                feedback_summary += f"ammissibilità della soluzione in `{answ['name_of_opt_sol']}`: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Nella lista `{answ['name_of_opt_sol']}` hai inserire l'elemento `{ele}` che è uno degli elementi proibiti. La tua soluzione non deve contenerlo!", pt_tot,pt_safe=None,pt_out=pt_tot)
        if sum_pesi > Capacity:
            feedback_summary += f"ammissibilità della soluzione in `{answ['name_of_opt_sol']}`: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda).", pt_tot,pt_safe=None,pt_out=pt_tot)
        feedback_summary += f"ammissibilità della soluzione in {answ['name_of_opt_sol']}: "+SEF.colored(f"OK [{pt_feasibility_OK} safe pt]{new_line}", "green", ["bold"])
        if answ['sol_type'] == "opt_sol":
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{answ['name_of_opt_sol']}` è ammissibile."+SEF.colored(f"{new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo o meno.)", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)
        assert answ['sol_type'] == "opt_sol_with_val"
        if sum_valori > answ['opt_val']:
            feedback_summary += f"{answ['name_of_opt_val']}={answ['opt_val']}<{sum_valori}, che è la somma dei valori su {answ['name_of_opt_sol']}: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
        if sum_valori < answ['opt_val']:
            feedback_summary += f"{answ['name_of_opt_val']}={answ['opt_val']}>{sum_valori}, che è la somma dei valori su {answ['name_of_opt_sol']}: "+SEF.colored(f"NO{new_line}", "red", ["bold"])
        if sum_valori != answ['opt_val']:
            return SEF.evaluation_format(task_number, feedback_summary, f"Il valore della soluzione immessa è {sum_valori} e non {answ['opt_val']} come hai immesso in `{answ['name_of_opt_val']}`. A mè risulta che la soluzione (ammissibile) che hai immesso sia {answ['opt_sol']}.", pt_tot,pt_safe=pt_formato_OK,pt_out=pt_tot - pt_formato_OK)
        else:
            feedback_summary += f"{answ['name_of_opt_val']}={answ['opt_val']} = somma dei valori su {answ['name_of_opt_sol']}: "+SEF.colored(f"OK{new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{answ['name_of_opt_sol']}` è ammissibile ed il suo valore corrisponde a quanto in `{answ['name_of_opt_val']}`."+SEF.colored(f"{new_line}Nota:", "cyan", ["bold"])+" Ovviamente in sede di esame non posso dirti se sia anche ottimo o meno.", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)

            

feedback_dict = verif_knapsack(ENV["task"],ENV["elementi"],ENV["pesi"],ENV["valori"],ENV["Knapsack_Capacity"], \
                                answ={"sol_type":ENV["sol_type"],"opt_sol":ENV["opt_sol"],"opt_val":ENV["opt_val"],"DPtable":ENV["DPtable"], \
                                      "name_of_opt_sol":ENV["name_of_opt_sol"], "name_of_opt_val":ENV["name_of_opt_val"], "name_of_DPtable":ENV["name_of_DPtable"]}, \
                                 pt_tot=ENV["pt_tot"],pt_formato_OK=ENV["pt_formato_OK"],pt_feasibility_OK=ENV["pt_feasibility_OK"],elementi_proibiti=ENV["elementi_proibiti"],elementi_obbligati=ENV["elementi_obbligati"])
if ENV['recall_input']:
    feedback_dict['input'] = knapsack_lib.dict_of_input(ENV)
if ENV['as_yaml_with_points']:
    print(feedback_dict)
else:
    print(feedback_dict['feedback_string'])


feedback_string = feedback_dict['feedback_string']
pt_safe = feedback_dict['pt_safe']
pt_maybe = feedback_dict['pt_maybe']
if ENV.LOG_FILES != None:
    opt_val, opt_sol, DPtable = knapsack_lib.solver(ENV)
    oracle_dict = knapsack_lib.dict_of_oracle(ENV, opt_val,opt_sol,DPtable)
    submission_dict = knapsack_lib.dict_of_input(ENV)
    pt_true = ENV['pt_tot']
    for key in oracle_dict:
        if ENV[key] != oracle_dict[key]:
            pt_true = pt_safe
    TALf.str2log_file(content="FEEDBACK: "+repr(feedback_dict)+"STUDENT_SUBMISSION: "+repr(submission_dict)+"ORACLE: "+repr(oracle_dict), filename=f'problem_{ENV["esercizio"]}_task_{ENV["task"]}_safe_{pt_safe}_maybe_{pt_maybe}_true_{pt_true}', timestamped = False)

if ENV["with_output_files"]:    
    TALf.str2output_file(content="FEEDBACK: "+repr(feedback_dict)+"STUDENT_SUBMISSION: "+repr(submission_dict), filename=f'problem_{ENV["esercizio"]}_task_{ENV["task"]}_safe_{pt_safe}_maybe_{pt_maybe}', timestamped = False)



