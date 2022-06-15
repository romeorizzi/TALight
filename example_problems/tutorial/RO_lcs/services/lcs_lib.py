#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable

from RO_verify_submission_gen_prob_lib import verify_submission_gen
from RO_utils import display_matrix

instance_objects_spec = [
    ('s',str),
    ('t',str),
    ('start_with',str),
    ('end_with',str),
    ('forbidden_s_interval_first_pos',int),
    ('forbidden_s_interval_last_pos',int),
    ('reduce_s_to_its_prefix_of_length',int),
    ('reduce_t_to_its_prefix_of_length',int),
    ('reduce_s_to_its_suffix_of_length',int),
    ('reduce_t_to_its_suffix_of_length',int),
]
additional_infos_spec=[
    ('partial_max_len_on_prefixes_of_len','matrix_of_int'),
    ('partial_max_len_on_suffixes_from_pos','matrix_of_int')
]
answer_objects_spec = {
    'opt_sol':'list_of_str',
    'opt_val':int,
    'max_len_on_prefixes_of_len':'matrix_of_int',
    'max_len_on_suffixes_from_pos':'matrix_of_int',
}
answer_objects_implemented = ['opt_sol','opt_val','max_len_on_prefixes_of_len','max_len_on_suffixes_from_pos']
request_setups = {}


def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    m = len(instance["s"]) 
    n = len(instance["t"]) 
    if instance["reduce_s_to_its_prefix_of_length"] < 0:
        print(f"Errore: reduce_s_to_its_prefix_of_length={reduce_s_to_its_prefix_of_length} < 0  non è permesso. Puoi invece usare numeri arbitrariamente grandi per questo argomento (oltre len(s) significa considerare l'intera stringa s).")    
        exit(0)
    if instance["reduce_t_to_its_prefix_of_length"] < 0:
        print(f"Errore: reduce_t_to_its_prefix_of_length={reduce_t_to_its_prefix_of_length} < 0  non è permesso. Puoi invece usare numeri arbitrariamente grandi per questo argomento (oltre len(t) significa considerare l'intera stringa t).")    
        exit(0)
    if instance["reduce_s_to_its_suffix_of_length"] < 0:
        print(f"Errore: reduce_s_to_its_suffix_of_length={reduce_s_to_its_suffix_of_length} < 0  non è permesso. Puoi invece usare numeri arbitrariamente grandi per questo argomento (oltre len(s) significa considerare l'intera stringa s).")    
        exit(0)
    if instance["reduce_t_to_its_suffix_of_length"] < 0:
        print(f"Errore: reduce_t_to_its_suffix_of_length={reduce_t_to_its_suffix_of_length} < 0  non è permesso. Puoi invece usare numeri arbitrariamente grandi per questo argomento (oltre len(t) significa considerare l'intera stringa t).")    
        exit(0)

class DPtable:
    def __init__(self, m,n,rlabels,clabels,init_fill=None):
        self.m = m
        self.n = n
        self.val = [ [ init_fill ]*m for i in range(n) ]
        self.rlabels = clabels
        self.clabels = clabels

    def __repr__(self):
        return f'Object goal(self.std_name={self.std_name}, self.alias={self.alias}, self.answ={self.answ})'

        
def solver(input_to_oracle):
    policy ="""NOTE: it is our fundamental policy and assumption that the request posed to the student may be settled by only looking at the following two fixed DP tables:
          1. max_len_on_prefixes_of_len:
              where s= I['s'] and t=I['t']
          2. max_len_on_suffixes_from_pos:
              where s= I['s'] and t=I['t']
       This rule should not be violated when designing the exercise supported with this problem. Therefore, we stick to it in any of our services.
    """
          
    #print(f"input_to_oracle={input_to_oracle}",file=stderr)
    I = input_to_oracle["input_data_assigned"]
    #print(f"Instance={I}",file=stderr)
    s= I['s']
    t= I['t']
    print(f"s={s}, len(s)={len(s)}")
    print(f"t={t}, len(t)={len(t)}")
    max_len_on_prefixes_of_len = [ [ 0 ] * (1+len(t)) for i in range(1+len(s)) ]
    for i in range(1,1+len(s)):
      for j in range(1,1+len(t)):
          if s[i-1] == t[j-1]:
              max_len_on_prefixes_of_len[i][j] = 1 + max_len_on_prefixes_of_len[i-1][j-1]
          else:
              max_len_on_prefixes_of_len[i][j] = max(max_len_on_prefixes_of_len[i-1][j],max_len_on_prefixes_of_len[i][j-1])

    print("max_len_on_prefixes_of_len:")
    #print(display_matrix(max_len_on_prefixes_of_len, rlabels=list("-"+s), clabels=list("-"+t)))
    print(str(display_matrix(max_len_on_prefixes_of_len, rlabels=list("-"+s), clabels=list("-"+t))))
    
    max_len_on_suffixes_from_pos = [ [ 0 ] * (1+len(t)) for i in range((1+len(s))) ]
    for i in range(len(s)-1,-1,-1):
      for j in range(len(t)-1,-1,-1):
          if s[i] == t[j]:
              max_len_on_suffixes_from_pos[i][j] = 1 + max_len_on_suffixes_from_pos[i+1][j+1]
          else:
              max_len_on_suffixes_from_pos[i][j] = max(max_len_on_suffixes_from_pos[i+1][j],max_len_on_suffixes_from_pos[i][j+1])
    assert(max_len_on_prefixes_of_len[len(s)][len(t)]==max_len_on_suffixes_from_pos[0][0])
    
    print(display_matrix(max_len_on_suffixes_from_pos, rlabels=list(range(len(s)))+['-'], clabels=list(range(len(t)))+['-']))

    
    def reconstruct_opt_lcs_pref_of_len(len_s,len_t):
        if max_len_on_prefixes_of_len[len_s][len_t] == 0:
            pass
        elif s[len_s-1] == t[len_t-1]:
            yield s[len_s-1]
            yield from reconstruct_opt_lcs_pref_of_len(len_s-1,len_t-1)
        elif len_s==1:
            yield from reconstruct_opt_lcs_pref_of_len(len_s,len_t-1)
        elif max_len_on_prefixes_of_len[len_s-1][len_t]==max_len_on_prefixes_of_len[len_s][len_t]:
            yield from reconstruct_opt_lcs_pref_of_len(len_s-1,len_t)
        else:
            yield from reconstruct_opt_lcs_pref_of_len(len_s,len_t-1)

    def reconstruct_opt_lcs_suff_from_pos(i,j):
        if max_len_on_suffixes_from_pos[i][j] == 0:
            pass
        elif s[i] == t[j]:
            yield s[i]
            yield from reconstruct_opt_lcs_suff_from_pos(i+1,j+1)
        elif i==len(s)-1:
            yield from reconstruct_opt_lcs_suff_from_pos(i,j+1)
        elif max_len_on_suffixes_from_pos[i+1][j]==max_len_on_suffixes_from_pos[i][j]:
            yield from reconstruct_opt_lcs_suff_from_pos(i+1,j)
        else:
            yield from reconstruct_opt_lcs_suff_from_pos(i,j+1)

    first_pos_in_s = max(0,len(s)-I['reduce_s_to_its_suffix_of_length'])
    first_pos_in_t = max(0,len(t)-I['reduce_t_to_its_suffix_of_length'])
    if I['start_with'] != '*':
        while first_pos_in_s < len(s) and (s[first_pos_in_s] != I['start_with'] or I['forbidden_s_interval_first_pos'] <= first_pos_in_s <= I['forbidden_s_interval_last_pos']):
            first_pos_in_s += 1
        while first_pos_in_t < len(t) and t[first_pos_in_t] != I['start_with']:
            first_pos_in_t += 1
    last_pos_in_s = min(len(s),I['reduce_s_to_its_prefix_of_length']) -1
    last_pos_in_t = min(len(t),I['reduce_t_to_its_prefix_of_length']) -1
    if I['end_with'] != '*':
        while last_pos_in_s >= 0 and (s[last_pos_in_s] != I['end_with'] or I['forbidden_s_interval_first_pos'] <= last_pos_in_s <= I['forbidden_s_interval_last_pos']):
            last_pos_in_s -= 1
        while last_pos_in_t >= 0 and t[last_pos_in_t] != I['end_with']:
            last_pos_in_t -= 1

    if last_pos_in_t < first_pos_in_t or last_pos_in_s < first_pos_in_s:
        opt_val = 0 ; opt_sol = []
    elif (first_pos_in_t > 0 and last_pos_in_t < len(t)-1) or (first_pos_in_s > 0 and last_pos_in_s < len(s)-1) or (first_pos_in_t > 0 and last_pos_in_s < len(s)-1) or (first_pos_in_s > 0 and last_pos_in_t < len(t)-1):
        return {'exception': ("the question posed violates the policy of this problem",policy)}
    else:
        if I['forbidden_s_interval_first_pos'] > I['forbidden_s_interval_last_pos']:
            if first_pos_in_s > 0 or first_pos_in_t > 0:
                opt_val = max_len_on_suffixes_from_pos[first_pos_in_s][first_pos_in_t]
                opt_sol = list(reconstruct_opt_lcs_suff_from_pos(first_pos_in_s,first_pos_in_t))
            else:
                opt_val = max_len_on_prefixes_of_len[last_pos_in_s +1][last_pos_in_t +1]
                opt_sol = list(reconstruct_opt_lcs_pref_of_len(last_pos_in_s +1,last_pos_in_t +1)); opt_sol.reverse()
        elif first_pos_in_s > I['forbidden_s_interval_last_pos']:
            opt_val = max_len_on_suffixes_from_pos[first_pos_in_s][first_pos_in_t]
            opt_sol = list(reconstruct_opt_lcs_suff_from_pos(first_pos_in_s,first_pos_in_t))
        elif last_pos_in_s < I['forbidden_s_interval_first_pos']:
            opt_val = max_len_on_prefixes_of_len[last_pos_in_s +1][last_pos_in_t +1]
            opt_sol = list(reconstruct_opt_lcs_pref_of_len(last_pos_in_s +1,last_pos_in_t +1)); opt_sol.reverse()
        else:
            if first_pos_in_s > 0 or last_pos_in_s < len(s)-1 or first_pos_in_t > 0 or last_pos_in_t < len(t)-1:
                return {'exception': ("the question posed violates the policy of this problem",policy)}
            best_so_far_val = max_len_on_suffixes_from_pos[I['forbidden_s_interval_last_pos']+1][0]
            best_so_far_sol = list(reconstruct_opt_lcs_suff_from_pos(first_pos_in_s,first_pos_in_t))
            if best_so_far_val < max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][len(t)]:
                best_so_far_val = max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][len(t)]
                best_so_far_sol = list(reconstruct_opt_lcs_pref_of_len(I['forbidden_s_interval_first_pos'],len(t))); best_so_far_sol.reverse()
            for sweet_t_pos in range(len(t)):
                if best_so_far_val < max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][sweet_t_pos+1] + max_len_on_suffixes_from_pos[I['forbidden_s_interval_last_pos']+1][sweet_t_pos+1]:
                    best_so_far_val = max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][sweet_t_pos+1] + max_len_on_suffixes_from_pos[I['forbidden_s_interval_last_pos']+1][sweet_t_pos+1]
                    best_so_far_sol = list(reconstruct_opt_lcs_pref_of_len(I['forbidden_s_interval_first_pos'],sweet_t_pos+1)); best_so_far_sol.reverse()
                    best_so_far_sol += list(reconstruct_opt_lcs_suff_from_pos(I['forbidden_s_interval_last_pos']+1,sweet_t_pos+1))
        

    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers


class verify_submission_problem_specific(verify_submission_gen):
    def __init__(self, SEF,input_data_assigned:Dict, long_answer_dict:Dict, request_setups:str):
        super().__init__(SEF,input_data_assigned, long_answer_dict, request_setups)

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
            g_val = self.goals['opt_val']; g_sol = self.goals['opt_sol'];
            if self.sum_vals != g_val.answ:
                return SEF.consistency_NO(['opt_val','opt_sol'], f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {self.sum_vals}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(['opt_val','opt_sol'], f"{g_val.alias}={g_val.answ} = somma dei valori sugli oggetti in `{g_sol.alias}`.", "")
        return True
