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
if len(sys.argv) == 3:
    service = sys.argv[1]
    test = sys.argv[2]
    # wait start
    wait_start()
    

    ######################################################################
    # check_one_sol
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

        if test == 'ignore_peg_from':
            print('1:XB')
            print('2:XC')
            print('1:XC')
            wait_end()

        if test == 'ignore_peg_to':
            print('1:AX')
            print('2:AX')
            print('1:BX')
            wait_end()

        if test == 'ignore_both':
            print('1:XX')
            print('2:XX')
            print('1:XX')
            wait_end()

    

    ######################################################################
    # eval_sol
    if service == 'eval_sol':
        if test == 'fake_correct':
            wait_start()
            print('1:AC')
            print('end')

            wait_start()
            wait_start()
            print('1:AB')
            print('2:AC')
            print('1:BC')
            print('end')
            wait_end()

        if test == 'fake_fail':
            wait_start()
            print('1:AC')
            print('end')

            wait_start()
            wait_start()
            print('1:AB')
            print('2:BC')
            print('1:BC')
            print('end')
            wait_end()
