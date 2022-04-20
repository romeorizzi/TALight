#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_string',str),
    ('with_output_files',bool),
    ('solution_string',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

TAc.print(LANG.render_feedback("ciao", 'Ciao.'), "yellow", ["bold"])
print(f'{ENV["instance_string"]=}')
print(f'{ENV["solution_string"]=}')

if ENV.LOG_FILES == None:
    print("Servizio chiamato senza access token")
else:
    print("Servizio chiamato con access token")
    TALf.str2log_file(content='Scrivo questo in un file di log.', filename=f'LOG_filename', timestamped = False)

if ENV["with_output_files"]:    
    print("Al servizio è stato richiesto di generare files nel folder di output")
    TALf.str2output_file(content='Scrivo questo in un output file.', filename=f'OK_{ENV["instance_id"]}', timestamped = False)
else:
    print("Al servizio non è stato richiesto di generare files nel folder di output")

if TALf.exists_input_file('optional_filehandler1'):
    file1_content_as_string = TALf.input_file_as_str('optional_filehandler1')
    print(f"You passed a file on `optional_filehandler1` and here is its content:\nBEGIN\n{file1_content_as_string}END")
else:
    print(f"You passed no file on `optional_filehandler1`")
