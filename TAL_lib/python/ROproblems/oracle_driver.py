#!/usr/bin/env python3

from sys import exit, stderr

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import RO_std_io_lib as RO_io

import problem_specific_lib as PSL

# METADATA OF THIS TAL_SERVICE:
args_list = [('pwd',str)] + PSL.instance_objects_spec + [
    ('input_data_assigned','yaml'),
    ('request_dict','yaml'),
    ('color_implementation',str),
    ('with_opening_message',bool),
    ('as_yaml',bool),
    ('recall_data_assigned',bool),
    ('recall_request',bool),
    ('with_output_files',bool),
    ('esercizio',int),
    ('task',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV, "None")
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

TOKEN_REQUIRED = True
RO_io.check_access_rights(ENV,TALf, require_pwd = True, TOKEN_REQUIRED = TOKEN_REQUIRED)
input_data_assigned = RO_io.dict_of_instance(PSL.instance_objects_spec,args_list,ENV)
#print("\n"f"input_data_assigned={input_data_assigned}", file=stderr)
PSL.check_instance_consistency(input_data_assigned)
RO_io.check_request(ENV['request_dict'], PSL.answer_objects_implemented)

request_dict = ENV["request_dict"] if len(ENV["request_dict"]) != 0 else { key:key for key in PSL.answer_objects_implemented }
#print(f"request_dict={request_dict}", file=stderr)
    
call_data = {"input_data_assigned":input_data_assigned,"request":request_dict}
#print(f"call_data={call_data}", file=stderr)
call_data["oracle"] = PSL.solver(call_data)

RO_io.oracle_outputs(call_data,ENV)
if ENV.LOG_FILES != None:
    RO_io.oracle_logs(call_data,ENV,TALf)
if ENV["with_output_files"]:    
    RO_io.oracle_output_files(call_data,ENV,TALf)
