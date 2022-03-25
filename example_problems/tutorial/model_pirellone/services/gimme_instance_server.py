#!/usr/bin/env python3
from sys import stderr, exit
from os import environ

from multilanguage import Env, Lang, TALcolors
from math_modeling import ModellingProblemHelper
from TALfiles import TALfilesHelper

import pirellone_lib as pl



# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('m',int),
    ('n',int),
    ('instance_id',int),
    ('instance_solvability',str),
    ('instance_format',str),
    ('silent',bool),
    ('display',bool),
    ('download',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:
extension=pl.format_name_to_file_extension(ENV['instance_format'], 'instance')
if ENV['source'] == 'catalogue':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format_name=extension)
    instance = pl.get_instance_from_str(instance_str, instance_format=ENV['instance_format'])
    m=len(instance)
    n=len(instance[1])
    output_filename = f"instance_catalogue_{ENV['instance_id']}.{ENV['instance_format']}.{extension}"

else:
    assert ENV['source'] == 'random'
    # Solvability
    if ENV['instance_solvability'] == 'solvable':
        ENV.arg['seed'] = pl.gen_instance_seed(solvable=True)
    elif ENV['instance_solvability'] == 'unsolvable':
        ENV.arg['seed'] = pl.gen_instance_seed(solvable=False)
    # Get pirellone
    try:
        instance = pl.gen_instance(ENV['m'], ENV['n'], ENV['seed'])
        instance_str = pl.instance_to_str(instance, instance_format=ENV['instance_format'])
        output_filename = f"instance_{ENV['m']}_{ENV['n']}_{ENV['seed']}.{ENV['instance_format']}.{extension}"
    except RuntimeError:
        TAc.print(LANG.render_feedback("error", f'It is not possible to generate an unsolvable {ENV["m"]}x{ENV["n"]} 0,1-matrix.'), "red", ["bold"])
        exit(0)


# Print Instance
if ENV['silent']:
    if ENV['display']:
        print(instance_str)
elif not ENV['source'] == 'catalogue':
    TAc.print(LANG.render_feedback("instance-title", f'The {ENV["m"]}x{ENV["n"]} 0,1-matrix is:'), "yellow", ["bold"])
    TAc.print(pl.instance_to_str(instance, instance_format=ENV["instance_format"]), "white", ["bold"])
    TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("instance-title", f'The {m}x{n} 0,1-matrix is:'), "yellow", ["bold"])
    TAc.print(instance_str, "white", ["bold"])

if ENV['download']:
    TALf.str2output_file(instance_str,output_filename)

exit(0)
