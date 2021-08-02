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

LANG=hardcoded



###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -arole=$ROLE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -ahelp=$HELP \
    -alang=$LANG

