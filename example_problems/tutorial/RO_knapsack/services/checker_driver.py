#!/usr/bin/env python3
from sys import exit

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
    ('var_name_of_answ_opt_val',str),
    ('var_name_of_answ_opt_sol',str),
    ('var_name_of_answ_DPtable',str),
    ('color_implementation',str),
    ('with_output_files',bool),
    ('with_opening_message',bool),
    ('with_summary',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

def evaluation_format(feedback_summary,feedback_message, pt_tot,pt_safe,pt_out, index_pt=None):
    global safe_points
    global maybe_points
    pt_maybe = pt_tot-pt_out-(pt_safe if pt_safe != None else 0)
    safe_points = pt_safe
    maybe_points = pt_maybe
    code_for_jupyter_commented = """
    if TAc.color_implementation == 'html':
        return f"{feedback_summary}<br>Totalizzi <span style='color:green'>[punti sicuri: {pt_safe}]</span>, <span style='color:blue'>[punti aggiuntivi possibili: {pt_maybe}]</span>, <span style='color:red'>[punti fuori portata: {pt_out}]</span>.<br><span style='color:cyan'>Spiegazione: </span>{feedback_message}<br>"
    """
    ret_str = feedback_summary + "Totalizzi "
    ret_str += TAc.colored(f"[punti sicuri: {pt_safe}]", "green", ["bold"]) + ", "
    ret_str += TAc.colored(f"[punti aggiuntivi possibili: {pt_maybe}]", "blue", ["bold"]) + ", " 
    ret_str += TAc.colored(f"[punti fuori portata: {pt_out}]", "red", ["bold"]) + TAc.colored("\nSpiegazione: ", "cyan", ["bold"]) + feedback_message + TAc.colored("\n")    
    return ret_str


def verif_knapsack(elementi,pesi,valori,Capacity, answer, pt_formato_OK,pt_feasibility_OK,pt_tot, index_pt):
    feedback_summary = ""
    if answer['sol_type'] in ["opt_val","opt_sol_and_val"]:
        if type(answer['opt_val']) != int:
            feedback_summary += f"formato di {ENV['var_name_of_answ_opt_val']}: "+TAc.colored("NO\n", "red", ["bold"])
            return evaluation_format(feedback_summary, f"Come `{ENV['var_name_of_answ_opt_val']}` hai immesso `{answer['opt_val']}` dove era invece richiesto di immettere un intero.", pt_tot,pt_safe=None,pt_out=pt_tot, index_pt=index_pt)
        if answer['sol_type'] == "opt_val":
            feedback_summary += f"formato di {ENV['var_name_of_answ_opt_val']}: "+TAc.colored(f"OK [{pt_formato_OK} safe pt]\n", "green", ["bold"])
            return evaluation_format(feedback_summary, f"Come `{ENV['var_name_of_answ_opt_val']}` hai immesso un intero come richiesto."+TAc.colored("\nNota:", "cyan", ["bold"])+"Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.", pt_tot,pt_safe=pt_formato_OK,pt_out=0, index_pt=index_pt)
        else:
            feedback_summary += f"formato di {ENV['var_name_of_answ_opt_val']}: "+TAc.colored("OK\n", "green", ["bold"])

    if answer['sol_type'] in ["opt_sol","opt_sol_and_val"]:
        if type(answer['opt_sol']) != list:
            feedback_summary += f"formato di {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored("NO\n", "red", ["bold"])
            return evaluation_format(feedback_summary, f"Come `{ENV['var_name_of_answ_opt_sol']}` è richiesto si inserisca una lista di oggetti (esempio ['{elementi[0]}','{elementi[2]}']). Hai invece immesso `{answer['opt_sol']}`.", pt_tot,pt_safe=None,pt_out=pt_tot, index_pt=index_pt)
        else:
            sum_valori=0
            sum_pesi=0
            for ele in answer['opt_sol']:
                if ele not in elementi:
                    feedback_summary += f"formato di {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored("NO\n", "red", ["bold"])
                    return evaluation_format(feedback_summary, f"Ogni elemento che collochi nella lista `{ENV['var_name_of_answ_opt_sol']}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {elementi}.", pt_tot,pt_safe=None,pt_out=pt_tot, index_pt=index_pt)
                index_of_ele = elementi.index(ele)
                sum_valori += valori[index_of_ele]
                sum_pesi += pesi[index_of_ele]
            feedback_summary += f"formato di {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored(f"OK [{pt_formato_OK} safe pt]\n", "green", ["bold"])
            if sum_pesi > Capacity:
                feedback_summary += f"ammissibilità della soluzione in {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored("NO\n", "red", ["bold"])
                return evaluation_format(feedback_summary, f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda).", pt_tot,pt_safe=None,pt_out=pt_tot, index_pt=index_pt)
            feedback_summary += f"ammissibilità della soluzione in {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored(f"OK [{pt_feasibility_OK} safe pt]\n", "green", ["bold"])
            if answer['sol_type'] == "opt_sol":
                return evaluation_format(feedback_summary, f"Il sottoinsieme di elementi specificato in {ENV['var_name_of_answ_opt_sol']} è ammissibile."+TAc.colored("\nNota:", "cyan", ["bold"])+"Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo o meno.)", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0, index_pt=index_pt)
            assert answer['sol_type'] == "opt_sol_and_val"
            if sum_valori > answer['opt_val']:
                feedback_summary += f"{ENV['var_name_of_answ_opt_val']}={answer['opt_val']}<{sum_valori}, che è la somma dei valori su {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored(f"NO\n", "red", ["bold"])
            if sum_valori < answer['opt_val']:
                feedback_summary += f"{ENV['var_name_of_answ_opt_val']}={answer['opt_val']}>{sum_valori}, che è la somma dei valori su {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored(f"NO\n", "red", ["bold"])
            if sum_valori != answer['opt_val']:
                return evaluation_format(feedback_summary, f"Il valore della soluzione immessa è {sum_valori} e non {answer['opt_val']} come hai immesso in `{ENV['var_name_of_answ_opt_val']}`. A mè risulta che la soluzione (ammissibile) che hai immesso sia {answer['opt_sol']}.", pt_tot,pt_safe=pt_formato_OK,pt_out=pt_tot - pt_formato_OK, index_pt=index_pt)
            else:
                feedback_summary += f"{ENV['var_name_of_answ_opt_val']}={answer['opt_val']} = somma dei valori su {ENV['var_name_of_answ_opt_sol']}: "+TAc.colored(f"OK\n", "green", ["bold"])
                return evaluation_format(feedback_summary, f"Il sottoinsieme di elementi specificato in `{ENV['var_name_of_answ_opt_sol']}` è ammissibile ed il suo valore corrisponde a quanto in `{ENV['var_name_of_answ_opt_val']}`."+TAc.colored("\nNota: ", "cyan", ["bold"])+"Ovviamente in sede di esame non posso dirti se sia anche ottimo o meno.", pt_tot,pt_safe=pt_formato_OK + pt_feasibility_OK,pt_out=0, index_pt=index_pt)

            
if len(ENV["elementi"])!=len(ENV["pesi"]):
    print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["pesi"])}=len(ENV["pesi"])')    
    exit(0)
