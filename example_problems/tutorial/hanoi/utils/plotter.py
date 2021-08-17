#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic
import matplotlib.pyplot as plt
import numpy as np


def plotting(data, figure_size):
    """data=(n, t_no_efficient, t_efficient) is a list of data to plotting."""

    # plotting settings
    plt.figure(figsize = figure_size)

    counter = 1
    for i in range(len(data)):
        # extract data
        name = data[i][0]
        n = data[i][1]
        t_no_efficient = data[i][2]
        t_efficient = data[i][3]
        diff = np.array(t_no_efficient) - np.array(t_efficient)


        # plotting times comparison
        plt.subplot(len(data), 2, counter)
        plt.title(f'{name}',fontweight="bold", loc="left")
        plt.plot(n, t_no_efficient, marker = 'o', color='b', label='only_correct')
        plt.plot(n, t_efficient, marker = 'o', color='g', label='also_efficient')
        plt.legend(loc="upper left")
        plt.xlabel('N')
        plt.ylabel('times (seconds)')
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)

        # plotting difference
        plt.subplot(len(data), 2, counter+1)
        if i == 0:
            plt.title('Difference between comparison',fontweight="bold")
        plt.plot(n, diff, marker = 'o', color='r')
        plt.xlabel('N')
        plt.ylabel('difference (seconds)')
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)

        #update counter
        counter += 2

    plt.suptitle('Efficiency comparison',fontweight="bold")
    plt.show()

