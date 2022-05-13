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
    ('elementi_obbligati','list_of_str'),
    ('sol_type',str),
    ('esercizio',int),
    ('task',int),
    ('name_of_opt_val',str),
    ('name_of_opt_sol',str),
    ('name_of_DPtable',str),
    ('color_implementation',str),
    ('as_yaml',bool),
    ('with_output_files',bool),
    ('with_opening_message',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if len(ENV["elementi"])!=len(ENV["pesi"]):
    print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["pesi"])}=len(ENV["pesi"])')    
    exit(0)
if len(ENV["elementi"])!=len(ENV["valori"]):
    print(f'Errore: {len(ENV["elementi"])=} != {len(ENV["valori"])}=len(ENV["valori"])')    
    exit(0)
    
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
opt_val_reduced_prob, opt_sol_reduced_prob, DPtable = knapsack_lib.solver(elementi,pesi,valori,ENV["Knapsack_Capacity"])
opt_val += opt_val_reduced_prob
opt_sol += opt_sol
if ENV['as_yaml']:
    summary_of_service_call = {'elementi':ENV["elementi"],'elementi_proibiti':ENV["elementi_proibiti"],'elementi_obbligati':ENV["elementi_obbligati"],'pesi':ENV["pesi"],'valori':ENV["valori"],'Knapsack_Capacity':ENV["Knapsack_Capacity"]}
    print({'opt_val':opt_val, 'opt_sol':opt_sol, 'DPtable':DPtable,
           'input': summary_of_service_call })
else:
    if ENV['sol_type'] in ['opt_sol','opt_sol_with_val','all']:
        print(f"opt_sol: {opt_sol}")
    if ENV['sol_type'] in ['opt_val','opt_sol_with_val','all']:
        print(f"opt_val: {opt_val}")
    if ENV['sol_type'] in ['DPtable','all']:
        print(f"DPtable: {DPtable}")

    print(f"\nSUMMARY OF THIS SERVICE CALL:")    
    print(f'elementi: {ENV["elementi"]}')
    if len(ENV["elementi_proibiti"]) > 0:
        print(f'elementi_proibiti: {ENV["elementi_proibiti"]}')
    if len(ENV["elementi_obbligati"]) > 0:
        print(f'elementi_obbligati: {ENV["elementi_obbligati"]}')
    if len(ENV["elementi_proibiti"] + ENV["elementi_proibiti"]) > 0:
        print(f'elementi_effettivi: {elementi}')
    print(f'pesi: {ENV["pesi"]}')
    print(f'valori: {ENV["valori"]}')
    print(f'Knapsack_Capacity: {ENV["Knapsack_Capacity"]}')
    print(f'sol_type: {ENV["sol_type"]}')
    print(f'color_implementation: {ENV["color_implementation"]}')
    print(f'with_opening_message: {ENV["with_opening_message"]}')

if ENV.LOG_FILES == None:
    print("Servizio chiamato senza access token")
else:
    print("Servizio chiamato con access token")
    TALf.str2log_file(content='Scrivo questo in un file di log.', filename=f'LOG_filename', timestamped = False)

if ENV["with_output_files"]:    
    print("Al servizio è stato richiesto di generare files nel folder di output")
    TALf.str2output_file(content='Scrivo questo in un output file.', filename=f'OK_{ENV["instance_id"]}', timestamped = False)
else:
    print("Al servizio non è stato richiesto di generare files nel folder di output")

if TALf.exists_input_file('optional_filehandler1'):
    file1_content_as_string = TALf.input_file_as_str('optional_filehandler1')
    print(f"You passed a file on `optional_filehandler1` and here is its content:\nBEGIN\n{file1_content_as_string}END")
else:
    print(f"You passed no file on `optional_filehandler1`")

