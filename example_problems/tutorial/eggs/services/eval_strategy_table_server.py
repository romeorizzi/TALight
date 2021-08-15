#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange

from multilanguage import Env, Lang, TALcolors
from get_tables import get_one_numeric_table

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="eval_strategy_table"
args_list = [
    ('separator',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

def check_entry_integer(row_index_name,col_index_name,entry_val):
    if type(entry_val) != int:
        print(f"# Error (in the table format): the entry ({row_index_name},{col_index_name}) in your table represents the floor from which to throw the first of {row_index_name} eggs when the floors are {col_index_name} (numbered from 1 to {col_index_name}). As such entry ({row_index_name},{col_index_name}) should be a natural number. However, the value {entry_val} is a non integer float with decimal part.")
        exit(1)        

def check_entry_range(row_index_name,col_index_name,entry_val):
    if entry_val < 1 or entry_val > col_index_name:
        print(f"# Error (in the table format): the entry ({row_index_name},{col_index_name}) in your table represents the floor from which to throw the first of {row_index_name} eggs when the floors are {col_index_name} (numbered from 1 to {col_index_name}). As such entry ({row_index_name},{col_index_name}) should be a natural in the interval [1,{col_index_name}]. However, the value {entry_val} does not belong to that interval.")
        exit(1)

strategy_table=get_one_numeric_table(sep=None if ENV['separator']=="None" else ENV['separator'], should_be_int=False, row_names_start_from=1, col_names_start_from=1, checks=[check_entry_integer, check_entry_range]) # we set should_be_int=False because we wanted to provide a more specific error message to the problem-solver, as managed in the handler check_entry_integer
print(f"Ok! Your table makes sense in every single entry! I can hence proceed evaluating the 'strategy' it represents.")

N_eggs = len(strategy_table)
N_floors = len(strategy_table[0])

max_launches = tot_launches = max_missions = tot_missions = 0

def simulate(strategy_table, truth, N_eggs, N_floors):
    launches = missions = 0
    previous_try = N_floors+1
    truth_lb=1 # the very first floor could already be a killer
    truth_ub=N_floors+1 # there in no breaking floor
    while truth_lb < truth_ub:
        n_floors = truth_ub-truth_lb # number of 'virtual flows' where the egg could break
        if N_eggs == 0:
            return truth_lb, truth_ub, True
        launches += 1
        try_floor = truth_lb -1 + strategy_table[N_eggs-1][n_floors-1]
        if try_floor < previous_try:
            missions += 1
        if truth > try_floor:   # BOUNCH!
            truth_lb = try_floor+1
        else:  # CRASH!
            N_eggs -= 1
            truth_ub = try_floor    
    return launches, missions, False

for truth in range(1, 2+N_floors):
    launches, missions, failure = simulate(strategy_table, truth, N_eggs, N_floors)
    if failure:
        if truth > N_floors:
            print(f"There is a serious problem with your strategy: if the truth is that the eggs never brake, then all of your eggs will go broken before you can discern this truth. In particular, you will never know whether an egg brakes when launched from floor {N_floors}. More generally, you will end up with no eggs left (all crashed) into a situation where you do not know whether an egg would brake or not when thrown from floor i for any i in the range [{launches},{missions}].")
        elif truth == 1:
            print(f"There is a serious problem with your strategy: if the truth is that the egg would brake even when thrown from floor 1, then all of your eggs will go broken before you can discern this truth. In particular, you will never know whether an egg brakes when launched from floor {N_floors}. More generally, you will end up with no eggs left (all crashed) into a situation where you do not know whether an egg would brake or not when thrown from floor i for any i in the range [{launches},{missions}].")
        else:
            print(f"There is a serious problem with your strategy: if the truth is that the egg brakes when thrown from floor {truth} but does not brake when thrown from floor {truth-1} then, by playing this strategy, you will end up with no eggs left (all crashed) into a situation where you do not know whether an egg would brake or not when thrown from floor {launches}. In fact, you do not know this for any floor in the range [{launches},{missions}]")
        exit(1)

    max_launches = max(max_launches,launches)
    max_missions = max(max_missions,missions)
    tot_launches += launches
    tot_missions += missions 

print(f"Here is the scoring profile of your strategy when run over all possible truths:\n   - max_launches = {max_launches}\n   - avg_launches = {tot_launches/(N_floors+1)}\n   - max_missions = {max_missions}\n   - avg_missions = {tot_missions/(N_floors+1)}")

exit(0)
