#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem = "3SAT"
service = "check_f_representation"
args_list = [
    ('f_k', str),
    ('f_3', str),
    ('lang', str),
    ('ISATTY', bool),
]

from sys import stderr, exit, argv
import SAT_lib
from multilanguage import Env, Lang, TALcolors
import re
import itertools


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
                TAc.print("\n\n# The two cnf are not equivalent\n# For the assignment:", "red")
                TAc.print("# {}"
                          "\n# there is not an assignment for the variables set:"
                          "\n#\t{}"
                          "\n# such that the cnf1:"
                          "\n#\t{})"
                          "\n# and the cnf2:"
                          "\n#\t{}"
                          "\n# gives as output the same result."
                          .format(readable_ass, new_literals, SAT_lib.to_string(cnf1).replace("and ", "and\n#\t"),
                                  SAT_lib.to_string(cnf2).replace("and ", "and\n#\t")), "yellow"
                          )
                TAc.print("# In fact the first one returns True while the second one returns always False "
                          "\n# no matter what value we assign to the variables in the set: {}".format(new_literals),
                          "red")
                exit(1)
            if (found and not a):
                readable_ass = '\n#'.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), ass))))
                TAc.print("\n\n#The two cnf are not equivalent", "red")
                TAc.print(
                    "# For the assignment: \n#{} \n# the cnf1:\n#\t{}\n# and the cnf2:\n#\t{} \n# are not equivalent.".
                        format(readable_ass, SAT_lib.to_string(cnf1).replace("and ", "and\n#\t"),
                               SAT_lib.to_string(cnf2).replace("and ", "and\n#\t")), "yellow")
                TAc.print("# In fact the first returns False while the second one returns True.","red")
                exit(1)
        else:
            a = SAT_lib.check_sol(cnf1, out_ass)
            b = SAT_lib.check_sol(cnf2, out_ass)
            if (a != b):
                readable_ass = '\n#'.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), out_ass))))
                TAc.print("\n\n# The two cnf are not equivalent", "red")
                TAc.print("# For the assignment: \n#{} \n"
                          "# the cnf1:\n#\t{}\n# and the cnf2:\n#\t{} \n# gives as output a different result.".
                          format(readable_ass, SAT_lib.to_string(cnf1).replace("and ", "and\n#\t"),
                                 SAT_lib.to_string(cnf2).replace("and ", "and\n#\t")), "yellow")
                TAc.print("# In fact the first one returns {} while the second one returns {}.".format(a, b), "red")
                exit(1)
    TAc.print("\n# Congraturation!!!\n# The two cnf are equivalent", "green")


ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

if (ENV['f_k'] == 'lazy_input'):
    TAc.print("\n# Insert the K-SAT formula:", "green")
    clause = input()
    if (not valid_cnf_string(clause,
                             '^(\s*\(\s*(\s*!?\s*x[1-9])(\s*or\s*!?\s*x[1-9])*\s*\)(\s*and\s*\(\s*(\s*!?\s*x[1-9])(\s*or\s*!?\s*x[1-9])*\s*\))*\s*)')):
        exit(1)
else:
    clause = ENV['f_k']

if (ENV['f_3'] == 'lazy_input'):
    TAc.print("\n# Insert the 3-SAT formula:", "green")
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
        TAc.print("\n\n# The second cnf inserted is not a valid 3-SAT.\n"
                  "# In fact {} contains more than 3 literals".format(SAT_lib.to_string([disj])), "red")
        exit(1)

check_equivalence(cnf1, cnf2)
