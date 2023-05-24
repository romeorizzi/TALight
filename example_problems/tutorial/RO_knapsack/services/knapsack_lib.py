#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable

from RO_verify_submission_gen_prob_lib import verify_submission_gen

instance_objects_spec = [
    ('Knapsack_Capacity',int),
    ('labels','list_of_str'),
    ('costs','list_of_int'),
    ('vals','list_of_int'),
    ('LB','list_of_int'),
    ('UB','list_of_int'),
    ('forced_out','list_of_str'),
    ('forced_in','list_of_str'),
    ('CAP_FOR_NUM_SOLS',int),
    ('CAP_FOR_NUM_OPT_SOLS',int),
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
limits = {'CAP_FOR_NUM_SOLS':100,'CAP_FOR_NUM_OPT_SOLS':100}

def sum_of_costs_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["costs"], instance["labels"]) if ele in ordered_list_of_elems])

def sum_of_vals_over(instance, ordered_list_of_elems):
    return sum([val for val,ele in zip(instance["vals"], instance["labels"]) if ele in ordered_list_of_elems])

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
    if instance["CAP_FOR_NUM_SOLS"] > limits["CAP_FOR_NUM_SOLS"]:
        print('Errore: non è consentito settare `CAP_FOR_NUM_SOLS` a {instance["CAP_FOR_NUM_SOLS"]} > {limits["CAP_FOR_NUM_SOLS"]}"]}')
        exit(0)
    if instance["CAP_FOR_NUM_OPT_SOLS"] > limits["CAP_FOR_NUM_OPT_SOLS"]:
        print('Errore: non è consentito settare `CAP_FOR_NUM_OPT_SOLS` a {instance["CAP_FOR_NUM_OPT_SOLS"]} > {limits["CAP_FOR_NUM_OPT_SOLS"]}"]}')
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
            if obj_LB*obj_cost > j or DPtable_opt_val[i-1][j-obj_LB*obj_cost] is None:
                DPtable_opt_val[i][j] = None
                DPtable_num_opts[i][j] = 0
            else:                
                DPtable_opt_val[i][j] = obj_LB*obj_val + DPtable_opt_val[i-1][j-obj_LB*obj_cost]
                DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j-obj_LB*obj_cost]
                obj_times = obj_LB+1
                while obj_times <= obj_UB and obj_times*obj_cost <= j and DPtable_num_opts[i-1][j-obj_times*obj_cost] > 0:
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
        #print(f'\ni={i}\nj={j}\npromise={promise}\nnum_opt_sols_MAX={num_opt_sols_MAX}\nobj_label={obj_label}\nobj_cost={obj_cost}\nobj_val={obj_val}\nobj_LB={obj_LB}\nobj_UB={obj_UB}', file=stderr)
        for obj_times in range(obj_LB,obj_UB+1):
            if obj_times*obj_cost > j or DPtable_opt_val[i-1][j-obj_times*obj_cost] is None:
                break
            if promise <= obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                assert promise == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                for opt_sol in yield_opt_sols_list(i-1,j-obj_times*obj_cost,promise-obj_times*obj_val,num_opt_sols_MAX):
                    assert num_opt_sols_MAX > 0
                    if num_opt_sols_MAX > 0:
                        yield opt_sol + [obj_label]*obj_times
                        num_opt_sols_MAX -= 1

    if n == 0:
        opt_val = 0; num_opt_sols = 1; list_opt_sols = [[]]
    else:
        opt_val=DPtable_opt_val[i][j]; num_opt_sols=DPtable_num_opts[i][j]
    num_opt_sols_MAX=I['CAP_FOR_NUM_OPT_SOLS']
    list_opt_sols = list(yield_opt_sols_list(i,j,promise=opt_val,num_opt_sols_MAX=num_opt_sols_MAX))
    opt_sol = list_opt_sols[0]
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nnum_opt_sols={num_opt_sols}\nDPtable_opt_val={DPtable_opt_val}\nDPtable_num_opts={DPtable_num_opts}\nlist_opt_sols={list_opt_sols}", file=stderr)
    oracle_answers = {}
    for std_name in answer_objects_spec:
        oracle_answers[std_name] = locals()[std_name]
        if std_name in input_to_oracle["request"]:
            ad_hoc_name = input_to_oracle["request"][std_name]
            oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers


