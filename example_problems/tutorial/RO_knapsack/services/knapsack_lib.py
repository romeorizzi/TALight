#!/usr/bin/env python3
from sys import stderr

instance_objects_spec = [
    ('Knapsack_Capacity',int),
    ('labels','list_of_str'),
    ('costs','list_of_int'),
    ('vals','list_of_int'),
    ('LB','list_of_int'),
    ('UB','list_of_int'),
    ('forced_out','list_of_str'),
    ('forced_in','list_of_str'),
]
additional_infos_spec=[
    ('partialDPtable','matrix_of_int')
]
answer_objects_spec = {
    'opt_sol':'list_of_str',
    'opt_val':'int',
    'num_opt_sols':'int',
    'list_opt_sols':'list_of_list_of_str',
    'DPtable_opt_val':'matrix_of_int',
    'DPtable_num_opts':'matrix_of_int',
}
answer_objects_implemented = ['opt_sol','opt_val','num_opt_sols','DPtable_opt_val','DPtable_num_opts','list_opt_sols']
request_setups = {'MAX_NUM_SOLS_IN_LIST':10, 'MAX_NUM_OPT_SOLS_IN_LIST':30}

def sum_of_costs_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["costs"], instance["labels"]) if ele in ordered_list_of_elems])

def sum_of_vals_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["vals"], instance["labels"]) if ele in ordered_list_of_elems])

def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    n = len(instance["labels"]) 
    if len(instance["costs"]) != n:
        print(f'Errore: len(instance["costs"])={len(instance["costs"])} != {n}=len(instance["labels"])')    
        exit(0)
    if len(instance["vals"]) != n:
        print(f'Errore: len(instance["vals"])={len(instance["vals"])=} != {n}=len(instance["labels"])')    
        exit(0)
    for ele in instance["forced_in"]:
        if ele in instance["forced_in"]:
            print(f'Errore: the element {ele} containd in the list `forced_in` is not contained in the list `labels` = {instance["labels"]}.\nIndeed, `forced_in` = {instance["forced_in"]}.')
            exit(0)
    for ele in instance["forced_out"]:
        if ele not in instance["labels"]:
            print(f'Errore: the element {ele} containd in the list `forced_out` is not contained in the list `labels` = {instance["labels"]}.\nIndeed, `forced_out` = {instance["forced_out"]}.')
            exit(0)
        if ele in instance["forced_in"]:
            print(f'Errore: the element {ele} is containd BOTH in the list `forced_out` and in the list `forced_in` = {instance["forced_in"]}.\nIndeed, `forced_out` = {instance["forced_out"]}.')
            exit(0)
    LB = instance["LB"]
    UB = instance["UB"]
    if len(UB)+len(LB) > 0:
        if len(UB)*len(LB)==0:
            print(f'Errore: delle liste UB ed LB non puoi averne esattamente una vuota. O sono entrambe vuote o entrambe devono essere lunghe quanto la lista `labels`')
            exit(0)
        if len(forced_out)+len(forced_in) > 0:
            print(f'Errore: quando le liste `forced_out` e/o `forced_in` sono impostate a liste NON vuote le liste `UB` e `LB` devono essere lasciate vuote')    
            exit(0)
        if len(UB) != n:
            print(f'Errore: len(instance["UB"])={len(UB)=} != {n}=len(instance["labels"])')    
            exit(0)
        if len(LB) != n:
            print(f'Errore: len(instance["LB"])={len(LB)=} != {n}=len(instance["labels"])')    
            exit(0)
    else:
        LB = [0]*n
        UB = [1]*n        
    cost_forced_in = 0
    for ele,indx in zip(instance["labels"],range(n)):
        if LB[indx] > UB[indx]:
            print(f'Errore: UB[{ele}]= {UB[ele]}>LB{LB[ele]} =LB[{ele}].')
            exit(0)
        if ele in instance["forced_in"]:
            LB[indx] = 1
        if ele in instance["forced_out"]:
            UB[indx] = 0
        cost_forced_in += LB[indx]*instance["costs"][indx]
    if cost_forced_in > instance["Knapsack_Capacity"]:
        if len(instance["forced_in"]) > 0:
            print(f'Errore: il costo/peso complessivo degli elementi obbligati ({cost_forced_in}) già eccede la capacità dello zaino {instance["Knapsack_Capacity"]}')
        else:
            print(f'Errore: il prodotto scalare del vettore `cost` e il vettore dei lower bounds `LB` già eccede la capacità dello zaino {instance["Knapsack_Capacity"]}')
        exit(0)

        
