#!/bin/zsh 

PROBLEM=hanoi
SERVICE=check_one_sol

V=classic
START=all_A
FINAL=all_C
N=2
GOAL=optimal

# FEEDBACK=yes_no
# FEEDBACK=spot_first_non_optimal_move
FEEDBACK=gimme_shorter_solution
# FEEDBACK=gimme_optimal_solution

BOT_PATH="../bots/classic_hanoi_bot_check.py"
FORMAT=minimal
LANG=hardcoded



###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -av=$V \
    -aformat=$FORMAT \
    -agoal=$GOAL \
    -afeedback=$FEEDBACK \
    -alang=$LANG \
    -- $BOT_PATH
