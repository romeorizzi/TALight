#!/usr/bin/env python3
import sys, os
import random
from time import monotonic
import matplotlib.pyplot as plt


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services")))
from hanoi_lib import ConfigGenerator, HanoiTowerProblem
from plotter import plotting


# Init data
data = list()


# function test
def one_test(version, seed, n_max_check, inc_check, n_max_perform, inc_perform):
    # generate list of n
    n_list = list(range(1, n_max_check, inc_check)) + \
            list(range(n_max_check, n_max_perform + inc_perform, inc_perform))

    # Init Hanoi Tower and configGenerator
    hanoi = HanoiTowerProblem(version)
    gen = ConfigGenerator(seed,)

    # Execute all test
    times_correct = list()
    times_efficient = list()
    for n in n_list:
        # get type of configurations
        start, final, error = gen.getConfigs('all_A', 'all_C', n)
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
    data.append((version, n_list, times_correct, times_efficient))



if __name__ == "__main__":
    # call all test
    seed = 130
    one_test('classic', seed, n_max_check=10, inc_check=1, n_max_perform=16, inc_perform=2)
    one_test('toddler', seed, n_max_check=10, inc_check=1, n_max_perform=16, inc_perform=2)
    one_test('clockwise', seed, n_max_check=10, inc_check=1, n_max_perform=16, inc_perform=2)

    # call plotter
    plotting(data, (12,10))
