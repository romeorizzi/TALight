#!/usr/bin/env python3
import RO_problems_lib as RO
      
def sum_of_pesi_over(ENV, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(ENV["pesi"], ENV["elementi"]) if ele in ordered_list_of_elems])

def sum_of_valori_over(ENV, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(ENV["valori"], ENV["elementi"]) if ele in ordered_list_of_elems])

def dict_of_oracle(ENV,opt_val, opt_sol, DPtable):
    oracle_dict = {}
    if ENV['sol_type'] in ['opt_sol','opt_sol_with_val','all']:
        oracle_dict['opt_sol'] = opt_sol
    if ENV['sol_type'] in ['opt_val','opt_sol_with_val','all']:
        oracle_dict['opt_val'] = opt_val
    if ENV['sol_type'] in ['DPtable','all']:
        oracle_dict['DPtable'] = DPtable
    return oracle_dict

def dict_of_input(ENV):
    dict_input = {}
    RO.add_ENV_vars(["elementi","pesi","valori","Knapsack_Capacity","sol_type"], dict_input, ENV)
    RO.add_ENV_vars(["elementi_proibiti","elementi_obbligati"], dict_input, ENV, lambda x : len(x) > 0)
    if ENV['sol_type'] in ['opt_sol','opt_sol_with_val','all']:
        RO.add_named_ENV_var('opt_sol', dict_input, ENV, lambda x : x is not None)
    if ENV['sol_type'] in ['opt_val','opt_sol_with_val','all']:
        RO.add_named_ENV_var('opt_val', dict_input, ENV, lambda x : x is not None)
    if ENV['sol_type'] in ['DPtable','all']:
        RO.add_named_ENV_var('DPtable', dict_input, ENV, lambda x : x is not None)
    return dict_input

def check_request_consistency(ENV):
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
    peso_elementi_obbligati = sum_of_pesi_over(ENV,ENV["elementi_obbligati"])
    if peso_elementi_obbligati > ENV["Knapsack_Capacity"]:
        print(f'Errore: il peso complessivo degli elementi obbligati ({peso_elementi_obbligati}) eccede la capacità dello zaino {ENV["Knapsack_Capacity"]}')    
        exit(0)

def solver(ENV):
    # the idea is to work over the reduced instance, where both the forced and the forbidden elements have been taken away from the table.
    Capacity=ENV["Knapsack_Capacity"] - sum_of_pesi_over(ENV,ENV["elementi_obbligati"])    
    elementi=[]
    pesi=[]
    valori=[]
    for ele,peso,val in zip(ENV["elementi"],ENV["pesi"],ENV["valori"]):
        if ele not in ENV["elementi_proibiti"] and ele not in ENV["elementi_obbligati"]:
            elementi.append(ele)
            pesi.append(peso)
            valori.append(val)

    n = len(elementi)    
    DPtable = [[0 for j in range(Capacity+1)] for i in range(n+1)] 
    for i in range(1,1+n):
        for j in range(Capacity+1):
            DPtable[i][j] = DPtable[i-1][j]
            if pesi[i-1] <= j and DPtable[i-1][j-pesi[i-1]] + valori[i-1] > DPtable[i][j]:
                DPtable[i][j] = DPtable[i-1][j-pesi[i-1]] + valori[i-1]
    opt_val=DPtable[i][j]
    promise = opt_val
    opt_sol = []
    while promise > 0:
        #print(f"\ni={i}\nj={j}\npromise={promise}\nelementi[i-1]={elementi[i-1]}\npesi[i-1]={pesi[i-1]}\nopt_sol={opt_sol}")
        if DPtable[i-1][j] < DPtable[i][j]:
            opt_sol.append(elementi[i-1])
            j -= pesi[i-1]
            assert j >= 0                
            promise -= valori[i-1]
        i -= 1
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nDPtable={DPtable}")
    return opt_val+sum_of_valori_over(ENV,ENV["elementi_obbligati"]), opt_sol+ENV["elementi_obbligati"], DPtable
