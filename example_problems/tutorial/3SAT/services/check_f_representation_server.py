#!/usr/bin/env python3
from sys import stderr, exit
import re
import itertools

from multilanguage import Env, Lang, TALcolors

import SAT_lib

# METADATA OF THIS TAL_SERVICE:
problem = "3SAT"
service = "check_f_representation"
args_list = [
    ('f', str),
    ('f_3', str),
    ('lang', str),
]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
def valid_cnf_string(string, regex):
    matches = re.match(regex,
                       string)
    if (matches != None):
        if (matches.span()[1] == len(string)):
            return True
        else:
            error_position = matches.span()[1]
    else:
        error_position = 0
    TAc.print("\n\n# Error found in the string at the position {}".format(error_position), "red")
    TAc.print("# " + string[error_position:error_position + 50], "yellow")
    TAc.print("# ^", "red")
    return False


def check_equivalence(cnf1, cnf2):
    literals1 = SAT_lib.get_literals(cnf1)
    literals2 = SAT_lib.get_literals(cnf2)

    new_literals = literals2 - literals1
    literals1 = list(literals1)
    lit1_n = len(literals1)
    new_lit_n = len(new_literals)

    ass = set()
    for out_seq in itertools.product([True, False], repeat=lit1_n):
        out_ass = list(zip(literals1, out_seq))
        if new_lit_n > 0:
            found = False
            a = SAT_lib.check_sol(cnf1, out_ass)
            for inn_seq in itertools.product([True, False], repeat=new_lit_n):
                inn_ass = list(zip(new_literals, inn_seq))
                ass = set(out_ass + inn_ass)
                if SAT_lib.check_sol(cnf2, ass):
                    found = True
                    break
            if a and not found:
                readable_ass = '\n#'.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), out_ass))))
                TAc.print(
                    "# Your 3CNF f_3 does not offer a representation of your CNF f as the prescribed property is not met.",
                    "red")
                TAc.print(
                    "# Indeed, for the assignment: \n# {} \n# the CNF f evaluates to True but the 3CNF f_3 evaluates "
                    "to False no matter how this assignment is extended on the variables in the set {}.\n".
                        format(readable_ass, new_literals), "yellow")
                exit(1)
            if (found and not a):
                readable_ass = '\n# '.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), ass))))
                TAc.print(
                    "# Your 3CNF f_3 does not offer a representation of your CNF f as the prescribed property is not met.",
                    "red")
                TAc.print(
                    "# Indeed, for the assignment: \n# {} \n# the CNF f evaluates to False whereas the 3CNF f_3 evaluates to True.\n".
                        format(readable_ass), "yellow")
                exit(1)
        else:
            a = SAT_lib.check_sol(cnf1, out_ass)
            b = SAT_lib.check_sol(cnf2, out_ass)
            if (a != b):
                readable_ass = '\n# '.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), out_ass))))
                TAc.print(
                    "# Your 3CNF f_3 does not offer a representation of your CNF f as the prescribed property is not met.",
                    "red")
                TAc.print("# Indeed, for the assignment: \n#{} \n"
                          "# the CNF f returns {} while the 3CNF f_3 one returns {}.".
                          format(readable_ass, a, b), "yellow")
                exit(1)
    TAc.print("\n# Congratulation!!!", "green")
    TAc.print(
        "Your 3CNF f_3 offers a faithful representation of your CNF f in the sense that the following property holds "
        "for every truth assignment x* for the x variables: f evaluates to true under x* iif there exists a truth"
        " assignment y* of the y variables such that f_3 evaluates to true under (x*,y*).")


if (ENV['f'] == 'lazy_input'):
    TAc.print("\n# Insert your CNF f:", "green")
    clause = input()
    if (not valid_cnf_string(clause,
                             '^(\s*\(\s*(\s*!?\s*x[1-9])(\s*or\s*!?\s*x[1-9])*\s*\)(\s*and\s*\(\s*(\s*!?\s*x[1-9])(\s*or\s*!?\s*x[1-9])*\s*\))*\s*)')):
        exit(1)
else:
    clause = ENV['f']

if (ENV['f_3'] == 'lazy_input'):
    TAc.print("\n# Insert your 3CNF f_3:", "green")
    representing_formula = input()
    if (not valid_cnf_string(representing_formula,
                             '^(\s*\(\s*(\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*\)(\s*and\s*\(\s*(\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*\))*\s*)')):
        exit(1)
else:
    representing_formula = ENV['f_3']

cnf1 = SAT_lib.to_cnf(clause)
cnf2 = SAT_lib.to_cnf(representing_formula)
for disj in cnf2:
    if len(disj) > 3:
        TAc.print("\n\n# The 3CNF f_3 inserted is not a valid 3-SAT.\n"
                  "# In fact {} contains more than 3 literals".format(SAT_lib.to_string([disj])), "red")
        exit(1)

check_equivalence(cnf1, cnf2)
