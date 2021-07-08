#!/bin/zsh 

PROBLEM=hanoi
SERVICE=check_one_sol

# START=all_A
# FINAL=all_A
# START=ABC
# FINAL=CBA
START=all_A
FINAL=all_C
# N=-1
N=2

V=classic

GOAL=any #any

# FEEDBACK=minimal
# FEEDBACK=spot_first_non_optimal_move
FEEDBACK=gimme_shorter_solution
# FEEDBACK=gimme_optimal_solution

LANG=hardcoded
BOT_PATH="../bots/classic_hanoi_bot_check.py"


###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -av=$V \
    -agoal=$GOAL \
    -afeedback=$FEEDBACK \
    -alang=$LANG \
    -- $BOT_PATH