def solver(input_to_oracle):
    #print(f"input_to_oracle={input_to_oracle}",file=stderr)
    I = input_to_oracle["input_data_assigned"]
    #print(f"Instance={I}",file=stderr)
    n = len(I["labels"])
    LB = I["LB"]
    UB = I["UB"]
    if len(UB)==0:
        LB = [0]*n
        UB = [1]*n

    DPtable_opt_val = [[0 for j in range(I["Knapsack_Capacity"]+1)] for i in range(n+1)]
    DPtable_num_opts = [[1 for j in range(I["Knapsack_Capacity"]+1)] for i in range(n+1)]
    for obj_label,i in zip(I["labels"],range(1,1+n)): # i=object index, but also i=row_index (row_indexes of the DP table start from zero, the first row is already computed as a base case, before entering this for loop)
        obj_cost = I["costs"][i-1]; obj_val = I["vals"][i-1]
        if obj_label in I["forced_in"]:
            LB[i-1] = 1
        if obj_label in I["forced_out"]:
            UB[i-1] = 0
        obj_LB = LB[i-1]; obj_UB = UB[i-1]
        for j in range(I["Knapsack_Capacity"]+1): # j=column_index of the DP table 
            DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j]
            DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j]
            obj_times = 1
            while obj_times <= obj_UB and obj_times*obj_cost <= j:
                #print(f"i={i}, obj_label={obj_label}, obj_cost={obj_cost}, obj_val={obj_val}, j={j}, obj_times={obj_times}",file=stderr)
                if DPtable_opt_val[i][j] == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                    DPtable_num_opts[i][j] += DPtable_num_opts[i-1][j-obj_times*obj_cost]
                elif DPtable_opt_val[i][j] < obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                    DPtable_opt_val[i][j] = obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                    DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j]
                obj_times += 1
        #print(f"DPtable_opt_val={DPtable_opt_val}",file=stderr)
        #print(f"DPtable_num_opts={DPtable_num_opts}",file=stderr)
        
    #print(f"DPtable_opt_val={DPtable_opt_val}",file=stderr)
    #print(f"DPtable_num_opts={DPtable_num_opts}",file=stderr)

    def yield_opt_sols_list(i,j,promise,num_opt_sols_MAX):
        assert promise >= 0 and j >= 0 and i >= 0   
        if i == 0:
            assert promise == 0
            yield []
            return
        obj_label = I["labels"][i-1]
        obj_cost = I["costs"][i-1]; obj_val = I["vals"][i-1]
        obj_LB = LB[i-1]; obj_UB = UB[i-1]
        #print(f'\ni={i}\nj={j}\npromise={promise}\nobj_label={obj_label}\nobj_cost={obj_cost}\nobj_val={obj_val}\nopt_sol={opt_sol}', file=stderr)
        for obj_times in range(obj_UB+1):
            if obj_times*obj_cost > j:
                break
            if promise <= obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                assert promise == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                for opt_sol in yield_opt_sols_list(i-1,j-obj_times*obj_cost,promise-obj_times*obj_val,num_opt_sols_MAX):
                    if num_opt_sols_MAX > 0:
                        yield opt_sol + [obj_label]*obj_times
                        num_opt_sols_MAX -= 1

    if n == 0:
        opt_val = 0; num_opt_sols = 1; list_opt_sols = [[]]
    else:
        opt_val=DPtable_opt_val[i][j]; num_opt_sols=DPtable_num_opts[i][j]
    num_opt_sols_MAX=input_to_oracle["request_setups"]['MAX_NUM_OPT_SOLS_IN_LIST']
    #print(f"num_opt_sols_MAX={num_opt_sols_MAX}")
    list_opt_sols = list(yield_opt_sols_list(i,j,promise=opt_val,num_opt_sols_MAX=num_opt_sols_MAX))
    opt_sol = list_opt_sols[0]
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nnum_opt_sols={num_opt_sols}\nDPtable_opt_val={DPtable_opt_val}\nDPtable_num_opts={DPtable_num_opts}\nlist_opt_sols={list_opt_sols}", file=stderr)
    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers
