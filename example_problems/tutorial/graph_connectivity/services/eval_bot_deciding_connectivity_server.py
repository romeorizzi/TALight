#!/usr/bin/env python3

from re import M
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import random 
import graph_connectivity_lib as gcl
from time import monotonic

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="eval_bot_deciding_connectivity"
args_list = [
    ("goal",str), 
    ("check_also_yes_certificate",bool),
    ("check_also_no_certificate",bool),
    ("code_lang",str),
    ("lang",str)
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# Random n
n = random.randint(2, 1000)
# Random m
max_m = (n * (n-1))//2
if max_m > 10000: # Setting maximum
    max_m = 10000
m = random.randint(n-1, max_m)

stderr.write(f"n: {n}, m: {m}\n")

is_connected = True
seed = gcl.gen_instance_seed(connected=is_connected)

g = gcl.generate_graph(n, m, seed , TAc=TAc, LANG=LANG)

TAc.print(LANG.render_feedback("assigned-instance",f'Instance:\n n: {n}\nm: {m}\n seed: {seed}'), "yellow")
TAc.print(f'graph:\n{g.to_str()}', "white")

# Getting answer (y or n)
start = monotonic()
user_answer = input()
end = monotonic()
time = end - start

stderr.write(f"user_answer: {user_answer}\n")
stderr.write(f"is_connected: {is_connected}\n")

# Checking input validity
if (user_answer == "Y" or user_answer == "y"):
    user_answer = "yes"
if (user_answer == "N" or user_answer == "n"):
    user_answer = "no"
if (user_answer!= "yes" and user_answer!="no"):
    TAc.print(LANG.render_feedback("not-input", 'Input not valid. You can say Y,N,yes,no'),"red")
    exit(0)

# Wrong answers
if(user_answer == "yes" and is_connected == False):
    TAc.print(LANG.render_feedback("wrong-not-connected", 'WRONG, the graph is not connected'),"red")
    exit(0)
if(user_answer == "no" and is_connected == True):
    TAc.print(LANG.render_feedback("wrong-connected", 'WRONG, the graph is connected'),"red")
    exit(0)

stderr.write(f"cert - {is_connected}, {ENV['check_also_yes_certificate']}\n")
# CERTIFICATE

# yes cert
if (is_connected and ENV["check_also_yes_certificate"]):
    TAc.print(LANG.render_feedback("waiting-sp-tree",f'#? waiting for your spanning tree as routing table.\n# Format: each line two numbers separated by space. Then follow m lines, one for each edge, each with two numbers in the interval [0,n).\n# These specify the tail node and the head node of the edge, in this order.\n# Any line beggining with the \'#\' character is ignored.\n# If you prefer, you can use the \'TA_send_txt_file.py\' util here to send us the lines of a file. Just plug in the util at the \'rtal connect\' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.'), "yellow")

    # Asking and getting sp.tree length
    TAc.print(LANG.render_feedback("waiting-sp-tree-len",'# Tell me how many rows are in your spanning tree table'), "yellow")
    start = monotonic()
    sptree_len = TALinput(int, 1, TAc=TAc)
    stderr.write(f"sp.tree len: {sptree_len}\n")
    span = gcl.Graph(sptree_len[0])
    has_outer_edges = True
    not_in_graph = []


    for i in range(sptree_len[0]):
        head, tail = TALinput(int, 2, TAc=TAc)
        head, tail = int(head),int(tail)

        

        # Checking if the inserted nodes are in the range [0, n]
        if tail >= n or head >= n or tail < 0 or head < 0:
            stderr.write(f"{head},{tail}\n")
            TAc.print(LANG.render_feedback("n-at-least-1", f'# ERROR: both ends of an edge must be nodes of the graph, i.e. integers in the range [0,{ENV["MAXN"]}.'), "red")
            exit(0)

        # check the existence of the edges (and nodes)
        if(g.check_edge(head,tail)):
            span.add_edge(head, tail)
        else:
            has_outer_edges = False
            edge = (int(head),int(tail))
            not_in_graph.append(edge)
    end = monotonic()
    time_certificate = end - start

    stderr.write(f"span\n{span.to_str()}\n")

    # check if is connect
    is_certificate_correct, not_conn = span.is_connected(True)
    is_certificate_correct = is_certificate_correct and has_outer_edges

# no cert
if (not is_connected and ENV["check_also_no_certificate"]):
    pass



if(ENV["goal"]=="correct"):
    if(ENV["check_also_yes_certificate"] or ENV["check_also_no_certificate"]):
        if is_certificate_correct:
            TAc.print(LANG.render_feedback("correct-certificate",'Good! Your certificate is correct'),"green")
        else:
            TAc.print(LANG.render_feedback("wrong-certificate",f'WRONG! Certificate is not correct'), "red")
    else:
        TAc.print(LANG.render_feedback("right",f'Right!'), "green")

if time > 10:
    TAc.print(LANG.render_feedback("not-efficient",'Your algorithm as a whole is not very efficient, it takes more than a second\n'),"red")
else:
    TAc.print(LANG.render_feedback("efficient",'Your algorithm overall seems to be efficient!\n'),"green")
TAc.print("#end", "white")
exit(0) 

'''

## With a list of instances increasing dimensions
instances = []
if ENV['goal'] == "linear":
    increase = 1.2
else: # Quadratic
    increase = 1.7

min_n = 2
max_n = 100

for i in range(8):
    n = random.randint(min_n, max_n)
    # Random m
    max_m = (n * (n-1))//2
    if max_m > 10000: # Setting maximum
        max_m = 10000
    m = random.randint(n-1, max_m)

    stderr.write(f"n: {n}, m: {m}\n")

    min_n = max_n
    max_n = int(max_n*increase)
    stderr.write(f"min_n: {min_n}, max_n: {max_n}\n")

    # Generating graph
    seed = gcl.gen_instance_seed(connected=True)
    instances.append(gcl.generate_graph(n, m, seed , TAc=TAc, LANG=LANG))

# Test
for graph in instances:
    TAc.print(LANG.render_feedback("assigned-instance",f'Instance:\n n: {n}\nm: {m}\n seed: {seed}'), "yellow")
    TAc.print(f'graph:\n{g.to_str()}', "white")

    # Getting answer (y or n)
    start = monotonic()
    user_answer = input()
    end = monotonic()
    time = end - start

    stderr.write(f"user_answer: {user_answer}\n")

    # Come sopra
'''