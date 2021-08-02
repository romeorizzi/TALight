#!/bin/zsh 

PROBLEM=hanoi
SERVICE=play_like


START=all_A
# START=AA
FINAL=all_C
# FINAL=AC

N=2

ROLE=daddy
# ROLE=toddler

# HELP=minimal
HELP=gimme_moves_available


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



###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -arole=$ROLE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -aformat=$FORMAT \
    -ahelp=$HELP \
    -alang=$LANG

