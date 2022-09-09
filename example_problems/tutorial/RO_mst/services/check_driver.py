#!/usr/bin/env python3

import RO_std_eval_lib as RO_eval
import RO_std_io_lib as RO_io
import problem_specific_lib as PSL
from TALfiles import TALfilesHelper
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
args_list = PSL.instance_objects_spec
args_list += [(key, PSL.answer_objects_spec[key]) for key in PSL.answer_objects_spec]
args_list += [
    ('pwd', str),
    ('input_data_assigned', 'yaml'),
    ('answer_dict', 'yaml'),
    ('alias_dict', 'yaml'),
    ('color_implementation', str),
    ('with_opening_message', bool),
    ('with_positive_enforcement', bool),
    ('with_notes', bool),
    ('with_oracle', bool),
    ('as_yaml_with_points', bool),
    ('yield_certificate_in_output_file', bool),
    ('recall_data_assigned', bool),
    ('pt_formato_OK', int),
    ('pt_feasibility_OK', int),
    ('pt_consistency_OK', int),
    ('pt_tot', int),
    ('esercizio', int),
    ('task', int),
]

ENV = Env(args_list)
TAc = TALcolors(ENV, ENV["color_implementation"])
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg='now' if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

RO_io.check_access_rights(ENV, TALf, require_pwd=ENV['with_oracle'])
input_data_assigned = RO_io.dict_of_instance(PSL.instance_objects_spec, args_list, ENV)

PSL.check_instance_consistency(input_data_assigned)
request_dict, answer_dict, name_of, answ_obj, long_answer_dict, goals = RO_io.check_and_standardization_of_request_answer_consistency(ENV, PSL.answer_objects_spec, PSL.answer_objects_implemented)
all_data = {"input_data_assigned": input_data_assigned, "long_answer": long_answer_dict, "request": name_of}

all_data["oracle"] = PSL.solver(all_data)
SEF = RO_eval.std_eval_feedback(ENV, all_data["oracle"])
KingArthur = PSL.VerifySubmissionProblemSpecific(SEF, input_data_assigned, long_answer_dict)
all_data["feedback"] = KingArthur.verify_submission(SEF)

unasked_answ_objects = [key for key in all_data["oracle"] if key not in request_dict.values()]
for key in unasked_answ_objects:
    del all_data["oracle"][key]
RO_io.checker_reply(all_data, ENV)
if ENV.LOG_FILES is not None:
    RO_io.checker_logs(all_data, ENV, TALf)
if ENV["yield_certificate_in_output_file"]:
    RO_io.checker_certificates(all_data, ENV, TALf)
