#!/usr/bin/env python3
from sys import exit
from typing import Optional, List

from tabulate import tabulate

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import knapsack_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('elementi','list_of_str'),
    ('pesi','list_of_int'),
    ('valori','list_of_int'),
    ('Knapsack_Capacity',int),
    ('elementi_proibiti','list_of_str'),
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
    ('get_yaml',bool),
    ('with_output_files',bool),
    ('with_opening_message',bool),
    ('with_summary',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

def evaluation_format(task_number, feedback_summary,feedback_message, pt_tot:int,pt_safe:Optional[int] = None,pt_out:Optional[int] = None):
    pt_maybe = pt_tot-(pt_safe if pt_safe != None else 0)-(pt_out if pt_out != None else 0)
    index_pt=task_number-1
    new_line = '\n'
    ret_str = feedback_summary + "Totalizzi "
    ret_str += TAc.colored(f"[punti sicuri: {pt_safe}]", "green", ["bold"]) + ", "
    ret_str += TAc.colored(f"[punti aggiuntivi possibili: {pt_maybe}]", "blue", ["bold"]) + ", " 
    ret_str += TAc.colored(f"[punti fuori portata: {pt_out}]", "red", ["bold"]) + TAc.colored(f"{new_line}Spiegazione: ", "cyan", ["bold"]) + feedback_message + TAc.colored(f"{new_line}")
    if pt_safe == None:
        pt_safe = 0
    if pt_out == None:
        pt_out = 0
    return ret_str, pt_safe,pt_maybe,pt_out

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
            feedback_summary += f"formato di {answ['name_of_opt_val']}: "+TAc.colored(f"NO{new_line}", "red", ["bold"])
            return evaluation_format(task_number, feedback_summary, f"Come `{answ['name_of_opt_val']}` hai immesso `{answ['opt_val']}` dove era invece richiesto di immettere un intero.", pt_tot,pt_safe=None,pt_out=pt_tot)
        if answ['sol_type'] == "opt_val":
            feedback_summary += f"formato di {answ['name_of_opt_val']}: "+TAc.colored(f"OK [{pt_formato_OK} safe pt]{new_line}", "green", ["bold"])
            return evaluation_format(task_number, feedback_summary, f"Come `{answ['name_of_opt_val']}` hai immesso un intero come richiesto."+TAc.colored(f"{new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.", pt_tot,pt_safe=pt_formato_OK,pt_out=0)
        else:
            feedback_summary += f"formato di {answ['name_of_opt_val']}: "+TAc.colored(f"OK{new_line}", "green", ["bold"])

    if answ['sol_type'] in ["opt_sol","opt_sol_with_val"]:
        if type(answ['opt_sol']) != list:
            feedback_summary += f"formato di {answ['name_of_opt_sol']}: "+TAc.colored(f"NO{new_line}", "red", ["bold"])
            return evaluation_format(task_number, feedback_summary, f"Come `{answ['name_of_opt_sol']}` è richiesto si inserisca una lista di oggetti (esempio ['{elementi[0]}','{elementi[2]}']). Hai invece immesso `{answ['opt_sol']}`.", pt_tot,pt_safe=None,pt_out=pt_tot)
        else:
            sum_valori=0
            sum_pesi=0
            for ele in answ['opt_sol']:
                if ele not in elementi:
                    feedback_summary += f"formato di {answ['name_of_opt_sol']}: "+TAc.colored(f"NO{new_line}", "red", ["bold"])
                    return evaluation_format(task_number, feedback_summary, f"Ogni elemento che collochi nella lista `{answ['name_of_opt_sol']}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {elementi}.", pt_tot,pt_safe=None,pt_out=pt_tot)
                index_of_ele = elementi.index(ele)
                sum_valori += valori[index_of_ele]
                sum_pesi += pesi[index_of_ele]
            feedback_summary += f"formato di {answ['name_of_opt_sol']}: "+TAc.colored(f"OK [{pt_formato_OK} safe pt]{new_line}", "green", ["bold"])
            if sum_pesi > Capacity:
                feedback_summary += f"ammissibilità della soluzione in {answ['name_of_opt_sol']}: "+TAc.colored(f"NO{new_line}", "red", ["bold"])
                return evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda).", pt_tot,pt_safe=None,pt_out=pt_tot)
            feedback_summary += f"ammissibilità della soluzione in {answ['name_of_opt_sol']}: "+TAc.colored(f"OK [{pt_feasibility_OK} safe pt]{new_line}", "green", ["bold"])
            if answ['sol_type'] == "opt_sol":
                return evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in {answ['name_of_opt_sol']} è ammissibile."+TAc.colored(f"{new_line}Nota:", "cyan", ["bold"])+" Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo o meno.)", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)
            assert answ['sol_type'] == "opt_sol_with_val"
            if sum_valori > answ['opt_val']:
                feedback_summary += f"{answ['name_of_opt_val']}={answ['opt_val']}<{sum_valori}, che è la somma dei valori su {answ['name_of_opt_sol']}: "+TAc.colored(f"NO{new_line}", "red", ["bold"])
            if sum_valori < answ['opt_val']:
                feedback_summary += f"{answ['name_of_opt_val']}={answ['opt_val']}>{sum_valori}, che è la somma dei valori su {answ['name_of_opt_sol']}: "+TAc.colored(f"NO{new_line}", "red", ["bold"])
            if sum_valori != answ['opt_val']:
                return evaluation_format(task_number, feedback_summary, f"Il valore della soluzione immessa è {sum_valori} e non {answ['opt_val']} come hai immesso in `{answ['name_of_opt_val']}`. A mè risulta che la soluzione (ammissibile) che hai immesso sia {answ['opt_sol']}.", pt_tot,pt_safe=pt_formato_OK,pt_out=pt_tot - pt_formato_OK)
            else:
                feedback_summary += f"{answ['name_of_opt_val']}={answ['opt_val']} = somma dei valori su {answ['name_of_opt_sol']}: "+TAc.colored(f"OK{new_line}", "green", ["bold"])
                return evaluation_format(task_number, feedback_summary, f"Il sottoinsieme di elementi specificato in `{answ['name_of_opt_sol']}` è ammissibile ed il suo valore corrisponde a quanto in `{answ['name_of_opt_val']}`."+TAc.colored(f"{new_line}Nota:", "cyan", ["bold"])+" Ovviamente in sede di esame non posso dirti se sia anche ottimo o meno.", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0)

            
