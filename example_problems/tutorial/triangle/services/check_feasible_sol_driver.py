#!/usr/bin/env python3
from sys import stderr, exit
import random

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('silent',bool),
    ('display',bool),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TALf = TALfilesHelper(TAc, ENV)

#CHECK MIN_VAL <= MAX_VAL


seed = random.randint(100000,999999)
big_seed = random.randint(100000,999999)

    
if ENV['source'] != 'catalogue':
    # Get random instance
    n = random.randint(1,20)
    m = random.randint(1,20)
    path = tl.random_path(n,n)
    instance = tl.instances_generator(1, 1, 0, 99, n, n, m, m, 0, 99, seed, big_seed, path)[0]
    instance_str = tl.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"random_instance_{ENV['seed']}_{big_seed}.{ENV['instance_format']}.txt" 
else: # Get instance from catalogue
    instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=tl.format_name_to_file_extension(ENV["instance_format"],'instance'))
    instance = tl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
    output_filename = f"instance_{ENV['instance_id']}.{ENV['instance_format']}.txt"
    path = tl.random_path(instance['n'],instance['n'])
    print(path)

right_answer = "yes"
if random.randint(0,1):
    path += "L"
    right_answer = "no"
    
TAc.print(LANG.render_feedback("triangle-size","We have a triangle whose number of rows is:"), "white", ["bold"])
TAc.print(instance['n'], "yellow", ["bold"])
if ENV['display']:
    TAc.print(LANG.render_feedback("triangle-instance","Triangle instance of reference:"), "white", ["bold"])
    tl.print_triangle(instance['triangle'],ENV['instance_format'])
TAc.print(LANG.render_feedback("display-path", f'\nGiven this triangle, do you think the following path offers a feasible solution?'), "white", ["bold"])
TAc.print(path, "yellow", ["bold"])
TAc.print(LANG.render_feedback("prompt", f'\nType [yes/no] to answer.'), "white", ["bold"])
answer = TALinput(str, line_recognizer=lambda val,TAc,LANG: tl.check_yes_or_no_answer(val,TAc,LANG), TAc=TAc, LANG=LANG)[0]
if answer == right_answer:
    if not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("right-answer", f'# We agree, the answer is {right_answer}.'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-answer", f'# We don\'t agree, the answer is {right_answer}.'), "red", ["bold"])
exit(0)
