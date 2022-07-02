#!/usr/bin/env python3
from sys import exit, stderr, stdout

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('msg',str),
    ('ping_via',str),
    ('bounch_on',str),
    ('with_opening_message',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now'if ENV['with_opening_message'] else 'never')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

if ENV['ping_via'] == 'TALight_argument':
    msg = ENV['msg']
elif ENV['ping_via'] == 'stdin_dry':
    msg=input()
elif ENV['ping_via'] == 'stdin_interactive':
    print(LANG.render_feedback("prompt", 'Insert your ping message:'), end=' ')
    msg=input()
else:
    assert ENV['ping_via'] == 'file'
    if TALf.exists_input_file('file_with_msg'):
        msg = TALf.input_file_as_str('file_with_msg')
    else:
        for fout in [stdout,stderr]:
            print(LANG.render_feedback("error-no-file", 'You called me with argument `ping_via` set to `file`, but forgot to attach a file to the `file_with_msg` filehandler when issuing your call to this ping service.'), file=fout)
        exit(1)

reply = "You sent me the string:\n" + msg
if ENV['bounch_on'] == 'stdout':
    print(reply)
elif ENV['bounch_on'] == 'stderr':
    print(reply, file=stderr)
else:
    assert ENV['bounch_on'] == 'file'
    TALf.str2output_file(reply,f'pong.txt')
exit(0)
