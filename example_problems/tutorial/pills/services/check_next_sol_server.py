#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_next_sol"
args_list = [
    ('current_sol',str),
    ('next_sol',str),
    ('sorting_criterion',str),
    ('tell_maximal_correct_feedback',bool),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if ( not recognize(ENV['current_sol'], TAc, LANG)
     or not recognize(ENV['next_sol'], TAc, LANG)
   ):
    exit(0)
if len(ENV['current_sol']) != len(ENV['next_sol']):
    TAc.print(LANG.render_feedback("different-n", f'No. The two treatments you have provided have different lengths! As such, they do not belong to the same list.'), "red", ["bold"])
    exit(0)
        
n_pills = len(ENV['current_sol'])//2 
p = Flask(n_pills)

if p.rank(ENV['current_sol'], sorting_criterion=ENV['sorting_criterion']) == p.num_sol(n_pills) -1:
    TAc.NO()
    TAc.print('Be told that your treatment current_sol is the very last in the list', "red")
    exit(0)
true_next = p.unrank(n_pills, 1+p.rank(ENV['current_sol'], sorting_criterion=ENV['sorting_criterion']), sorting_criterion=ENV['sorting_criterion'])
if ENV['next_sol'] == true_next:
    if not ENV['silent']:
        TAc.OK()
        print(LANG.render_feedback("next-ok", f'♥  The next_sol treatment is indeed the treatment that comes just after the current_sol treatment (according to sorting_criterion={ENV["sorting_criterion"]}).'))
    exit(0)

# INDEPTH NEGATIVE FEEDBACK:
TAc.print(LANG.render_feedback("next-wrong", f'No. The next_sol treatment you have provided is NOT the treatment coming just after the current_sol treatment according to sorting_criterion={ENV["sorting_criterion"]}.'), "red", ["bold"])
if ENV['tell_maximal_correct_feedback']:
    print(LANG.render_feedback("feedback", f'The maximal prefix of your next_sol treatment that is actually correct is the following:'))
    maximal_correct = ''
    for c1, c2 in zip(true_next, ENV['next_sol']):
        if c1 == c2:
          maximal_correct += c1
        else:
          break
    TAc.print(maximal_correct, "yellow", ["bold"])
exit(0)
