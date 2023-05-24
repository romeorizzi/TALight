#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from bot_file_exchange_sym_interface import service_server_requires_and_gets_the_only_file

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
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file. An example of the accepted files are `examples/instance_with_solution_subsequence.txt` and `examples/instance_with_solution_annotated_subseq.txt`."), "yellow")

    instance_str = service_server_requires_and_gets_the_only_file().decode()
    instance_with_solution = ll.get_instance_from_str(instance_str, "only_strings.txt")

    if len(instance_with_solution[0]) != ENV['m']:
        TAc.print(LANG.render_feedback('error-s-length', f"#ERROR: The first string must have {ENV['m']} characters, you insert a string with {len(instance_with_solution[0])} characters."), 'red', ['bold'])
        exit(0)
    if len(instance_with_solution[1]) != ENV['n']:
        TAc.print(LANG.render_feedback('error-t-length', f"#ERROR: The second string must have {ENV['n']} characters, you insert a string with {len(instance_with_solution[1])} characters."), 'red', ['bold'])
        exit(0)

    TAc.print(LANG.render_feedback("instance", f'The first string and the second string are:\n{ll.sequence_to_str(instance_with_solution[0])}\n{ll.sequence_to_str(instance_with_solution[1])}'), "yellow", ["bold"]) 

    if ENV['sol_style'] == 'subsequence':
        TAc.print(LANG.render_feedback("user-sol", f'Your solution is:\n{ll.sequence_to_str(instance_with_solution[2])}'), "yellow", ["bold"]) 
        if ll.check_sol_feas_and_opt(TAc, LANG, ENV, instance_with_solution[2], instance_with_solution[0], instance_with_solution[1]):
            TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done! You have found the Longest Common Subsequence.'), "green", ["bold"]) 
        exit(0)

    if ENV['sol_style'] == 'annotated_subseq':
        user_sol ={}
        for line in instance_with_solution[2:]:
            if ll.check_input(TAc, LANG, ENV, line):
                user_sol[(int(line[1]), int(line[2]))] = line[0]
        TAc.print(LANG.render_feedback("user-sol", f'Your solution is:\n{ll.annotated_subseq_to_str(user_sol)}'), "yellow", ["bold"]) 
        if ll.check_sol_feas_and_opt(TAc, LANG, ENV, user_sol, instance_with_solution[0], instance_with_solution[1]):
            TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done! You have found the Longest Common Subsequence.'), "green", ["bold"]) 
        exit(0)

alphabet = ll.get_alphabet(ENV['alphabet'])

if ENV['sol_style'] == 'subsequence':
    TAc.print(LANG.render_feedback("user_sol", 'Insert your solution: '), "yellow", ["bold"]) 
    line = TALinput(
        str,
        regex=f"^({'|'.join(e for e in alphabet)})$",
        TAc=TAc,
        regex_explained="the whole longest common subsequence without spaces between characters."
    )
    user_sol = line

if ENV['sol_style'] == 'annotated_subseq':
    user_sol={}
    line = " "
    TAc.print(LANG.render_feedback("waiting", f'#? waiting for your solution.\nFormat: char index_s index_t, where `char` is the single common charater, index_s is its index in the first string, index_t is its index in the second string, each element must be separated by a space.\nWhen you have finished, enter `#end`.'), "yellow")
    while line[0] != "#end":
        line = TALinput(
            str,
            num_tokens=3,
            exceptions = "#end",
            regex=f"^({'|'.join(e for e in alphabet)}|[0-{ENV['m']}]|[0-{ENV['n']}])$",
            TAc=TAc,
            regex_explained="the common single character followed by its index in the first string and then its index in the second string, one per line."
        )
        if line[0] != "#end":
            if ll.check_input(TAc, LANG, ENV, line):
                user_sol[(int(line[1]), int(line[2]))] = line[0]

if ll.check_sol_feas_and_opt(TAc, LANG, ENV, user_sol, instance[0], instance[1]):
    TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done! You have found the Longest Common Subsequence.'), "green", ["bold"]) 

exit(0)
