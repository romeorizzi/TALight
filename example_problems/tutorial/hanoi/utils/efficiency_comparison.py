#!/usr/bin/env python3
import sys, os
import random
from time import monotonic

import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services")))
from hanoi_lib import ConfigGenerator, HanoiTowerProblem
from plotter import plotting


# Init data
data = list()


# generate n_list
def generate_n_list(n_max, scaling_factor):
    n_list = list()
    n = 0
    while True:
        n = 1 + int(n * scaling_factor)
        if n > n_max:
            break
        n_list.append(n)
    return n_list


# function test
def one_test(version, initial_type, final_type, seed, n_max, scaling_factor):
    # generate list of n
    n_list = generate_n_list(n_max, scaling_factor)

    # Init Hanoi Tower and configGenerator
    hanoi = HanoiTowerProblem(version)
    gen = ConfigGenerator(seed)

    # Execute all test
    times_correct = list()
    times_efficient = list()
    for n in n_list:
        # get type of configurations
        start, final, error = gen.getConfigs(initial_type, final_type, n)
        assert error == None

        # Get correct answer
        t_start = monotonic()
        hanoi.getMinMoves(start, final, False)
        t_end = monotonic()
        time = t_end - t_start # seconds in float
        times_correct.append(time)

        # Get efficient correct answer
        t_start = monotonic()
        hanoi.getMinMoves(start, final, True)
        t_end = monotonic()
        time = t_end - t_start # seconds in float
        times_efficient.append(time)

        # print
        print(f'Finish test with n={n}')
    print('Finish all test of')

    # Extract data
    diff = np.array(times_correct) - np.array(times_efficient)
    data.append((version, n_list, times_correct, times_efficient, diff))



if __name__ == "__main__":
    # call all test
    initial_type = 'general'
    final_type = 'general'
    seed = 130
    n_max = 16
    scaling_factor = 1.2
    one_test('classic', initial_type, final_type, seed, n_max, scaling_factor)
    one_test('toddler', initial_type, final_type, seed, n_max, scaling_factor)
    one_test('clockwise', initial_type, final_type, seed, n_max, scaling_factor)

    # call plotter
    plotting(data, (12,10))
