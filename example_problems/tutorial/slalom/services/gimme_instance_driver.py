#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

import lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('m',int),
    ('n',int),
    ('alphabet', str),
    ('opt_val',int),
    ('instance_format',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
if ENV['silent']:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

outputfile_extension=ll.format_name_to_file_extension(ENV['instance_format'], 'instance')
if ENV['source'] != 'catalogue':
    # Get random instance
    if ENV['source'] == 'randgen_1':
        instance = ll.instance_randgen_1(ENV['m'], ENV['n'], ENV['alphabet'], ENV['seed'])
    elif ENV['source'] == 'randgen_2':
        instance = ll.instance_randgen_2(ENV['m'], ENV['n'], ENV['opt_val'], ENV['alphabet'], ENV['seed'])
    else:
        assert False
    instance_str = ll.instance_to_str(instance, format_name=ENV['instance_format'])
    output_filename = f"instance_{ENV['m']}_{ENV['n']}_{ENV['seed']}.{ENV['instance_format']}.{outputfile_extension}"
else: # Get instance from catalogue
    instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=ll.format_name_to_file_extension(ENV["instance_format"],'instance'))
    instance = ll.get_instance_from_str(instance_str, instance_format_name=ENV['instance_format'])
    output_filename = f"instance_catalogue_{ENV['instance_id']}.{ENV['instance_format']}.{outputfile_extension}"

# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
else:
    TAc.print(LANG.render_feedback("instance-title", f'The first string of {len(instance[0])} character and the second string of {len(instance[1])} character are:'), "yellow", ["bold"])
    if ENV['display']:
        TAc.print(instance_str, "white", ["bold"])
        if ENV['source'] != 'catalogue':
            TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)
 
exit(0)
