#!/bin/zsh 

PROBLEM=hanoi
SERVICE=eval_opt_num_moves

V=classic

START=all_A
# START=general
FINAL=all_C
# FINAL=general

MODULUS=0

GOAL=correct
# GOAL=efficient

# SEED=-1
SEED=130000

TESTS=1
# TESTS=5
# N_MAX=10
N_MAX=20

CODE=python

LANG=hardcoded
BOT_PATH="../bots/classic_hanoi_bot_eval_min_moves.py"


###########################################
rtal connect -e \
    $PROBLEM \
    $SERVICE \
    -av=$V \
    -astart=$START \
    -afinal=$FINAL \
    -aok_if_congruent_modulus=$MODULUS \
    -agoal=$GOAL \
    -aseed=$SEED \
    -anum_tests=$TESTS \
    -an_max=$N_MAX \
    -acode_lang=$CODE \
    -alang=$LANG \
    -- $BOT_PATH

