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
elif [ $TEST = 2 ]; then
    START=general
    FINAL=general
    TESTS=2
    N_MAX=5
elif [ $TEST = 3 ]; then
    START=all_A
    FINAL=all_C
    TESTS=1
    N_MAX=2
fi




TEST=1
if [ $TEST = 1 ]; then
    FORMAT=minimal
    LANG=hardcoded
elif [ $TEST = 2 ]; then
    FORMAT=extended
    LANG=hardcoded
elif [ $TEST = 3 ]; then
    FORMAT=extended
    LANG=it
elif [ $TEST = 4 ]; then
    FORMAT=extended
    LANG=en
fi

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

