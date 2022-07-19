#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import collage_lib as cl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('seq_len',int),
    ('num_col',int),
    ('mod',int),
    ('seed',str),
    ('download',bool),
    ('lang',str)
]

# Max sequence length and max colors number in the sequence
MAX_SEQ_LEN = 1000
MAX_NUM_COL = 256

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)


# START CODING YOUR SERVICE:

#Check if the choosen number of colours is bigger than MAX_NUM_COL
if ENV['num_col'] > MAX_NUM_COL:
  TAc.NO()
  TAc.print(LANG.render_feedback("color-limit-exceeded", f"Error: the maximum number of colors must be lower or equal than {MAX_NUM_COL}!", {"MAX_NUM_COL":MAX_NUM_COL}), "red", ["bold"])
  exit(0)

# Check the size of the sequence
if ENV["seq_len"] > MAX_SEQ_LEN:
  TAc.print(LANG.render_feedback("wrong-sequence-length", f'Error: the lenght of the sequence ({ENV["seq_len"]}) exceeded the limit ({MAX_SEQ_LEN}).'), "red", ["bold"])
  exit(0)

## Input Sources
if TALf.exists_input_file('instance'):
  instance = cl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("successful-load", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])

elif ENV["source"] == 'terminal':
  instance = {}
  instance['seq_len'] = ENV['seq_len']
  instance['num_col'] = ENV['num_col']

  rainbow = []
  TAc.print(LANG.render_feedback("waiting-line", f'#? waiting for the color stripes.\nFormat: numbers separated by spaces\n'), "yellow")

  TAc.print(LANG.render_feedback("insert-line", f'Enter sequence containing {ENV["seq_len"]} stripes:'), "yellow", ["bold"])
  l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
  l = [int(x) for x in l]

  for el in l:
    if el < 0 or el > ENV['num_col']:
      TAc.NO()
      TAc.print(LANG.render_feedback("val-out-of-range", f"The value {el} falls outside the valid range [1,{MAX_NUM_COL}]."), "red", ["bold"])
      exit(0)

    if len(l) != ENV['seq_len']:
      TAc.NO()
      TAc.print(LANG.render_feedback("wrong-elements-number", f"Expected elements for line, but received {len(l)}."), "red", ["bold"])
      exit(0)

  rainbow.append(l)
    
  instance['rainbow'] = rainbow[0]
  instance_str = cl.instance_to_str(instance, format_name=ENV['instance_format'])
  output_filename = f"terminal_instance.{ENV['instance_format']}.txt"

elif ENV["source"] == 'randgen_1':
  if ENV['mod'] == -1:
    mod = random.choice([1,2])
  else:
    mod = ENV['mod']

  # Get random instance
  #instance = cl.instances_generator(1, 1, ENV['seq_len'], ENV['num_col'], ENV['mod'], ENV['seed'])[0]
  instance = cl.instances_generator(1, 1, ENV['seq_len'], ENV['num_col'], mod, ENV['seed'])[0]
  # TAc.print(LANG.render_feedback("instance-generation-successful", f'The instance has been successfully generated by the pseudo-random generator {ENV["source"]} called with arguments:\nseq_len={instance["seq_len"]},\nnum_col={instance["num_col"]},\nmod={instance["mod"]}\nseed={instance["seed"]}'), "yellow", ["bold"])

else: # take instance from catalogue
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=cl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = cl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])

TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"])
TAc.print(cl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"])

content = cl.solutions(instance,ENV['instance_format'])

TAc.print(LANG.render_feedback("all-solutions-title", f"Here are the solutions for the given instance:"), "green", ["bold"])

for key in content.keys():
  TAc.print(LANG.render_feedback("solutions", f'Solution for service {key}: {content[key]}'), "white",["bold"])

if ENV["download"]:
  TALf.str2output_file(content,f'all_solutions.txt')

exit(0)
