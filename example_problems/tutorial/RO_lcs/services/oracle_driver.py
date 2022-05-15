#!/usr/bin/env python3

from sys import exit

from tabulate import tabulate

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_problems_lib as RO
import lcs_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('pwd',str),
    ('s','str'),
    ('t','str'),
    ('start_with','str'),
    ('end_with','str'),
    ('forbidden_s_interval_first_pos','int'),
    ('forbidden_s_interval_last_pos','int'),
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
lcs_lib.check_request_consistency(ENV)
                    
opt_val, opt_sol, DPtable = lcs_lib.solver(ENV)

call_data = {'oracle': lcs_lib.dict_of_oracle(ENV, opt_val,opt_sol,DPtable), 'input': lcs_lib.dict_of_input(ENV) }

RO.oracle_outputs(ENV, call_data)

