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
    ('seed',str),
    ('big_seed',str),
    ('n',int),
    ('m',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('display',bool),
    ('display_sol',bool),
    ('silent',bool),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

#CHECK MIN_VAL <= MAX_VAL
if ENV['MIN_VAL'] > ENV['MAX_VAL']:
    TAc.NO()
    TAc.print(LANG.render_feedback("range-is-empty", f"Error: I can not choose the integers for the triangle from the range [{MIN_VAL},{MAX_VAL}] since this range is empty.", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
    exit(0)
    
# CHECK SIZES
if ENV["m"] < ENV["n"]:
    TAc.print(LANG.render_feedback("wrong-triangles-sizes", f'Error: the size of the bigger triangle ({ENV["n"]}) is smaller than the size of the smaller triangle ({ENV["n"]}).'), "red", ["bold"])
    exit(0)
    
if TALf.exists_input_file('instance'):
    instance = tl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
    TAc.print(LANG.render_feedback("successful-load", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])
elif ENV["source"] == 'terminal':
    instance = {}
    instance['n'] = ENV['n']
    instance['m'] = ENV['m']
    #first triangle
    TAc.print(LANG.render_feedback("waiting-first-line", f'#? waiting for the first string of the first triangle.\nFormat: the i-th line contains i elements\n'), "yellow")
    triangle = []
    for i in range(ENV['n']):
        TAc.print(LANG.render_feedback("insert-line", f'Enter line n. {i+1} containing {i+1} elements:'), "yellow", ["bold"]) 
        l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
        l = [int(x) for x in l]
        for el in l:
            if el < ENV['MIN_VAL'] or el > ENV['MAX_VAL']:
                TAc.NO()
                TAc.print(LANG.render_feedback("val-out-of-range", f"The value {el} falls outside the valid range [{ENV['MIN_VAL']},{ENV['MAX_VAL']}]."), "red", ["bold"])
                exit(0)
            if len(l) != i+1:
                TAc.NO()
                TAc.print(LANG.render_feedback("wrong-elements-number", f"Expected {i+1} elements for line {i+1}, but received {len(l)}."), "red", ["bold"])
                exit(0)
        triangle.append(l)
    instance['triangle'] = triangle
    # second triangle
    TAc.print(LANG.render_feedback("waiting-second-line", f'#? waiting for the first string of the second triangle.\nFormat: the i-th line contains i elements\n'), "yellow")
    big_triangle = []
    for i in range(ENV['m']):
        TAc.print(LANG.render_feedback("insert-line", f'Enter line n. {i+1} containing {i+1} elements:'), "yellow", ["bold"]) 
        l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
        l = [int(x) for x in l]
        for el in l:
            if el < ENV['MIN_VAL'] or el > ENV['MAX_VAL']:
                TAc.NO()
                TAc.print(LANG.render_feedback("val-out-of-range", f"The value {el} falls outside the valid range [{ENV['MIN_VAL']},{ENV['MAX_VAL']}]."), "red", ["bold"])
                exit(0)
            if len(l) != i+1:
                TAc.NO()
                TAc.print(LANG.render_feedback("wrong-elements-number", f"Expected {i+1} elements for line {i+1}, but received {len(l)}."), "red", ["bold"])
                exit(0)
        big_triangle.append(l)
    instance['big_triangle'] = big_triangle
    instance_str = tl.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"terminal_instance.{ENV['instance_format']}.txt" 
        
elif ENV["source"] == 'randgen_1':
    # Get random instance
    instance = tl.instances_generator(1, 1, ENV['MIN_VAL'], ENV['MAX_VAL'], ENV['n'], ENV['n'], ENV['m'], ENV['m'], ENV['seed'], ENV['big_seed'])[0]
    TAc.print(LANG.render_feedback("instance-generation-successful", f'The instance has been successfully generated by the pseudo-random generator {ENV["source"]} called with arguments:\nn={instance["n"]},\nm={instance["m"]},\nMIN_VAL={instance["MIN_VAL"]},\nMAX_VAL={instance["MAX_VAL"]},\nseed={instance["seed"]},\nbig_seed={instance["big_seed"]}'), "yellow", ["bold"])

else: # take instance from catalogue
    instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=tl.format_name_to_file_extension(ENV["instance_format"],'instance'))
    instance = tl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
    if "big_triangle" in instance.keys(): # check well formed instance
        TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback("instance-from-catalogue-not-successful", f'The instance with instance_id={ENV["instance_id"]} does not suit this service, as it contains just one triangle, while this service needs two triangles. We suggest you to look for double instances inside the catalogue.'), "red", ["bold"])
        exit(0)
        
big = tl.cast_to_array(instance['big_triangle'])
small = tl.cast_to_array(instance['triangle'])
L = len(instance['big_triangle'])
l = len(instance['triangle'])

right_answer, indexes = tl.num_of_occurrences(small,big,l,L)
            
if ENV["display"]:
    TAc.print(LANG.render_feedback("display-small",f'\nThe small triangle is displayed here:\n'), "green")
    tl.print_triangle(instance['triangle'],ENV['instance_format'])
    TAc.print(LANG.render_feedback("display-big",f'The big triangle is displayed here:\n'), "green")
    tl.print_triangle(instance['big_triangle'],ENV['instance_format'])
    
    
TAc.print(LANG.render_feedback("fit-question", f'\nGiven these triangles, how many times does the smaller one fit inside the bigger one?\nYour answer shall be a positive integer'), "green")
answer = TALinput(int, token_recognizer=lambda val,TAc,LANG: True, TAc=TAc, LANG=LANG)[0]
if answer == right_answer:
    if not ENV["silent"]:
        TAc.OK()
        if ENV["display_sol"]:
            if answer != 0:
                TAc.print(LANG.render_feedback("right-answer-display", f'We agree, the answer is {right_answer}, as you can see below.\n'), "green", ["bold"])
                tl.print_triangle_occurencies(instance['big_triangle'],sum(indexes,[]),ENV['instance_format'])
            else:
                TAc.print(LANG.render_feedback("right-answer", f'We agree, the answer is {right_answer}.\n'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("right-answer", f'We agree, the answer is {right_answer}.\n'), "green", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-answer", f'We don\'t agree, the answer is {right_answer}.'), "red", ["bold"])  
exit(0)

