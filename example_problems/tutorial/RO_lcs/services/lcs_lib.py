#!/usr/bin/env python3
from sys import stderr
import re
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
    'opt_sol':str,
    'opt_val':int,
    'max_len_on_prefixes_of_len':'matrix_of_int',
    'max_len_on_suffixes_from_pos':'matrix_of_int',
}
answer_objects_implemented = ['opt_sol','opt_val','max_len_on_prefixes_of_len','max_len_on_suffixes_from_pos']
request_setups = {}


def is_subseq(s,t):
    if len(s)==0:
        return True
    if len(t)==0:
        return False
    if s[0]==t[0]:
        return is_subseq(s[1:],t[1:])
    return is_subseq(s,t[1:])
        
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
    max_len_on_prefixes_of_len = [ [ 0 ] * (1+len(t)) for i in range(1+len(s)) ]
    for i in range(1,1+len(s)):
      for j in range(1,1+len(t)):
          if s[i-1] == t[j-1]:
              max_len_on_prefixes_of_len[i][j] = 1 + max_len_on_prefixes_of_len[i-1][j-1]
          else:
              max_len_on_prefixes_of_len[i][j] = max(max_len_on_prefixes_of_len[i-1][j],max_len_on_prefixes_of_len[i][j-1])

    #print("max_len_on_prefixes_of_len:")
    #print(display_matrix(max_len_on_prefixes_of_len, rlabels=list("-"+s), clabels=list("-"+t)))
    #print(str(display_matrix(max_len_on_prefixes_of_len, rlabels=list("-"+s), clabels=list("-"+t))))
    
    max_len_on_suffixes_from_pos = [ [ 0 ] * (1+len(t)) for i in range((1+len(s))) ]
    for i in range(len(s)-1,-1,-1):
      for j in range(len(t)-1,-1,-1):
          if s[i] == t[j]:
              max_len_on_suffixes_from_pos[i][j] = 1 + max_len_on_suffixes_from_pos[i+1][j+1]
          else:
              max_len_on_suffixes_from_pos[i][j] = max(max_len_on_suffixes_from_pos[i+1][j],max_len_on_suffixes_from_pos[i][j+1])
    assert(max_len_on_prefixes_of_len[len(s)][len(t)]==max_len_on_suffixes_from_pos[0][0])
    
    #print("max_len_on_suffixes_from_pos:")
    #print(display_matrix(max_len_on_suffixes_from_pos, rlabels=list(range(len(s)))+['-'], clabels=list(range(len(t)))+['-']))

    
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
                opt_sol = ''.join(reconstruct_opt_lcs_suff_from_pos(first_pos_in_s,first_pos_in_t))
            else:
                opt_val = max_len_on_prefixes_of_len[last_pos_in_s +1][last_pos_in_t +1]
                opt_sol = ''.join(reconstruct_opt_lcs_pref_of_len(last_pos_in_s +1,last_pos_in_t +1))[::-1]  #the slice at the end reverses the string
        elif first_pos_in_s > I['forbidden_s_interval_last_pos']:
            opt_val = max_len_on_suffixes_from_pos[first_pos_in_s][first_pos_in_t]
            opt_sol = ''.join(reconstruct_opt_lcs_suff_from_pos(first_pos_in_s,first_pos_in_t))
        elif last_pos_in_s < I['forbidden_s_interval_first_pos']:
            opt_val = max_len_on_prefixes_of_len[last_pos_in_s +1][last_pos_in_t +1]
            opt_sol = ''.join(reconstruct_opt_lcs_pref_of_len(last_pos_in_s +1,last_pos_in_t +1))[::-1]  #the slice at the end reverses the string
        else:
            if first_pos_in_s > 0 or last_pos_in_s < len(s)-1 or first_pos_in_t > 0 or last_pos_in_t < len(t)-1:
                return {'exception': ("the question posed violates the policy of this problem",policy)}
            best_so_far_val = max_len_on_suffixes_from_pos[I['forbidden_s_interval_last_pos']+1][0]
            best_so_far_sol = ''.join(reconstruct_opt_lcs_suff_from_pos(first_pos_in_s,first_pos_in_t))
            if best_so_far_val < max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][len(t)]:
                best_so_far_val = max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][len(t)]
                best_so_far_sol = ''.join(reconstruct_opt_lcs_pref_of_len(I['forbidden_s_interval_first_pos'],len(t)))[::-1]
            for sweet_t_pos in range(len(t)):
                if best_so_far_val < max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][sweet_t_pos+1] + max_len_on_suffixes_from_pos[I['forbidden_s_interval_last_pos']+1][sweet_t_pos+1]:
                    best_so_far_val = max_len_on_prefixes_of_len[I['forbidden_s_interval_first_pos']][sweet_t_pos+1] + max_len_on_suffixes_from_pos[I['forbidden_s_interval_last_pos']+1][sweet_t_pos+1]
                    best_so_far_sol = ''.join(reconstruct_opt_lcs_pref_of_len(I['forbidden_s_interval_first_pos'],sweet_t_pos+1))[::-1]
                    best_so_far_sol += ''.join(reconstruct_opt_lcs_suff_from_pos(I['forbidden_s_interval_last_pos']+1,sweet_t_pos+1))
        

    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers


class verify_submission_problem_specific(verify_submission_gen):
    def __init__(self, SEF,input_data_assigned:Dict, long_answer_dict:Dict, request_setups:Dict):
        super().__init__(SEF,input_data_assigned, long_answer_dict, request_setups)

    def verify_format(self, SEF):
        if not super().verify_format(SEF):
            return False
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if not bool(re.match("",g.answ)):
                return SEF.format_NO(g, f"Come `{g.alias}` và inserita una stringa sull'alfabeto delle 26 lettere inglesi maiuscole. Invece hai immesso '{g.answ}'.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso una stringa sul corretto alfabeto (le 26 lettere inglesi maiuscole).", f"resta da stabilire l'ammissibilità di `{g.alias}`")
        return True
            
    def verify_feasibility(self, SEF):
        if not super().verify_feasibility(SEF):
            return False
        s=self.I.s ; t=self.I.t
#        s=self.I['s'] ; s=self.I['t']
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if not is_subseq(g.answ,s):
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una sottosequenza di `s`='{s}'. Hai invece immesso '{g.answ}'.")
            if not is_subseq(g.answ,t):
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una sottosequenza di `t`='{t}'. Hai invece immesso '{g.answ}'.")
            if not is_subseq(g.answ,s[:self.I.reduce_s_to_its_prefix_of_length]):
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non è una sottosequenza del prefisso di s di lunghezza {self.I.reduce_s_to_its_prefix_of_length}")
            if not is_subseq(g.answ,t[:self.I.reduce_t_to_its_prefix_of_length]):
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non è una sottosequenza del prefisso di t di lunghezza {self.I.reduce_t_to_its_prefix_of_length}")
            if not is_subseq(g.answ,s[-self.I.reduce_s_to_its_suffix_of_length:]):
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non è una sottosequenza del suffisso di s di lunghezza {self.I.reduce_s_to_its_prefix_of_length}")
            if not is_subseq(g.answ,t[-self.I.reduce_t_to_its_suffix_of_length:]):
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non è una sottosequenza del suffisso di t di lunghezza {self.I.reduce_t_to_its_prefix_of_length}")
            if self.I.forbidden_s_interval_first_pos <= self.I.forbidden_s_interval_last_pos and not is_subseq(g.answ,s[:self.I.forbidden_s_interval_first_pos]+s[self.I.forbidden_s_interval_last_pos+1:]):
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non è una sottosequenza di s che eviti l'intervallo escluso s[{self.I.forbidden_s_interval_first_pos},{self.I.forbidden_s_interval_last_pos}]")
            if self.I.start_with != '*' and g.answ[0] != self.I.start_with:
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non inizia con carattere {self.I.start_with}")
            if self.I.end_with != '*' and g.answ[0] != self.I.end_with:
                SEF.format_NO(g, f"la stringa `{g.alias}` che hai immesso non termina con carattere {self.I.end_with}")
            SEF.feasibility_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ottimalità di `{g.alias}`")
        return True
                
    def verify_consistency(self, SEF):
        if not super().verify_consistency(SEF):
            return False
        if 'opt_val' in self.goals and 'opt_sol' in self.goals:
            g_val = self.goals['opt_val']; g_sol = self.goals['opt_sol'];
            if len(g_sol.answ) != g_val.answ:
                return SEF.consistency_NO(['opt_val','opt_sol'], f"La lunghezza della soluzione immessa in `{g_sol.alias}` è {len(g_sol.answ)} e NON {g_val.answ}. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(['opt_val','opt_sol'], f"{g_val.alias}={g_val.answ} = len({g_sol.alias}).", "")
        return True
