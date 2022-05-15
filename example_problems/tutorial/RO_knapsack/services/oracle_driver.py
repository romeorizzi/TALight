#!/usr/bin/env python3

from sys import exit

from tabulate import tabulate

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_problems_lib as RO
import knapsack_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('pwd',str),
    ('elementi','list_of_str'),
    ('pesi','list_of_int'),
    ('valori','list_of_int'),
    ('Knapsack_Capacity',int),
    ('elementi_proibiti','list_of_str'),
    ('elementi_obbligati','list_of_str'),
    ('sol_type',str),
    ('name_of_opt_val',str),
    ('name_of_opt_sol',str),
    ('name_of_DPtable',str),
    ('as_yaml',bool),
    ('recall_input',bool),
    ('with_opening_message',bool),
    ('esercizio',int),
    ('task',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, "None")
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

RO.check_access_rights(ENV,TALf, ask_pwd = True, ask_token = True)
knapsack_lib.check_request_consistency(ENV)
                    
opt_val, opt_sol, DPtable = knapsack_lib.solver(ENV)

call_data = {'oracle': knapsack_lib.dict_of_oracle(ENV, opt_val,opt_sol,DPtable), 'input': knapsack_lib.dict_of_input(ENV) }

RO.oracle_output(ENV, call_data)

