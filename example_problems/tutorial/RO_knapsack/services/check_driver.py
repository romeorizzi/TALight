#!/usr/bin/env python3
from sys import exit, stderr
from typing import Optional, List, Dict, Tuple
from types import SimpleNamespace

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_std_io_lib as RO_io
import RO_std_eval_lib as RO_eval

from knapsack_lib import solver, check_instance_consistency

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('labels','list_of_str'),
    ('costs','list_of_int'),
    ('vals','list_of_int'),
    ('Knapsack_Capacity',int),
    ('forced_out','list_of_str'),
    ('forced_in','list_of_str'),
    ('partialDPtable','matrix_of_int'),
    ('instance_dict','yaml'),
    ('opt_sol','yaml'),
    ('opt_val','yaml'),
    ('num_opt_sols','yaml'),
    ('list_opt_sols','yaml'),
    ('DPtable_opt_val','yaml'),
    ('DPtable_num_opts','yaml'),
    ('alias_dict','yaml'),
    ('answer_dict','yaml'),
    ('color_implementation',str),
    ('as_yaml_with_points',bool),
    ('yield_certificate_in_output_file',bool),
    ('recall_instance',bool),
    ('with_opening_message',bool),
    ('pt_formato_OK',int),
    ('pt_feasibility_OK',int),
    ('pt_consistency_OK',int),
    ('pt_tot',int),
    ('esercizio',int),
    ('task',int),
]
instance_objects = ['labels','costs','vals','Knapsack_Capacity','forced_out','forced_in','partialDPtable']
answer_object_type_spec = {
    'opt_sol':'list_of_str',
    'opt_val':'int',
    'num_opt_sols':'int',
    'list_opt_sols':'list_of_list_of_str',
    'DPtable_opt_val':'matrix_of_int',
    'DPtable_num_opts':'matrix_of_int',
}
sol_objects_implemented = ['opt_sol','opt_val','DPtable_opt_val']

ENV =Env(args_list)
TAc =TALcolors(ENV, ENV["color_implementation"])
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

TOKEN_REQUIRED = False
RO_io.check_access_rights(ENV,TALf, require_pwd = False, TOKEN_REQUIRED = TOKEN_REQUIRED)
instance_dict = RO_io.dict_of_instance(instance_objects,args_list,ENV)
#print(f"instance_dict={instance_dict}", file=stderr)
check_instance_consistency(instance_dict)
request_dict, answer_dict, name_of, answ_obj, long_answer_dict, goals = RO_io.check_and_standardization_of_request_answer_consistency(ENV['answer_dict'],ENV['alias_dict'], answer_object_type_spec, sol_objects_implemented)
#print(f"long_answer_dict={long_answer_dict}", file=stderr)


def verify_RO_knapsack_submission(SEF,instance_dict:Dict, long_answer_dict:Dict):
    I = SimpleNamespace(**instance_dict)
    goals = SEF.load(long_answer_dict)
            
    def verify_format():
        if 'opt_val' in goals:
            g = goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'opt_sol' in goals:
            g = goals['opt_sol']
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di oggetti (esempio ['{I.labels[0]}','{I.labels[2]}']). Hai invece immesso `{g.answ}`.")
            for ele in g.answ:
                if ele not in I.labels:
                    return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista `{g.alias}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {I.labels}.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ammissibilità di `{g.alias}`")
        return True
                
    def verify_feasibility():
        if 'opt_sol' in goals:
            g = goals['opt_sol']
            for ele in g.answ:
                if ele in I.forced_out:
                    return SEF.feasibility_NO(g, f"L'oggetto `{ele}` da tè inserito nella lista `{g.alias}` è tra quelli proibiti. Gli oggetti proibiti per la Richiesta {str(SEF.task_number)}, sono {I.forced_out}.")
            for ele in I.forced_in:
                if ele not in g.answ:
                    return SEF.feasibility_NO(g, f"Nella lista `{g.alias}` hai dimenticato di inserire l'oggetto `{ele}` che invece è forzato. Gli oggetti forzati per la Richiesta {str(SEF.task_number)} sono {I.forced_in}.")
            if sum_costs > I.Knapsack_Capacity:
                return SEF.feasibility_NO(g, f"La tua soluzione in `{g.alias}` ha costo {sum_costs} > I.Knapsack_Capacity e quindi NON è ammissibile in quanto fora il budget per la Richiesta {str(SEF.task_number)}. La soluzione da tè inserita ricomprende il sottoinsieme di oggetti `{g.alias}`= {g.answ}.")
            SEF.feasibility_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ottimalità di `{g.alias}`")
        return True
                
    def verify_consistency():
        if 'opt_val' in goals and 'opt_sol' in goals:
            g_val = goals['opt_val']; g_sol = goals['opt_sol'];
            if sum_vals != g_val.answ:
                return SEF.consistency_NO(['opt_val','opt_sol'], f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {sum_vals}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(['opt_val','opt_sol'], f"{g_val.alias}={g_val.answ} = somma dei valori sugli oggetti in `{g_sol.alias}`.")
        return True
                
    if not verify_format():
        return SEF.completed_feedback
    if 'opt_sol' in goals:
        sum_vals = sum([val for ele,cost,val in zip(I.labels,I.costs,I.vals) if ele in goals['opt_sol'].answ])
        sum_costs = sum([cost for ele,cost,val in zip(I.labels,I.costs,I.vals) if ele in goals['opt_sol'].answ])
    if not verify_feasibility():
        return SEF.completed_feedback
    if not verify_consistency():
        return SEF.completed_feedback
    return SEF.feedback_when_all_checks_passed()


            
SEF = RO_eval.std_eval_feedback(ENV)
feedback_dict = verify_RO_knapsack_submission(SEF,instance_dict, long_answer_dict=long_answer_dict)
#print(f"feedback_dict={feedback_dict}", file=stderr)

all_data = {"instance":instance_dict,"long_answer":long_answer_dict,"feedback":feedback_dict,"request":name_of}
#print(f"all_data={all_data}", file=stderr)
RO_io.checker_reply(all_data,ENV)
if ENV.LOG_FILES != None:
    all_data["oracle"] = solver(all_data)
    RO_io.checker_logs(all_data,ENV,TALf)
if ENV["yield_certificate_in_output_file"]:    
    RO_io.checker_certificates(all_data,ENV,TALf)