class verify_submission_problem_specific(verify_submission_gen):
    def __init__(self, SEF,input_data_assigned:Dict, long_answer_dict:Dict, oracle_response:Dict = None):
        super().__init__(SEF,input_data_assigned, long_answer_dict, oracle_response)

    def verify_format(self, SEF):
        if not super().verify_format(SEF):
            return False
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di oggetti (esempio ['{self.I.labels[0]}','{self.I.labels[2]}']). Hai invece immesso `{g.answ}`.")
            for ele in g.answ:
                if ele not in self.I.labels:
                    return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista `{g.alias}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {self.I.labels}.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ammissibilità di `{g.alias}`")
        return True
                
    def set_up_and_cash_handy_data(self):
        if 'opt_sol' in self.goals:
            self.sum_vals = sum([val for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in self.goals['opt_sol'].answ])
            self.sum_costs = sum([cost for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in self.goals['opt_sol'].answ])
            
    def verify_feasibility(self, SEF):
        if not super().verify_feasibility(SEF):
            return False
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            for ele in g.answ:
                if ele in self.I.forced_out:
                    return SEF.feasibility_NO(g, f"L'oggetto `{ele}` da tè inserito nella lista `{g.alias}` è tra quelli proibiti. Gli oggetti proibiti per la Richiesta {str(SEF.task_number)}, sono {self.I.forced_out}.")
            for ele in self.I.forced_in:
                if ele not in g.answ:
                    return SEF.feasibility_NO(g, f"Nella lista `{g.alias}` hai dimenticato di inserire l'oggetto `{ele}` che invece è forzato. Gli oggetti forzati per la Richiesta {str(SEF.task_number)} sono {self.I.forced_in}.")
            if self.sum_costs > self.I.Knapsack_Capacity:
                return SEF.feasibility_NO(g, f"La tua soluzione in `{g.alias}` ha costo {self.sum_costs} > Knapsack_Capacity e quindi NON è ammissibile in quanto fora il budget per la Richiesta {str(SEF.task_number)}. La soluzione da tè inserita ricomprende il sottoinsieme di oggetti `{g.alias}`= {g.answ}.")
            SEF.feasibility_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ottimalità di `{g.alias}`")
        return True
                
    def verify_consistency(self, SEF):
        if not super().verify_consistency(SEF):
            return False
        if 'opt_val' in self.goals and 'opt_sol' in self.goals:
            g_val = self.goals['opt_val']; g_sol = self.goals['opt_sol']
            if self.sum_vals != g_val.answ:
                return SEF.consistency_NO(['opt_val','opt_sol'], f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {self.sum_vals}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(['opt_val','opt_sol'], f"{g_val.alias}={g_val.answ} = somma dei valori sugli oggetti in `{g_sol.alias}`.", f"resta da stabilire l'ottimalità di `{g_val.alias}` e `{g_sol.alias}`")
        return True

    def verify_optimality(self, SEF):
        if not super().verify_optimality(SEF):
            return False
        true_opt_val = SEF.oracle_dict['opt_val']
        true_opt_sol = SEF.oracle_dict['opt_sol']
        if 'opt_val' in self.goals:
            g_val = self.goals['opt_val']
            if true_opt_val != g_val.answ:
                return SEF.optimality_NO(g_val, f"Il valore ottimo corretto è {true_opt_val} {'>' if true_opt_val != g_val.answ else '<'} {g_val.answ}, che è il valore invece immesso in `{g_val.alias}`. Una soluzione di valore ottimo è {true_opt_sol}.")
            else:
                SEF.optimality_OK(g_val, f"{g_val.alias}={g_val.answ} è effettivamente il valore ottimo.", "")
        if 'opt_sol' in self.goals:
            g_sol = self.goals['opt_sol']
            g_sol_answ = self.goals['opt_sol'].answ
            g_val_answ = sum([val for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in g_sol_answ])
            assert g_val_answ <= true_opt_val
            if g_val_answ < true_opt_val:
                return SEF.optimality_NO(g_sol, f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {g_val_answ} < {true_opt_val}, valore corretto per una soluzione ottima quale {true_opt_sol}. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            else:
                SEF.optimality_OK(g_sol, f"Confermo l'ottimailtà della soluzione {g_sol.alias}={g_sol.answ}.", "")
        return True
