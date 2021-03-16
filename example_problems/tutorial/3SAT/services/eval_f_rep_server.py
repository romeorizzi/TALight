#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem = "3SAT"
service = "eval_f_rep"
args_list = [
    ('k', int),
    ('size', str),
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
    TAc.print("# "+string[error_position:error_position + 50], "yellow")
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
                TAc.print("# The two cnf are not equivalent", "red")
                TAc.print(
                    "# For the assignment: \n# {} \n# there is not an assignment for the variables set: {} such that"
                    "# the K-SAT formula:\n#\t {}\n# and the 3-SAT formula:\n#\t{} \n# gives as output the same result.\n"
                    "# In fact the first one returns True while the second one returns always False no matter what value "
                    "we assign to the variables in the set: {}".
                        format(readable_ass, new_literals, SAT_lib.to_string(cnf1).replace("and ", "and\n#\t"),
                               SAT_lib.to_string(cnf2).replace("and ", "and\n#\t"), new_literals), "yellow")
                exit(1)
            if (found and not a):
                readable_ass = '\n# '.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), ass))))
                TAc.print("#  The two cnf are not equivalent", "red")
                TAc.print(
                    "#  For the assignment: \n# {} \n# the K-SAT formula:\n#\t{}\n# and the 3-SAT formula:\n#\t{} \n# are not equivalent.\n"
                    "# In fact the first returns False while the second one returns True.".format(
                        readable_ass, SAT_lib.to_string(cnf1).replace("and ", "and\n#\t"),
                        SAT_lib.to_string(cnf2).replace("and ", "and\n#\t")), "yellow")
                exit(1)
        else:
            a = SAT_lib.check_sol(cnf1, out_ass)
            b = SAT_lib.check_sol(cnf2, out_ass)
            if (a != b):
                readable_ass = '\n# '.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), out_ass))))
                TAc.print("# The two cnf are not equivalent", "red")
                TAc.print("# For the assignment: \n#{} \n"
                          "# the K-SAT formula:\n#\t{}\n# and the 3-SAT formula:\n#\t{} \n# gives as output a different result.\n"
                          "# In fact the first one returns {} while the second one returns {}.".
                          format(readable_ass, SAT_lib.to_string(cnf1).replace("and ", "and\n\t"),
                                 SAT_lib.to_string(cnf2).replace("and ", "and\n#\t"), a, b), "yellow")
                exit(1)


ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

k = ENV['k']
size = ['tiny', 'small', 'medium', 'large'].index(ENV['size'])
ksat = SAT_lib.random_kcnf(k * pow(2, size), k)
(solvable, certificate) = SAT_lib.solve(ksat)

if solvable:
    TAc.print("\n# Here's a {}-SAT formula and a certificate that show that it's solvable.\n"
              "# Give me an equivalent 3-SAT formula and a certificate that show that your 3-SAT "
              "is solvable\n\n{}\n\n{}".format(k, SAT_lib.to_string(ksat), certificate), "green")
else :
    TAc.print("\n#Give me a 3-SAT formula that is equivalent to this {}-SAT:\n".format(k, SAT_lib.to_string(ksat).replace("and ", "and\n#\t")), "green")

three_cnf = input()
if solvable:
    three_cnf_certificate = SAT_lib.parse_certificate(input())

if (not valid_cnf_string(three_cnf,
                         '^(\s*\(\s*(\s*!?\s*(x|y)[0-9]*)(\s*or\s*!?\s*(x|y)[0-9]*)*\s*\)(\s*and\s*\(\s*(\s*!?\s*(x|y)[0-9]*)(\s*or\s*!?\s*(x|y)[0-9]*)*\s*\))*\s*)')):
    exit(1)
three_cnf = SAT_lib.to_cnf(three_cnf)

for disj in three_cnf:
    if len(disj) > 3:
        TAc.print("\n\n# The second cnf inserted is not a valid 3-SAT.\n"
                  "# In fact {} contains more than 3 literals".format(SAT_lib.to_string([disj])), "red")
        exit(1)

check_equivalence(ksat, three_cnf)

if solvable:
    if SAT_lib.check_sol(three_cnf, three_cnf_certificate):
        TAc.print("\n# Congraturation!!!\n# The two cnf are equivalent and the certificate given is valid", "green")
    else:
        TAc.print("\n# The two cnf are equivalent but the certificate given is not valid", "yellow")
        exit(1)
else:
    TAc.print("\n# Congraturation!!!\n# The two cnf are equivalent", "green")

if solvable:
    (_, three_cnf_certificate) = SAT_lib.solve(three_cnf)
    TAc.print("\n# Can you give me a certificate for my {}-SAT formula starting from this certificate"
              " that satisfy your 3-SAT?\n#{}\n".format(k,three_cnf_certificate), "green")

    certificate = SAT_lib.parse_certificate(input())

    ksat_lit = SAT_lib.get_literals(ksat)
    for ass in three_cnf_certificate:
        if ass[0] in ksat_lit:
            if ass not in certificate:
                TAc.print("\n# You should use {} in your certificate for the K-SAT".format(ass),"green")
                exit(1)

    if SAT_lib.check_sol(ksat, certificate):
        TAc.print("\n# Congraturation!!!\n# Your certificate satisfy the {}-SAT".format(k), "green")
    else:
        TAc.print("\n# Your certificate does not satisfy the {}-SAT".format(k), "yellow")
        exit(1)
