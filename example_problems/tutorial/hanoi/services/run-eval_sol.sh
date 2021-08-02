#!/bin/zsh 

PROBLEM=hanoi
SERVICE=eval_sol

V=classic

# SEED=-1
SEED=130000


TEST=1
if [ $TEST = 1 ]; then
    START=all_A
    FINAL=all_C
    TESTS=1
    N_MAX=5
else
    START=general
    FINAL=general
    TESTS=2
    N_MAX=5
fi



FORMAT=minimal
# FORMAT=extended
LANG=hardcoded
BOT_PATH="../bots/classic_hanoi_bot_eval_sol.py"


###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -av=$V \
    -astart=$START \
    -afinal=$FINAL \
    -aformat=$FORMAT \
    -aseed=$SEED \
    -anum_tests=$TESTS \
    -an_max=$N_MAX \
    -alang=$LANG \
    -- $BOT_PATH

