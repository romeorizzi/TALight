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

FEEDBACK=minimal
# FEEDBACK=gimme_moves_available

LANG=hardcoded



###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -aai_role=$ROLE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -afeedback=$FEEDBACK \
    -alang=$LANG