if len(ENV["elementi"])!=len(ENV["valori"]):
    print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["valori"])}=len(ENV["valori"])')    
    exit(0)
elementi=[]
pesi=[]
valori=[]
for ele,peso,val in zip(ENV["elementi"],ENV["pesi"],ENV["valori"]):
    if ele not in ENV["elementi_proibiti"]:
        elementi.append(ele)
        pesi.append(peso)
        valori.append(val)

student_answer = {'sol_type':ENV["sol_type"],'opt_sol':ENV["opt_sol"],'opt_val':ENV["opt_val"],'DPtable':ENV["DPtable"] }
feedback_string = verif_knapsack(elementi,pesi,valori,ENV["Knapsack_Capacity"], student_answer, ENV["pt_formato_OK"],ENV["pt_feasibility_OK"],ENV["pt_tot"], index_pt=None)
print(feedback_string)

summary=f"""
SUMMARY OF THIS SERVICE CALL: 
elementi: {ENV["elementi"]}
if len(ENV["elementi_proibiti"]) > 0:
    print(f'elementi_proibiti: {ENV["elementi_proibiti"]}')
    print(f'elementi_effettivi: {elementi}')
pesi: {ENV["pesi"]}
valori: {ENV["valori"]}
Knapsack_Capacity: {ENV["Knapsack_Capacity"]}
sol_type: {ENV["sol_type"]}
"""
if ENV["sol_type"] in ['opt_sol', 'opt_val_and_sol']:
    summary += f'opt_sol: {ENV["opt_sol"]}\n'
    summary += f'var_name_of_answ_opt_sol: {ENV["var_name_of_answ_opt_sol"]}\n'
if ENV["sol_type"] in ['opt_val', 'opt_val_and_sol']:
    summary += f'opt_val: {ENV["opt_val"]}\n'
    summary += f'var_name_of_answ_opt_val: {ENV["var_name_of_answ_opt_val"]}\n'
if ENV["sol_type"] in ['DPtable']:
    summary += f'DPtable: {ENV["DPtable"]}\n'
    summary += f'var_name_of_answ_DPtable: {ENV["var_name_of_answ_DPtable"]}\n'
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
    TALf.str2log_file(content=feedback_string+summary, filename=f'problem_{ENV["problem"]}_task_{ENV["task"]}_safe_{safe_points}_maybe_{maybe_points}', timestamped = False)

if ENV["with_output_files"]:    
    TALf.str2output_file(content=feedback_string+summary, filename=f'problem_{ENV["problem"]}_task_{ENV["task"]}_safe_{safe_points}_maybe_{maybe_points}', timestamped = False)

if ENV["with_summary"]:
    print(summary)

