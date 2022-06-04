#!/usr/bin/env python3
from sys import stderr
import RO_problems_lib as RO
      
def dict_of_instance(ENV):
    dict_input = {}
    RO.add_ENV_vars(["elementi","pesi","valori","Knapsack_Capacity","elementi_proibiti","elementi_obbligati","partialDPtable"], dict_input, ENV)
    return dict_input

def sum_of_pesi_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["pesi"], instance["elementi"]) if ele in ordered_list_of_elems])

def sum_of_valori_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["valori"], instance["elementi"]) if ele in ordered_list_of_elems])

def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    if len(instance["elementi"])!=len(instance["pesi"]):
        print(f'Errore: {len(instance["elementi"])=} != {len(instance["pesi"])}=len(instance["pesi"])')    
        exit(0)
    if len(instance["elementi"])!=len(instance["valori"]):
        print(f'Errore: {len(instance["elementi"])=} != {len(instance["valori"])}=len(instance["valori"])')    
        exit(0)
    for ele in instance["elementi_obbligati"]:
        if ele not in instance["elementi"]:
            print(f'Errore: the element {ele} containd in the list `elementi_obbligati` is not contained in the list `elementi` = {instance["elementi"]}.\nIndeed, `elementi_obbligati` = {instance["elementi_obbligati"]}.')
            exit(0)
    for ele in instance["elementi_proibiti"]:
        if ele not in instance["elementi"]:
            print(f'Errore: the element {ele} containd in the list `elementi_proibiti` is not contained in the list `elementi` = {instance["elementi"]}.\nIndeed, `elementi_proibiti` = {instance["elementi_proibiti"]}.')
            exit(0)
        if ele in instance["elementi_obbligati"]:
            print(f'Errore: the element {ele} is containd BOTH in the list `elementi_proibiti` and in the list `elementi_obbligati` = {instance["elementi_obbligati"]}.\nIndeed, `elementi_proibiti` = {instance["elementi_proibiti"]}.')
            exit(0)
    peso_elementi_obbligati = sum_of_pesi_over(instance,instance["elementi_obbligati"])
    if peso_elementi_obbligati > instance["Knapsack_Capacity"]:
        print(f'Errore: il peso complessivo degli elementi obbligati ({peso_elementi_obbligati}) eccede la capacità dello zaino {instance["Knapsack_Capacity"]}')    
        exit(0)

        
def solver(input_to_oracle):
    inst = input_to_oracle["instance"]
    # the idea is to work over a reduced instance, where both the forced and the forbidden elements have been taken away from the table.
    Capacity=inst["Knapsack_Capacity"] - sum_of_pesi_over(inst,inst["elementi_obbligati"])    
    elementi=[]
    pesi=[]
    valori=[]
    for ele,peso,val in zip(inst["elementi"],inst["pesi"],inst["valori"]):
        if ele not in inst["elementi_proibiti"] and ele not in inst["elementi_obbligati"]:
            elementi.append(ele)
            pesi.append(peso)
            valori.append(val)

    n = len(elementi)    
    DPtable_opt_val = [[0 for j in range(Capacity+1)] for i in range(n+1)] 
    for i in range(1,1+n):
        for j in range(Capacity+1):
            DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j]
            if pesi[i-1] <= j and DPtable_opt_val[i-1][j-pesi[i-1]] + valori[i-1] > DPtable_opt_val[i][j]:
                DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j-pesi[i-1]] + valori[i-1]
    opt_val=DPtable_opt_val[i][j]
    promise = opt_val
    opt_sol = []
    while promise > 0:
        #print(f"\ni={i}\nj={j}\npromise={promise}\nelementi[i-1]={elementi[i-1]}\npesi[i-1]={pesi[i-1]}\nopt_sol={opt_sol}", file=stderr)
        if DPtable_opt_val[i-1][j] < DPtable_opt_val[i][j]:
            opt_sol.append(elementi[i-1])
            j -= pesi[i-1]
            assert j >= 0                
            promise -= valori[i-1]
        i -= 1
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nDPtable_opt_val={DPtable_opt_val}", file=stderr)
    opt_val += sum_of_valori_over(inst,inst["elementi_obbligati"])
    opt_sol += inst["elementi_obbligati"]
    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers
