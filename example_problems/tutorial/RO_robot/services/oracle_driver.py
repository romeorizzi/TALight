#!/usr/bin/env python3

from sys import exit, stderr

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_std_io_lib as RO_io
from robot_lib import solver, check_instance_consistency

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('pwd', str),
    ('grid', 'list_of_str'),
    ('diag', bool),
    ('partialDP_to', 'list_of_str'),
    ('partialDP_from', 'list_of_str'),
    ('cell_from', str),
    ('cell_to', str),
    ('cell_through', str),
    ('request_dict', 'yaml'),
    ('as_yaml', bool),
    ('recall_instance', bool),
    ('recall_request', bool),
    ('with_opening_message', bool),
    ('with_output_files', bool),
    ('esercizio', int),
    ('task', int),
]
instance_objects = ['grid', 'diag', 'partialDP_to',
                    'partialDP_from', 'cell_from', 'cell_to', 'cell_through']
sol_objects_implemented = ['opt_val','opt_path','DPtable_opt_from']

ENV = Env(args_list)
TAc = TALcolors(ENV, "None")
LANG = Lang(ENV, TAc, lambda fstring: eval(
    f"f'{fstring}'"), print_opening_msg='now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

TOKEN_REQUIRED = True
RO_io.check_access_rights(ENV, TALf, require_pwd=True,
                       TOKEN_REQUIRED=TOKEN_REQUIRED)
instance_dict = RO_io.dict_of_instance(instance_objects, args_list, ENV)
check_instance_consistency(instance_dict)
RO_io.check_request(ENV['request_dict'], sol_objects_implemented)

request_dict = ENV["request_dict"]
if len(request_dict) == 0:
    request_dict = {key: key for key in sol_objects_implemented}
print(f"request_dict={request_dict}", file=stderr)

call_data = {"instance": instance_dict, "request": request_dict}
call_data["oracle"] = solver(call_data)

RO_io.oracle_outputs(call_data, ENV)
if ENV.LOG_FILES != None:
    RO_io.oracle_logs(call_data, ENV, TALf)
if ENV["with_output_files"]:
    RO_io.oracle_output_files(call_data, ENV, TALf)
