#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file

import model_lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('m',int), 
    ('n',int),
    ('alphabet', str),
    ('sol_style',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
if ENV['source'] == 'random':
    instance = ll.instance_randgen_1(ENV['m'], ENV['n'], ENV['alphabet'], ENV['seed'])

    TAc.print(LANG.render_feedback("seed", f"The seed is: {ENV['seed']}"), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {ENV["m"]} character and the second string of {ENV["n"]} character, over the alphabet {ENV["alphabet"]} are:'), "yellow", ["bold"])

    TAc.print(LANG.render_feedback("instance", f"{ll.instance_to_str(instance)}"), "white", ["bold"])

elif ENV['source'] == 'terminal':
    TAc.print(LANG.render_feedback("waiting", f'#? waiting for the first string of {ENV["m"]} character and the second string of {ENV["n"]} character, over the alphabet {ENV["alphabet"]}.\nFormat: the first line is the first string and the second line is the second string, each character must be separated by a space.\nAny line beggining with the "#" character is ignored.\nIf you prefer, you can use the "TA_send_txt_file.py" util here to send us the raw_instance of a file. Just plug in the util at the "rtal connect" command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.'), "yellow")
    TAc.print(LANG.render_feedback("instance-title", f"Enter the first string and then the second string:"), "yellow", ["bold"])

    alphabet = ll.get_alphabet(ENV['alphabet'])

    instance = list()
    instance.append([e for e in TALinput(str, num_tokens=ENV['m'], regex=f"^({'|'.join(e for e in alphabet)})$", sep=' ', TAc=TAc)])
    instance.append([e for e in TALinput(str, num_tokens=ENV['n'], regex=f"^({'|'.join(e for e in alphabet)})$", sep=' ', TAc=TAc)])

elif ENV['source'] == 'TA_send_files_bot':
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file. An example of the accepted files is `examples/instance.txt`)."), "yellow")

    instance_str = service_server_requires_and_gets_the_only_file().decode()
    instance = ll.get_instance_from_str(instance_str, "only_strings.txt")
    
    if len(instance[0]) != ENV['m']:
        TAc.print(LANG.render_feedback('error-s-length', f"#ERROR: The first string must have {ENV['m']} characters, you insert a string with {len(instance[0])} characters."), 'red', ['bold'])
        exit(0)
    if len(instance[1]) != ENV['n']:
        TAc.print(LANG.render_feedback('error-t-length', f"#ERROR: The second string must have {ENV['n']} characters, you insert a string with {len(instance[1])} characters."), 'red', ['bold'])
        exit(0)
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {ENV["m"]} character and the second string of {ENV["n"]} character are:'), "yellow", ["bold"])

    TAc.print(LANG.render_feedback("instance", f"{instance_str}"), "white", ["bold"])

max_len, an_opt_sol_annotated_subseq = ll.get_opt_val_and_sol(instance[0], instance[1])
TAc.print(LANG.render_feedback("solution-title", f"The solution for this instance is:"), "green", ["bold"])
if ENV['sol_style'] == 'subsequence':
    TAc.print(LANG.render_feedback("solution", f'{ll.sequence_to_str(ll.annotated_subseq_to_sequence(an_opt_sol_annotated_subseq))}'), "white", ["reverse"])
elif ENV['sol_style'] == 'annotated_subseq':
    TAc.print(LANG.render_feedback("legend-annotated_subseq", f"(LCS Character - First string index - Second string index)"), "white", ["bold"])
    TAc.print(LANG.render_feedback("solution", f'{ll.annotated_subseq_to_str(an_opt_sol_annotated_subseq)}'), "white", ["reverse"])

exit(0)
