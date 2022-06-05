#!/usr/bin/env python3
from sys import exit, stderr
from typing import Optional, List, Dict, Tuple

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_problems_lib as RO
from knapsack_lib import solver, check_instance_consistency

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('elementi','list_of_str'),
    ('pesi','list_of_int'),
    ('valori','list_of_int'),
    ('Knapsack_Capacity',int),
    ('elementi_proibiti','list_of_str'),
    ('elementi_obbligati','list_of_str'),
    ('partialDPtable','matrix_of_int'),
    ('instance_dict','yaml'),
    ('opt_sol','yaml'),
    ('opt_val','yaml'),
    ('num_opt_sols','yaml'),
    ('list_opt_sols','yaml'),
    ('DPtable_opt_val','yaml'),
    ('DPtable_num_opts','yaml'),
    ('alias_dict','yaml'),
    ('answer_dict','yaml'),
    ('color_implementation',str),
    ('as_yaml_with_points',bool),
    ('yield_certificate_in_output_file',bool),
    ('recall_instance',bool),
    ('with_opening_message',bool),
    ('pt_formato_OK',int),
    ('pt_feasibility_OK',int),
    ('pt_tot',int),
    ('esercizio',int),
    ('task',int),
]
instance_objects = ['elementi','pesi','valori','Knapsack_Capacity','elementi_proibiti','elementi_obbligati','partialDPtable']
answer_object_type_spec = {
    'opt_sol':'list_of_str',
    'opt_val':'int',
    'num_opt_sols':'int',
    'list_opt_sols':'list_of_list_of_str',
    'DPtable_opt_val':'matrix_of_int',
    'DPtable_num_opts':'matrix_of_int',
}
sol_objects_implemented = ['opt_sol','opt_val','DPtable_opt_val']

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
SEF = RO.std_eval_feedback(TAc.color_implementation)

LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

TOKEN_REQUIRED = False
RO.check_access_rights(ENV,TALf, require_pwd = False, TOKEN_REQUIRED = TOKEN_REQUIRED)
instance_dict = RO.dict_of_instance(instance_objects,args_list,ENV)
check_instance_consistency(instance_dict)
request_dict, answer_dict, name_of, answ_obj, long_answer_dict, goals = RO.check_and_standardization_of_request_answer_consistency(ENV['answer_dict'],ENV['alias_dict'], answer_object_type_spec, sol_objects_implemented)
#print(f"long_answer_dict={long_answer_dict}", file=stderr)


