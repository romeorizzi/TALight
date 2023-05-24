#!/usr/bin/env python3
from sys import stderr, exit
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator



# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n_instances',int),
    ('start', str),
    ('final', str),
    ('n',int),
    ('verbose',int),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never' if ENV["verbose"] < 2 else 'delayed')


# INITIALIZATION
# get seed
seed = ENV['seed']
if seed == 'random_seed':
    seed = random.randint(100000, 999999)
    if ENV['verbose'] == 1:
        TAc.print(LANG.render_feedback("print-seed", f"seed = {seed}"), "yellow", ["bold"])
else:
    seed = int(seed)
if ENV['verbose'] == 2:
    TAc.print(LANG.render_feedback("print-seed", f"seed = {seed}"), "yellow", ["bold"])

# get type of configurations
gen = ConfigGenerator(seed)


for _ in range(ENV['n_instances']):
    start = gen.getRandom(ENV['n'])
    final = gen.getRandom(ENV['n'])

    TAc.print(LANG.render_feedback("print-configs", f"# start: {start}\n# final: {final}"), "green", ["bold"])
    TAc.print(LANG.render_feedback("print-configs-arg", f"-astart={start} -afinal={final}"), "yellow", ["bold"])

exit(0)
