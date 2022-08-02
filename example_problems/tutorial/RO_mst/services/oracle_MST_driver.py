#!/usr/bin/env python3

from sys import exit

from tabulate import tabulate

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_problems_lib as RO
import MST_lib

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('pwd',str),
    ('n','int'),
    ('nodi','list_of_str'),
    ('archi','yaml'),
    ('archi_proibiti','yaml'),
    ('archi_obbligati','yaml'),
    ('sol_type',str),
    ('name_of_opt_val',str),
    ('name_of_opt_sol',str),
    ('name_of_num_opt_sols',str),
    ('name_of_list_opt_sols',str),
    ('as_yaml',bool),
    ('recall_input',bool),
    ('with_opening_message',bool),
    ('esercizio',int),
    ('task',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, None)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

TOKEN_REQUIRED = True
RO.check_access_rights(ENV,TALf, require_pwd = True, TOKEN_REQUIRED = TOKEN_REQUIRED)
MST_lib.check_request_consistency(ENV)
                    
opt_val, opt_sol, DPtable = MST_lib.solver(ENV)

call_data = {'oracle': MST_lib.dict_of_oracle(ENV, opt_val,opt_sol,DPtable), 'input': MST_lib.dict_of_input(ENV) }

RO.oracle_outputs(call_data,ENV)
if ENV.LOG_FILES != None:
    RO.oracle_logs(call_data,ENV,TALf)

