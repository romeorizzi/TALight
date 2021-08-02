#!/usr/bin/env python3
from sys import stderr, exit, argv
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from hanoi_lib import ConfigGenerator



# METADATA OF THIS TAL_SERVICE:
problem="hanoi"
service="gen_random_puzzle"
args_list = [
    ('n',int),
    ('seed',int),
    ('start', str),
    ('final', str),
    ('verbose',int),
    ('lang',str),
    ('ISATTY',bool),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
# LANG.manage_opening_msg()


# INITIALIZATION
# get seed
seed = ENV['seed']
if seed == -1:
    seed = random.randint(1,9) * 100000
    seed += random.randint(0, 99999)
    if ENV['verbose'] == 1:
        TAc.print(LANG.render_feedback("print-seed", f"seed = {seed}"), "yellow", ["bold"])
if ENV['verbose'] == 2:
    TAc.print(LANG.render_feedback("print-seed", f"seed = {seed}"), "yellow", ["bold"])

# get type of configurations
gen = ConfigGenerator(seed)
start = gen.getRandom(ENV['n'])
final = gen.getRandom(ENV['n'])

TAc.print(LANG.render_feedback("print-configs", f"# start: {start}\n# final: {final}"), "green", ["bold"])
TAc.print(LANG.render_feedback("print-configs-arg", f"-astart={start} -afinal={final}"), "yellow", ["bold"])

exit(0)