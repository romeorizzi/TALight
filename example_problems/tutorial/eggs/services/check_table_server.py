#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="check_table"
args_list = [
    ('eggs_from_zero',bool),
    ('floors_from_zero',bool),
    ('separator',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
from random import randrange
from math import inf as IMPOSSIBLE

from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

sep=None if ENV['separator']=="None" else ENV['separator']
if ENV['eggs_from_zero']:
    print('# waiting for a rectangular table of natural numbers. The first row (i.e., the 0 eggs row) may contain "inf" entries to represent that the truth can not be learned with 0 eggs. Insert a closing line "# END" after the last row of the table.')
else:
    print('# waiting for a rectangular table of natural numbers. Insert a closing line "# END" after the last row of the table.')
def get_line():
    raw_line = input().strip()
    if raw_line[0] != "#":
        return [tk.strip() for tk in raw_line.split("#")[0].split(sep)], None
    key = raw_line[1:].strip().split()[0].upper()
    if key == "END" or key == "NEXT":
        return None, key 
    return None, "GEN_COMMENT"

def represents_int(s, extended=False):
    if extended and s=="inf":
        return True
    try: 
        int(s)
        return True
    except ValueError:
        return False    

first_line, cmd = get_line() 
while first_line == None:
    first_line, cmd = get_line()

last_floor = len(first_line) -1 if ENV['floors_from_zero'] else len(first_line)
table_submitted = [ [0] + [IMPOSSIBLE] * last_floor]

if ENV['eggs_from_zero']:
    if not all(represents_int(_,True) for _ in first_line):
        print("# Error (in the table format): All entries in the first row of your table should be extended integers (either naturals or 'inf').")
        exit(1)
    if ENV['floors_from_zero']:
        if not represents_int(first_line[0]) or int(first_line[0]) != 0:
            print("! We disagree: the answer should always be the natural number 0 when given 0 eggs and 0 floors.")
            exit(0)
        first_line = first_line[1:]
    if not all(elem == "inf" for elem in first_line):
        print('! We disagree: when given 0 eggs and >0 floors there is no way (which we represent with "inf").')
        exit(0)            
else:
    if not all(represents_int(_) for _ in first_line):
        print(f"# Error (in the table format): All entries in your table should be integers (actually, natural numbers). Just check row {len(table_submitted)} in your file for a first occurrence of a type mismatch.")
    table_submitted.append(([] if ENV['floors_from_zero'] else [0]) + list(map(int, first_line)))

next_line, cmd = get_line() 
while cmd != "END":
    if cmd == "NEXT":
        print("# Error: This service does not accept more than one single table.")
        exit(1)
    if next_line != None:
        if not all(represents_int(_) for _ in next_line):
            if ENV['eggs_from_zero']:
                print(f"# Error (in the table format): Except for the first row (where we use 'inf' entries to represent impossibility), all other entries in your table should be integers. Just check row {len(table_submitted)} in your file.")
            else:
                print(f"# Error (in the table format): All entries in your table should be integers. Just check row {len(table_submitted)} in your file for a first occurrence of a type mismatch.")
            exit(1)
        if len(next_line) != (last_floor+1 if ENV['floors_from_zero'] else last_floor):
            print(f"# Error (in the table format): The row {1+len(table_submitted)} of your table contains {len(next_line)} elements whereas all previous rows contain {last_floor+1 if ENV['floors_from_zero'] else last_floor} elements.")
            exit(1)
        table_submitted.append(([] if ENV['floors_from_zero'] else [0]) + list(map(int, next_line)))
    next_line, cmd = get_line()
print("# FILE GOT")

def entry_should_be(n_eggs,n_floors):
    if n_floors == 0:
        return 0
    if n_eggs == 0:
        return IMPOSSIBLE
    risp = IMPOSSIBLE
    for first_launch_floor in range(1,1+n_floors):
        risp = min(risp,1+max(table_submitted[n_eggs][n_floors-first_launch_floor],table_submitted[n_eggs-1][first_launch_floor-1]))
    return risp

def check_entry(n_eggs,n_floors):
    if table_submitted[n_eggs][n_floors] != entry_should_be(n_eggs,n_floors):
        print(f"! We disagree: according to your table, you need {table_submitted[n_eggs][n_floors]} launches when given {n_eggs} eggs and {n_floors} floors. In our opinion the minimum number of launches needed in the worst case is {entry_should_be(n_eggs,n_floors)}.")
        exit(0)

for n_eggs in range(len(table_submitted)):
    for n_floors in range(len(table_submitted[0])):
        check_entry(n_eggs,n_floors)

print(f"Ok! Your table is correct in every single entry!")

exit(0)
