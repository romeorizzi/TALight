#!/usr/bin/env python3
from sys import stderr, exit
import re
import itertools
import random

from multilanguage import Env, Lang, TALcolors

import SAT_lib

# METADATA OF THIS TAL_SERVICE:

problem = "3SAT"
service = "eval_f_rep"
args_list = [
    ('k', int),
    ('size', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring:  eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

def input_is_valid(string, regex):
    matches = re.match(regex,
                       string)
    if (matches != None):
        if (matches.span()[1] == len(string)):
            return True
        else:
            error_position = matches.span()[1]
    else:
        error_position = 0
    print("\n\n# Error found in the string at the position {}".format(error_position),"red")
    print("# "+string[error_position:error_position + 50], "yellow")
    print("# ^", "red")
    return False



def check_if_3cnf(cnf):
    for disj in cnf:
        if len(disj) > 3:
            TAc.print("\n\n# The 3CNF f_3 inserted is not a valid 3-SAT.\n"
                      "# In fact {} contains more than 3 literals".format(SAT_lib.to_string([disj])), "red")
            exit(1)
    return cnf

def round1_2(cnf):
    TAc.print("# Here's a CNF. Can you give me an equivalent 3CNF ones?\n1\n{}".format(SAT_lib.to_string(cnf)), "green")
    T_f = input()
    if (not input_is_valid(T_f,
                             '^(\s*\(\s*(\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*\)(\s*and\s*\(\s*(\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*\))*\s*)')):
        exit(1)
    return check_if_3cnf(SAT_lib.to_cnf(T_f))

def round3(cert):
    TAc.print("# Thanks for your CNF. Here's a certificate for the original one."
    "\n# Can you give me a certificate that is valid for yours CNF ?\n2\n{}".format(cert), "green")
    cert = input()
    if (not input_is_valid(cert,
                             "^\s*{\s*\(\s*'(x|y)[0-9]+'\s*,\s*(True|False)\s*\)\s*(,\s*\(\s*'(x|y)[0-9]+'\s*,\s*(True|False)\s*\)\s*)*}\s*")):
        exit(1)

    return SAT_lib.parse_certificate(cert)

def round4(cnf_yes, cert):
    users_yes_cnf = round1_2(cnf_yes)
    TAc.print("# Thanks for your CNF. Here's an assignment that satisfy your CNF.\n# Can you give me a certificate that is valid for my CNF ?\n3\n{}".format(cert), "green")
    cert = input()
    if (not input_is_valid(T_f,"^\s*{\s*\(\s*'(x|y)[0-9]+'\s*,\s*(True|False)\s*\)\s*(,\s*\(\s*'(x|y)[0-9]+'\s*,\s*(True|False)\s*\)\s*)*}\s*")):
        exit(1)
    return SAT_lib.parse_certificate(cert)


k = ENV['k']
size = ENV['size']

cnf_file = "services/sat_database/{}/{}/{}/cnf.cnf"
cert_file = "services/sat_database/yes/{}/{}/solution.txt"

cnf_file_yes = cnf_file.format("yes",size,k)
cert_file_yes = cert_file.format(size,k)
cnf_file_no = cnf_file.format("no",size,k)

cnf_yes = SAT_lib.dimacs_file_to_cnf(cnf_file_yes)
cnf_no = SAT_lib.dimacs_file_to_cnf(cnf_file_no)
cert_yes = SAT_lib.saved_certificate_to_cnf(cert_file_yes)


users_yes_cnf = []
users_no_cnf = []

users_yes_cnf = round1_2(cnf_yes)
users_no_cnf = round1_2(cnf_no)
users_yes_cnf = (round1_2(cnf_yes),users_yes_cnf)[random.randint(0, 1)]
users_yes_cert = round3(cert_yes)

if(not SAT_lib.check_sol(users_yes_cnf,users_yes_cert)):
    TAc.print("# The certificate that you gave me is not a valid one for your CNF", "red")
    quit(0)

users_yes_cert = round4(cnf_yes, users_yes_cert)

if(not SAT_lib.check_sol(cnf_yes,users_yes_cert)):
    TAc.print("# The certificate that you gave me is not a valid one for my CNF", "red")
    quit(0)
