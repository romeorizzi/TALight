#!/usr/bin/env python3
from sys import stderr
      
def sum_of_costs_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["costs"], instance["labels"]) if ele in ordered_list_of_elems])

def sum_of_vals_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["vals"], instance["labels"]) if ele in ordered_list_of_elems])

def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    if len(instance["labels"])!=len(instance["costs"]):
        print(f'Errore: {len(instance["labels"])=} != {len(instance["costs"])}=len(instance["costs"])')    
        exit(0)
    if len(instance["labels"])!=len(instance["vals"]):
        print(f'Errore: {len(instance["labels"])=} != {len(instance["vals"])}=len(instance["vals"])')    
        exit(0)
    for ele in instance["forced_in"]:
        if ele not in instance["labels"]:
            print(f'Errore: the element {ele} containd in the list `forced_in` is not contained in the list `labels` = {instance["labels"]}.\nIndeed, `forced_in` = {instance["forced_in"]}.')
            exit(0)
    for ele in instance["forced_out"]:
        if ele not in instance["labels"]:
            print(f'Errore: the element {ele} containd in the list `forced_out` is not contained in the list `labels` = {instance["labels"]}.\nIndeed, `forced_out` = {instance["forced_out"]}.')
            exit(0)
        if ele in instance["forced_in"]:
            print(f'Errore: the element {ele} is containd BOTH in the list `forced_out` and in the list `forced_in` = {instance["forced_in"]}.\nIndeed, `forced_out` = {instance["forced_out"]}.')
            exit(0)
    peso_forced_in = sum_of_costs_over(instance,instance["forced_in"])
    if peso_forced_in > instance["Knapsack_Capacity"]:
        print(f'Errore: il peso complessivo degli elementi obbligati ({peso_forced_in}) eccede la capacità dello zaino {instance["Knapsack_Capacity"]}')    
        exit(0)

        
def solver(input_to_oracle):
    I = input_to_oracle["instance"]
    #print(f"Instance={I}")
    # the idea is to work over a reduced instance, where both the forced and the forbidden elements have been taken away from the table.
    Capacity=I["Knapsack_Capacity"] - sum_of_costs_over(I,I["forced_in"])    
    labels=[]
    costs=[]
    vals=[]
    for ele,peso,val in zip(I["labels"],I["costs"],I["vals"]):
        if ele not in I["forced_out"] and ele not in I["forced_in"]:
            labels.append(ele)
            costs.append(peso)
            vals.append(val)

    n = len(labels)
    DPtable_opt_val = [[0 for j in range(Capacity+1)] for i in range(n+1)]
    for i in range(1,1+n):
        for j in range(Capacity+1):
            DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j]
            if costs[i-1] <= j and DPtable_opt_val[i-1][j-costs[i-1]] + vals[i-1] > DPtable_opt_val[i][j]:
                DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j-costs[i-1]] + vals[i-1]
    if n == 0:
        opt_val = 0
    else:
        opt_val=DPtable_opt_val[i][j]
    promise = opt_val
    opt_sol = []
    while promise > 0:
        #print(f"\ni={i}\nj={j}\npromise={promise}\nlabels[i-1]={labels[i-1]}\ncosts[i-1]={costs[i-1]}\nopt_sol={opt_sol}", file=stderr)
        if DPtable_opt_val[i-1][j] < DPtable_opt_val[i][j]:
            opt_sol.append(labels[i-1])
            j -= costs[i-1]
            assert j >= 0                
            promise -= vals[i-1]
        i -= 1
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nDPtable_opt_val={DPtable_opt_val}", file=stderr)
    opt_val += sum_of_vals_over(I,I["forced_in"])
    opt_sol += I["forced_in"]
    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers
