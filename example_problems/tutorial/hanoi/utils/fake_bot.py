#!/usr/bin/env python3
import sys


def wait_start():
    while True:
        spoon = input()
        if spoon[0] != '#':
            break


def wait_end():
    print('end')
    while True:
        spoon = input()



######################################################################
# main
if len(sys.argv) == 4 and sys.argv[1] == 'bot_mode':
    service = sys.argv[2]
    test = sys.argv[3]
    # wait start
    wait_start()
    

    ######################################################################
    # check_opt_num_moves
    if service == 'check_one_sol':
        if test == 'optimal':
            print('1:AB')
            print('2:AC')
            print('1:BC')
            wait_end()

        if test == 'optimal_custom_config':
            print('1:AB')
            print('3:CA')
            print('1:BC')
            wait_end()

        if test == 'wrong':
            print('2:AC')
            print('1:AB')
            print('1:BC')
            wait_end()

        if test == 'wrong_short':
            print('2:AC')
            print('1:AC')
            wait_end()

        if test == 'admissible_loop':
            print('1:AB')
            print('2:AC')
            print('2:CA')
            print('2:AC')
            print('1:BC')
            wait_end()

        if test == 'simple_walk_not_optimal':
            print('1:AC')
            print('1:CB')
            print('2:AC')
            print('1:BA')
            print('1:AC')
            wait_end()
