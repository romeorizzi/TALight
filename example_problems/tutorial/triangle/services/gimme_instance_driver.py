#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper


import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('m',int), 
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('seed',str),
    ('big_seed',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TALf = TALfilesHelper(TAc, ENV)

if ENV['silent']:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if ENV['source'] != 'catalogue':
    # Get random instance
    instance = tl.instances_generator(1, 1, ENV['MIN_VAL'], ENV['MAX_VAL'], ENV['n'], ENV['n'], ENV['m'], ENV['m'], ENV['seed'], ENV['big_seed'])[0]
    instance_str = tl.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"random_instance_{ENV['seed']}_{ENV['big_seed']}.{ENV['instance_format']}.txt" 
else: # Get instance from catalogue
    instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=tl.format_name_to_file_extension(ENV["instance_format"],'instance'))
    instance = tl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
    output_filename = f"instance_{ENV['instance_id']}.{ENV['instance_format']}.txt"

# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'This is the instance:\n'), "yellow", ["bold"])
    if ENV['display']:
        TAc.print(instance_str, "white", ["bold"])
        if ENV['source'] != 'catalogue': # display random instance
            output = ""
            if ENV['m'] != 0:
                output += f'The parameters encoding this instance are:\nn: {ENV["n"]}\nseed: {ENV["seed"]}\nm: {ENV["m"]}\nbig_seed: {instance["big_seed"]}\nMIN_VAL: {ENV["MIN_VAL"]}\nMAX_VAL: {ENV["MAX_VAL"]}'  
            else:
                output += f'\nThe parameters encoding this instance are:\nn: {ENV["n"]}\nseed: {ENV["seed"]}\nMIN_VAL: {ENV["MIN_VAL"]}\nMAX_VAL: {ENV["MAX_VAL"]}'          
            TAc.print(LANG.render_feedback("output-instance", output), "yellow", ["bold"])
if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)