def verif_submission(task_number:int,pt_tot:int,pt_formato_OK:int,pt_feasibility_OK:int, elements:List[str],weights:List[int],vals:List[int],Capacity:int,elementi_proibiti:List[str],elementi_obbligati:List[str],partialDPtable:List[List[int]], long_answer_dict:Dict):
    goals = long_answer_dict.keys()
    answ = { key:val[0] for key,val in long_answer_dict.items() }
    name = { key:val[1] for key,val in long_answer_dict.items() }
    feedback_summary = ""
    elementi=[]
    pesi=[]
    valori=[]
    for ele,peso,val in zip(elements,weights,vals):
        if ele not in elementi_proibiti:
            elementi.append(ele)
            pesi.append(peso)
            valori.append(val)
    num_formats_OK = 0
    if 'opt_val' in goals:
        if type(answ['opt_val']) != int:
            feedback_summary += f"formato di `{name['opt_val']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{name['opt_val']}` hai immesso `{answ['opt_val']}` dove era invece richiesto di immettere un intero.", pt_tot,pt_safe=None,pt_out=pt_tot)
        num_formats_OK += 1
        if num_formats_OK >= len(goals):
            feedback_summary += f"formato di `{name['opt_val']}`: "+SEF.colored(f"OK [{pt_formato_OK} safe pt]{SEF.new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{name['opt_val']}` hai immesso un intero come richiesto."+SEF.colored(f"{SEF.new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.", pt_tot,pt_safe=pt_formato_OK,pt_out=0)
        feedback_summary += f"formato di `{name['opt_val']}`: "+SEF.colored(f"OK{SEF.new_line}", "green", ["bold"])
    if 'opt_sol' in goals:
        if type(answ['opt_sol']) != list:
            feedback_summary += f"formato di `{name['opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Come `{name['opt_sol']}` è richiesto si inserisca una lista di oggetti (esempio ['{elementi[0]}','{elementi[2]}']). Hai invece immesso `{answ['opt_sol']}`.", pt_tot,pt_safe=None,pt_out=pt_tot)
        sum_valori=0
        sum_pesi=0
        for ele in answ['opt_sol']:
            if ele not in elementi:
                feedback_summary += f"formato di `{name['opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Ogni elemento che collochi nella lista `{name['opt_sol']}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {elementi}.", pt_tot,pt_safe=None,pt_out=pt_tot)
            index_of_ele = elementi.index(ele)
            sum_valori += valori[index_of_ele]
            sum_pesi += pesi[index_of_ele]
        num_formats_OK += 1
        if num_formats_OK >= len(goals):
            feedback_summary += f"formato di `{name['opt_sol']}`: "+SEF.colored(f"OK [{pt_formato_OK} safe pt]{SEF.new_line}", "green", ["bold"])
        else:
            feedback_summary += f"formato di `{name['opt_sol']}`: "+SEF.colored(f"OK{SEF.new_line}", "green", ["bold"])
        for ele in elementi_obbligati:
            if ele not in answ['opt_sol']:
                feedback_summary += f"ammissibilità della soluzione in `{name['opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Nella lista `{name['opt_sol']}` hai dimenticato di inserire l'elemento `{ele}` che è uno degli elementi_obbligati. La tua soluzione è tenuta a contenerlo!", pt_tot,pt_safe=None,pt_out=pt_tot)
        for ele in answ['opt_sol']:
            if ele in elementi_proibiti:
                feedback_summary += f"ammissibilità della soluzione in `{name['opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Nella lista `{name['opt_sol']}` hai inserire l'elemento `{ele}` che è uno degli elementi proibiti. La tua soluzione non deve contenerlo!", pt_tot,pt_safe=None,pt_out=pt_tot)
        if sum_pesi > Capacity:
            feedback_summary += f"ammissibilità della soluzione in `{name['opt_sol']}`: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda).", pt_tot,pt_safe=None,pt_out=pt_tot)
        if len(goals) == 1:
            feedback_summary += f"ammissibilità della soluzione in {name['opt_sol']}: "+SEF.colored(f"OK [{pt_feasibility_OK} safe pt]{SEF.new_line}", "green", ["bold"])
            return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{name['opt_sol']}` è ammissibile."+SEF.colored(f"{SEF.new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo o meno.)", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)
        feedback_summary += f"ammissibilità della soluzione in {name['opt_sol']}: "+SEF.colored(f"OK{SEF.new_line}", "green", ["bold"])
        if 'opt_val' in goals:
            if sum_valori != answ['opt_val']:
                feedback_summary += f"autoconsistenza: "+SEF.colored(f"NO{SEF.new_line}", "red", ["bold"])
                return SEF.evaluation_format(task_number, feedback_summary, f"Il valore della soluzione immessa in `{name['opt_sol']}` è {sum_valori}, non {answ['opt_val']} come hai immesso in `{name['opt_val']}`. La soluzione (ammissibile) che hai immesso è {answ['opt_sol']}", pt_tot,pt_safe=pt_formato_OK,pt_out=pt_tot - pt_formato_OK)
            feedback_summary += f"{name['opt_val']}={answ['opt_val']} = somma dei valori su {name['opt_sol']}: "+SEF.colored(f"OK [{pt_feasibility_OK} safe pt]{SEF.new_line}", "green", ["bold"])
            if len(goals) <= 2:
                return SEF.evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{name['opt_sol']}` è ammissibile ed il suo valore corrisponde a quanto in `{name['opt_val']}`."+SEF.colored(f"{SEF.new_line}Nota:", "cyan", ["bold"])+" Ovviamente in sede di esame non posso dirti se sia anche ottimo o meno.", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)


            
feedback_dict = verif_submission(ENV["task"],ENV["pt_tot"],ENV["pt_formato_OK"],ENV["pt_feasibility_OK"], ENV["elementi"],ENV["pesi"],ENV["valori"],ENV["Knapsack_Capacity"],ENV["elementi_proibiti"],ENV["elementi_obbligati"],ENV["partialDPtable"], long_answer_dict=long_answer_dict )
#print(f"feedback_dict={feedback_dict}", file=stderr)

all_data = {"instance":instance_dict,"long_answer":long_answer_dict,"feedback":feedback_dict,"request":name_of}
#print(f"all_data={all_data}", file=stderr)
RO.checker_reply(all_data,ENV)
if ENV.LOG_FILES != None:
    all_data["oracle"] = solver(all_data)
    RO.checker_logs(all_data,ENV,TALf)
if ENV["yield_certificate_in_output_file"]:    
    RO.checker_certificates(all_data,ENV,TALf)


