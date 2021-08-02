#!/bin/zsh 

PROBLEM=hanoi
SERVICE=gen_random_puzzle

SEED=-1
# SEED=130000

N=3
# START=all_A
START=general
# FINAL=all_C
FINAL=general

# VERBOSE=0
VERBOSE=1
# VERBOSE=2

LANG=hardcoded



###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -an=$N \
    -aseed=$SEED \
    -astart=$START \
    -afinal=$FINAL \
    -averbose=$VERBOSE \
    -alang=$LANG

