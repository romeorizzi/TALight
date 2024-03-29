#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic
import matplotlib.pyplot as plt


def plotting(data, figure_size):
    """data=(name, n, t_no_efficient, t_efficient) is a list of data to plotting."""

    # plotting settings
    plt.figure(figsize = figure_size)

    counter = 1
    for i in range(len(data)):
        # extract data
        name = data[i][0]
        n = data[i][1]
        t_no_efficient = data[i][2]
        t_efficient = data[i][3]
        assert len(t_no_efficient) == len(t_efficient)
        diff = [t_no_efficient[i] - t_efficient[i] for i in range(len(t_no_efficient))]

        # print stats
        print(f'n={n}')
        print(f'last_no_eff={t_no_efficient[-1]}')
        print(f'last_eff={t_efficient[-1]}')
        print(f'last_diff={diff[-1]}')
        print()


        # plotting times comparison
        plt.subplot(len(data), 2, counter)
        plt.title(f'{name}',fontweight="bold", loc="right")
        plt.plot(n, t_no_efficient, marker = 'o', color='b', label='only_correct')
        plt.plot(n, t_efficient, marker = 'o', color='g', label='also_efficient')
        plt.legend(loc="upper left")
        plt.xlabel('N')
        plt.ylabel('times (seconds)')
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)

        # plotting difference
        plt.subplot(len(data), 2, counter+1)
        plt.plot(n, diff, marker = 'o', color='r', label='difference')
        plt.legend(loc="upper left")
        plt.xlabel('N')
        plt.ylabel('difference (seconds)')
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)

        #update counter
        counter += 2

    plt.suptitle('EFFICIENCY COMPARISON',fontweight="bold")
    plt.show()

