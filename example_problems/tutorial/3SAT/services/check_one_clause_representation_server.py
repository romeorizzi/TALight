#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="3SAT"
service="check_one_clause_representation"
args_list = [
    ('clause',str),
    ('representing_formula',str),
    ('lang',str),
]

from sys import stderr, exit, argv
import SAT_lib
from multilanguage import Env, Lang, TALcolors
import re
import itertools

def valid_cnf_string(string, regex):
    matches = re.match(regex,
        string)
    if(matches != None):
        if (matches.span()[1] == len(string)):
            return True
        else :
            error_position = matches.span()[1]
    else:
        error_position = 0
    TAc.print("Error found in the string at the position {}".format(error_position),"red")
    TAc.print(string[error_position:error_position + 50],"yellow")
    TAc.print("^","red")
    return False

def check_equivalence(cnf1, cnf2):
    literals1 = SAT_lib.get_literals(cnf1)
    literals2 = SAT_lib.get_literals(cnf2)
    if(len(literals1 - literals2)> 0):
        TAc.print("The second cnf should at least have te literals that are in the first one\n"
                  "In fact the second one doesn't have the literals:{}".format(literals1 - literals2),"green")
        exit()

    new_literals = literals2 - literals1
    literals1 = list(literals1)
    lit1_n = len(literals1)
    new_lit_n = len(new_literals)

    ass=set()
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
                readable_ass = '\n'.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), out_ass))))
                TAc.print("The two cnf are not equivalent", "red")
                TAc.print("For the assignment: \n{} \nthere is not an assignment for the variables set: {} such that"
                      " the cnf1:\n\t{}\nand the cnf2:\n\t{} \ngives as output the same result.\n"
                      "In fact the first one returns True while the second one returns always False no matter what value "
                      "we assign to the variables in the set: {}".
                      format(readable_ass, new_literals, SAT_lib.to_string(cnf1).replace("and ", "and\n\t"),
                             SAT_lib.to_string(cnf2).replace("and ", "and\n\t"), new_literals), "yellow")
                break
            if (found and not a):
                readable_ass = '\n'.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), ass))))
                TAc.print("The two cnf are not equivalent", "red")
                TAc.print("For the assignment: \n{} \n the cnf1:\n\t{}\nand the cnf2:\n\t{} \n are not equivalent.\n"
                          "In fact the second ones returns True while the first one returns False ".format(
                    readable_ass, SAT_lib.to_string(cnf1).replace("and ", "and\n\t"),
                                 SAT_lib.to_string(cnf2).replace("and ", "and\n\t")), "yellow")
        else:
            a = SAT_lib.check_sol(cnf1, out_ass)
            b = SAT_lib.check_sol(cnf2, out_ass)
            if (a != b):
                readable_ass = '\n'.join(sorted(set(map(lambda x: "\t" + x[0] + " = " + str(x[1]), out_ass))))
                TAc.print("The two cnf are not equivalent","red")
                TAc.print("For the assignment: \n{} \nt"
                      " the cnf1:\n\t{}\nand the cnf2:\n\t{} \ngives as output a different result.\n"
                      "In fact the first one returns {} while the second one returns {}.".
                      format(readable_ass, SAT_lib.to_string(cnf1).replace("and ", "and\n\t"),
                             SAT_lib.to_string(cnf2).replace("and ", "and\n\t"), a, b), "yellow")
                break
    TAc.print("\nCongraturation!!!\nThe two cnf are equivalent", "green")

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")

if (ENV['clause'] == 'lazy_input'):
    TAc.print("\nInsert first CNF:", "green")
    clause = input()
    if (not valid_cnf_string(clause,'^((\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*|lazy_input)')):
        exit(1)
else:
    clause = ENV['clause']

if (ENV['representing_formula'] == 'lazy_input'):
    TAc.print("\nInsert second CNF:", "green")
    representing_formula = input()
    if (not valid_cnf_string(representing_formula,'^(\s*\(\s*(\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*\)(\s*and\s*\(\s*(\s*!?\s*(x|y)[1-9])(\s*or\s*!?\s*(x|y)[1-9])*\s*\))*\s*|lazy_input)')):
        exit(1)
else:
    representing_formula = ENV['representing_formula']



cnf1 = SAT_lib.to_cnf(clause)
cnf2 = SAT_lib.to_cnf(representing_formula)
check_equivalence(cnf1, cnf2)