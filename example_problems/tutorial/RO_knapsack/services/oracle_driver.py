#!/usr/bin/env python3
from sys import exit

from tabulate import tabulate

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import knapsack_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('pwd',str),
    ('elementi','list_of_str'),
    ('pesi','list_of_int'),
    ('valori','list_of_int'),
    ('Knapsack_Capacity',int),
    ('elementi_proibiti','list_of_str'),
    ('elementi_obbligati','list_of_str'),
    ('sol_type',str),
    ('esercizio',int),
    ('task',int),
    ('name_of_opt_val',str),
    ('name_of_opt_sol',str),
    ('name_of_DPtable',str),
    ('as_yaml',bool),
    ('with_opening_message',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, "None")
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

def check_access_rights():
    if ENV["pwd"] != 'tmppwd':
        print(f'Password di accesso non corretta (password immessa: `{ENV["pwd"]}`)')
        exit(0)    

    if ENV.LOG_FILES == None:
        print("Il servizio è stato chiamato senza access token. Modalità attualmente non consentita.")
        exit(0)    
    else:
        TALf.str2log_file(content="Questo log file intende consentire il tracciamento dell'utente che ha chiamato il servizio.", filename='ORACLE_CALL', timestamped = False)

def check_request_consistency():
    if len(ENV["elementi"])!=len(ENV["pesi"]):
        print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["pesi"])}=len(ENV["pesi"])')    
        exit(0)
    if len(ENV["elementi"])!=len(ENV["valori"]):
        print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["valori"])}=len(ENV["valori"])')    
        exit(0)
    for ele in ENV["elementi_obbligati"]:
        if ele not in ENV["elementi"]:
            print(f'Errore: the element {ele} containd in the list `elementi_obbligati` is not contained in tje list `elementi` = {ENV["elementi"]}.\nIndeed, `elementi_obbligati` = {ENV["elementi_obbligati"]}.')
            exit(0)
    for ele in ENV["elementi_proibiti"]:
        if ele not in ENV["elementi"]:
            print(f'Errore: the element {ele} containd in the list `elementi_proibiti` is not contained in tje list `elementi` = {ENV["elementi"]}.\nIndeed, `elementi_proibiti` = {ENV["elementi_proibiti"]}.')
            exit(0)
        if ele in ENV["elementi_obbligati"]:
            print(f'Errore: the element {ele} is containd BOTH in the list `elementi_proibiti` and in the list `elementi_obbligati` = {ENV["elementi_obbligati"]}.\nIndeed, `elementi_proibiti` = {ENV["elementi_proibiti"]}.')
            exit(0)

            
check_access_rights()
check_request_consistency()
            
elementi=[]
pesi=[]
valori=[]
opt_val = 0
opt_sol=[]
cur_weight = 0
for ele,peso,val in zip(ENV["elementi"],ENV["pesi"],ENV["valori"]):
    if ele in ENV["elementi_obbligati"]:
        opt_val += peso
        opt_sol.append(ele)
        cur_weight += peso
    elif ele not in ENV["elementi_proibiti"]:
        elementi.append(ele)
        pesi.append(peso)
        valori.append(val)
        
opt_val_reduced_prob, opt_sol_reduced_prob, DPtable = knapsack_lib.solver(elementi,pesi,valori,ENV["Knapsack_Capacity"] - cur_weight)
opt_val += opt_val_reduced_prob
opt_sol += opt_sol_reduced_prob

call_data = {'feedback': {}, 'input': { 'elementi':ENV["elementi"],'elementi_proibiti':ENV["elementi_proibiti"],'elementi_obbligati':ENV["elementi_obbligati"],'pesi':ENV["pesi"],'valori':ENV["valori"],'Knapsack_Capacity':ENV["Knapsack_Capacity"], 'sol_type' : ENV['sol_type'] } }
if ENV['sol_type'] in ['opt_sol','opt_sol_with_val','all']:
    call_data['feedback']['opt_sol'] = opt_sol
if ENV['sol_type'] in ['opt_val','opt_sol_with_val','all']:
    call_data['feedback']['opt_val'] = opt_val
if ENV['sol_type'] in ['DPtable','all']:
    call_data['feedback']['DPtable'] = DPtable


if ENV['as_yaml']:
    print(call_data['feedback'])
else:
    for key,val in call_data['feedback'].items():
        print(f"{key}: {val}")


