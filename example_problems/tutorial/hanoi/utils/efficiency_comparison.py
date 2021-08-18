#!/usr/bin/env python3
import os, sys
import ast
from plotter import plotting


VERSIONS = ['classic', 'toddler', 'clockwise']


def string_to_list(s):
    # Converting string to list
    return ast.literal_eval(s)


if __name__ == "__main__":
    data = list()
    for v in VERSIONS:
        with open(f'data/{v}_n.txt', 'r') as mode_file:
            n = string_to_list(mode_file.readline())
        with open(f'data/{v}_correct.txt', 'r') as mode_file:
            correct = string_to_list(mode_file.readline())
        with open(f'data/{v}_efficient.txt', 'r') as mode_file:
            efficient = string_to_list(mode_file.readline())
        data.append((v, n, correct, efficient))

    plotting(data, (12,9))
