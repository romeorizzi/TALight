#!/bin/zsh 

PROBLEM=hanoi
SERVICE=check_lower_bounds

START=all_A
# START=ABC
FINAL=all_C
# FINAL=CBAC
# N=-1
N=3

DISK=3

SOL=2

V=classic
# V=toddler
# V=clockwise

SILENT=0

# FEEDBACK=yes_no
# FEEDBACK=smaller_or_bigger
FEEDBACK=true_val

LANG=hardcoded


###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -adisk=$DISK \
    -aansw=$SOL \
    -av=$V \
    -asilent=$SILENT \
    -afeedback=$FEEDBACK \
    -alang=$LANG

