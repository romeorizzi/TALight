#!/usr/bin/env python3

def num_sol(num_pairs):
    # risps_correct[num_open][num_closed] = number of different prefixes of well-formed formula with <num_open> open parentheses and <num_closed> closed parentheses.
    risps_correct = [ [1] * (num_pairs+2) for _ in range(num_pairs+1)]
    for num_open in range(1,num_pairs+1):
        risps_correct[num_open][0] = risps_correct[num_open-1][1]
        for num_closed in range(1,num_pairs+1):
            risps_correct[num_open][num_closed] = risps_correct[num_open][num_closed-1] + risps_correct[num_open-1][num_closed+1]

    return risps_correct[num_pairs][0]

