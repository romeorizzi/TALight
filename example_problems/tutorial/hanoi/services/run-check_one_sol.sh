#!/bin/zsh 

PROBLEM=hanoi
SERVICE=check_one_sol

V=classic

FORMAT=minimal
# FORMAT=extended

GOAL=admissible
# GOAL=optimal
# GOAL=simple_walk
# GOAL=check_only_disk

# FEEDBACK=yes_no
# FEEDBACK=spot_first_non_optimal_move
FEEDBACK=gimme_shorter_solution
# FEEDBACK=gimme_optimal_solution

BOT_PATH="../bots/classic_hanoi_bot_check.py"
LANG=hardcoded
# LANG=en


TEST=1
if [ $TEST = 1 ]; then
    START=all_A
    FINAL=all_C
    N=2
elif [ $TEST = 2 ]; then
    START=ABC
    FINAL=CBA
    N=-1
else
    START=AABB
    FINAL=CBBA
    N=-1
fi



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