if len(ENV["elementi"])!=len(ENV["pesi"]):
    print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["pesi"])}=len(ENV["pesi"])')    
    exit(0)
if len(ENV["elementi"])!=len(ENV["valori"]):
    print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["valori"])}=len(ENV["valori"])')    
    exit(0)

feedback_string, pt_safe,pt_maybe,pt_out = verif_knapsack(ENV["task"],ENV["elementi"],ENV["pesi"],ENV["valori"],ENV["Knapsack_Capacity"], \
                                answ={"sol_type":ENV["sol_type"],"opt_sol":ENV["opt_sol"],"opt_val":ENV["opt_val"],"DPtable":ENV["DPtable"], \
                                      "name_of_opt_sol":ENV["name_of_opt_sol"], "name_of_opt_val":ENV["name_of_opt_val"], "name_of_DPtable":ENV["name_of_DPtable"]}, \
                                 pt_tot=ENV["pt_tot"],pt_formato_OK=ENV["pt_formato_OK"],pt_feasibility_OK=ENV["pt_feasibility_OK"],elementi_proibiti=ENV["elementi_proibiti"])
if ENV['get_yaml']:
    print({'pt_safe':pt_safe,'pt_maybe':pt_maybe,'pt_out':pt_out,'feedback_string':feedback_string})
else:
    print(feedback_string)

summary=f"""
SUMMARY OF THIS SERVICE CALL: 
elementi: {ENV["elementi"]}
if len(ENV["elementi_proibiti"]) > 0:
    print(f'elementi_proibiti: {ENV["elementi_proibiti"]}')
pesi: {ENV["pesi"]}
valori: {ENV["valori"]}
Knapsack_Capacity: {ENV["Knapsack_Capacity"]}
sol_type: {ENV["sol_type"]}
"""
if ENV["sol_type"] in ['opt_sol', 'opt_sol_with_val']:
    summary += f'opt_sol: {ENV["opt_sol"]}\n'
    summary += f'name_of_opt_sol: {ENV["name_of_opt_sol"]}\n'
if ENV["sol_type"] in ['opt_val', 'opt_sol_with_val']:
    summary += f'opt_val: {ENV["opt_val"]}\n'
    summary += f'name_of_opt_val: {ENV["name_of_opt_val"]}\n'
if ENV["sol_type"] in ['DPtable']:
    summary += f'DPtable: {ENV["DPtable"]}\n'
    summary += f'name_of_DPtable: {ENV["name_of_DPtable"]}\n'
summary += f'color_implementation: {ENV["color_implementation"]}\n'
summary += f'with_opening_message: {ENV["with_opening_message"]}\n'

if ENV.LOG_FILES == None:
    summary += 'Servizio chiamato senza access token\n'
else:
    summary += 'Servizio chiamato con access token\n'

if ENV["with_output_files"]:    
    summary += 'Al servizio è stato richiesto di generare files nel folder di output\n'
else:
    summary += 'Al servizio non è stato richiesto di generare files nel folder di output\n'

if ENV.LOG_FILES != None:
    TALf.str2log_file(content=feedback_string+summary, filename=f'problem_{ENV["esercizio"]}_task_{ENV["task"]}_safe_{pt_safe}_maybe_{pt_maybe}', timestamped = False)

if ENV["with_output_files"]:    
    TALf.str2output_file(content=feedback_string+summary, filename=f'problem_{ENV["esercizio"]}_task_{ENV["task"]}_safe_{pt_safe}_maybe_{pt_maybe}', timestamped = False)

if ENV["with_summary"]:
    print(summary)

