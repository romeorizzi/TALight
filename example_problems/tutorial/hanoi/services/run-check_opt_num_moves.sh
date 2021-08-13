#!/bin/zsh 

PROBLEM=hanoi
SERVICE=check_opt_num_moves

START=all_A
FINAL=all_C
# START=ABC
# FINAL=CBA
# N=-1

N=2
SOL=3
MODULUS=0

# N=3
# SOL=1
# MODULUS=5

V=classic
# V=toddler
# V=clockwise

SILENT=1

# FEEDBACK=yes_no
# FEEDBACK=smaller_or_bigger
FEEDBACK=true_val

CERTIFICATE=1

LANG=hardcoded


###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -astart=$START \
    -afinal=$FINAL \
    -an=$N \
    -aansw=$SOL \
    -aok_if_congruent_modulus=$MODULUS \
    -av=$V \
    -asilent=$SILENT \
    -afeedback=$FEEDBACK \
    -awith_certificate=$CERTIFICATE \
    -alang=$LANG

