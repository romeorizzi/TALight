#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_sol_set"
args_list = [
    ('feedback',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

stopping_command_set={"#end"}
print("#? waiting for your set of feasible treatments.\nPlease, each treatment should go on a different line and each line should have the same length and comprise only 'I' or 'H' characters.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

p = Flask(20)      
      
line = None
while line == None:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(I|H)*$", regex_explained="any string comprising of 'I' and 'H' characters.", TAc=TAc)
    if line == "#end":
        TAc.print(LANG.render_feedback("at-least-one-line", f'No. You are required to enter at least one feasible treatment before closing.'), "yellow")
        
input_solution_list = [line]
input_solution_set = {line}
if not recognize(input_solution_list[-1], TAc, LANG):
    TAc.print(LANG.render_feedback("first-line-not-feasible", f'No. Your very first treatment is not feasible.'), "red", ["bold"])
    exit(0)
len_lines = len(line)
n_pills = len_lines//2

while True:
    line, = TALinput(str, num_tokens=1, exceptions = stopping_command_set, regex="^(I|H)+$", regex_explained="any string of 'I' and 'H' characters.", TAc=TAc)
    if line in stopping_command_set:
        break
    if not len(line) == len_lines:
        TAc.print(LANG.render_feedback("different_lengths", f'No. Il trattamento che hai appena introdotto (tua riga {len(input_solution_list)+1}) è di lunghezza diversa dai precedenti.'), "red", ["bold"])
        exit(0)   
    if not recognize(line, TAc, LANG):
        exit(0)
    if line in input_solution_set:
        TAc.print(LANG.render_feedback("repeated", f'No. Il trattamento ammissibile che hai appena introdotto (tua riga {len(input_solution_list)+1}) è la stessa dell\'inserimento numero {input_solution_list.index(line)+1}. Nulla è perduto: questo doppio inserimento verrà ignorato. Puoi procedere.'), "red", ["bold"])
    else:
        input_solution_set.add(line)
        input_solution_list.append(line)

print("# FILE GOT")
TAc.print(LANG.render_feedback("your-treatments-all-ok", f'All the treatments you have introduced are feasible.'), "green")

input_solution_list.sort()
#print(input_solution_list)

if len(input_solution_list) == p.num_sol(n_pills):
    TAc.OK()
    TAc.print(f'Congrats! You have input all the feasible treatments on {n_pills} pills.', "green")
    exit(0)
else:
    TAc.print(LANG.render_feedback("one-treatment-is-missing-no-feedback", f'No. Your set is missing at least one feasible treatment.'), "red", ["bold"])
if ENV["feedback"] == "yes_no":
    exit(0)


for pos in range(p.num_sol(n_pills)):
    #print(f"pos={pos}, input_solution_list[pos]={input_solution_list[pos]}, p.unrank(n_pills, pos)={p.unrank(n_pills, pos)}")
    if input_solution_list[pos] != p.unrank(n_pills, pos):
        missing = p.unrank(n_pills, pos)
        #print(f"missing={missing}")
        if ENV["feedback"] == "give_one_missing":
            TAc.print(LANG.render_feedback("give-missing-treatment", f'Consider for example:'), "red", ["bold"])
            TAc.print(missing, "yellow", ["bold"])
        elif ENV["feedback"] == "tell_a_minimal_missing_prefix":
            min_len1 = 0
            if pos > 0:
                while missing[min_len1] == input_solution_list[pos-1][min_len1]:
                    min_len1 += 1

            min_len2 = 0
            if pos < len(input_solution_list):
                while missing[min_len2] == input_solution_list[pos][min_len2]:
                    min_len2 += 1
            minimal_missing_prefix = missing[0:1+max(min_len1,min_len2)]
            TAc.print(LANG.render_feedback("one-missing-minimal-prefix", f'As a strong hint, here is the prefix of a feasible treatment and no treatment in your set has this prefix:'), "red", ["bold"])
            TAc.print(minimal_missing_prefix, "yellow", ["bold"])
        exit(0)
