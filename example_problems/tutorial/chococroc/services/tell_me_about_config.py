import sys
from chococroc_lib import build_table
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="tell_me_about_config"
args_list = [
    ('m',int),
    ('n',int),
    ('info_requested',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#print(f"# I will serve: problem=chococroc, service=tell_me_about_config")

# START CODING YOUR SERVICE:
rowM = ENV['m']
columnN = ENV['n']
info_requested = ENV['info_requested']
lang = ENV['lang']

TAc.print(LANG.render_feedback("explain configuration", f'Your initial configuration is {rowM} x {columnN}.\nTo work on this problem and understand the underlying mechanism you have different problems available'), "yellow", ["bold"])

if(info_requested == "won_or_lost"):
    TAc.print(LANG.render_feedback("explain configuration", f'service check_is_winning: to find out if your bet of winning for your configuration is a winning one or a losing one;\nservice check_is_losing: to find out if your bet of losing for your configuration is a winning one or a losing one'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("explain configuration", f'service chek_grundy_value: to find out if the grundy value you assumed for your configuration is correct or not'), "yellow", ["bold"])




exit(0)
