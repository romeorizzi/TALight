#!/usr/bin/env python3
from sys import exit

import copy
from tabulate import tabulate

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('elementi','list_of_str'),
    ('pesi','list_of_int'),
    ('valori','list_of_int'),
    ('Knapsack_Capacity',int),
    ('sol_type',str),
    ('sol','list_of_str'),
    ('val',int),
    ('DPtable','matrix_of_int'),
    ('caller',str),
    ('with_output_files',bool),
    ('with_opening_message',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

def evaluation_format(answ, pt_green,pt_red, index_pt):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    # arr_point[index_pt]=pt_green
    # file = open("points.txt", "w")
    # file.write(str(arr_point))
    # file.close()
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"

def verif_knapsack(elementi,pesi, valori, Capacity,answer,pt_green,pt_red, index_pt, sol_type="sol",edr=False):
    elementi2=copy.deepcopy(elementi)
    pesi2=copy.deepcopy(pesi)
    valori2=copy.deepcopy(valori)
    if edr!=False:
        for elemento in edr:
            i=elementi2.index(elemento)
            elementi2.pop(i)
            pesi2.pop(i)
            valori2.pop(i)
        
    n = len(pesi2)
    S = [[0 for j in range(Capacity+1)] for i in range(n)] 
    for i in range(1,n):
        for j in range(Capacity+1):
            S[i][j] = S[i-1][j]
            if pesi2[i] <= j and S[i-1][j-pesi2[i]] + valori2[i] > S[i][j]:
                S[i][j] = S[i-1][j-pesi2[i]] + valori2[i]
    max_val=S[-1][-1]
    if sol_type=="val":
        if type(answer)==int:
            return evaluation_format("Si", 1,pt_red,index_pt)+"Hai immesso un intero come richiesto. (Ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto.)"
        else:
            return evaluation_format("No", 0,pt_red,index_pt)+"A questa domanda è richiesto si risponda con un intero."
    if sol_type=="sol":
        if type(answer)==list:
            sum_valori=0
            sum_pesi=0
            for i in range(len(answer)):
                sum_valori+=valori2[elementi.index(answer[i])]
                sum_pesi+=pesi2[elementi.index(answer[i])]
            if sum_pesi<=Capacity:
                return evaluation_format("Si", 1,pt_red,index_pt)+"Il sottoinsieme di elementi è ammissibile. (Ovviamente durante lo svolgimento dell'esame non posso dirti se sia anche ottimo.)"
            else:
                return evaluation_format("No", 0,pt_red,index_pt)+f"Il sottoinsieme di elementi NON è ammissibile in quanto la somma dei loro pesi è {sum_pesi}>{Capacity} (ossia supera la capacità dello zaino per questa domanda)."
        else:
            return evaluation_format("No", 0,pt_red,index_pt)+"A questa domanda è richiesto si risponda con una lista di oggetti (esempio ['B','D'])."    

if ENV["with_opening_message"]:
    TAc.print(LANG.render_feedback("ciao", 'Ciao.'), "yellow", ["bold"])
    print(f'{ENV["elementi"]=}')
    print(f'{ENV["pesi"]=}')
    print(f'{ENV["valori"]=}')
    print(f'{ENV["Knapsack_Capacity"]=}')
    print(f'{ENV["sol_type"]=}')
    if ENV["sol_type"] in ['sol', 'val_and_sol']:
        print(f'{ENV["sol"]=}')
    if ENV["sol_type"] in ['val', 'val_and_sol']:
        print(f'{ENV["val"]=}')
    if ENV["sol_type"] in ['DPtable']:
        print(f'{ENV["DPtable"]=}')
    print(f'{ENV["caller"]=}')
    print(f'{ENV["with_opening_message"]=}')

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


if ENV["sol_type"] in ['sol', 'val_and_sol']:
    print(verif_knapsack(ENV["elementi"],ENV["pesi"],ENV["valori"],ENV["Knapsack_Capacity"],ENV["sol"], pt_green=1, pt_red=5, index_pt=0, sol_type=ENV["sol_type"]))
