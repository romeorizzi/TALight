#!/usr/bin/env python3

from sys import stderr

if __name__ == "__main__":

    def num_ones_over_interval(left_point, num_points):
        global q
        print(f"? {left_point} {num_points}", flush=True)
        q += 1
        risp = int(input())
        print(f"num_ones_over_interval({left_point=}, {num_points=}) = {risp}", file=stderr)
        return risp


    def find_leftmost_one():
        lb_left = 0
        ub_left = n - num_ones
        while lb_left < ub_left:
            num_points = (num_ones + ub_left - lb_left) // 2
            mass = num_ones_over_interval(lb_left, num_points)
            if mass == -1:
                return -1
            elif mass == 0:
                lb_left += num_points
            elif mass == num_ones:
                ub_left = lb_left + num_points - num_ones
            else:
                assert 0 < mass < num_ones, f"{mass=}"
                return lb_left + num_points - mass 
        assert lb_left == ub_left
        return ub_left


    T = int(input())
    for t in range(T):
        n = int(input())
        print(f"{n=}", file=stderr)
        q = 0
        num_ones = num_ones_over_interval(0, n)
        assert 0 < num_ones <= n, f"invece {num_ones=}"
        left = find_leftmost_one()
        if left >= 0:
            print(f"! {left} {num_ones}", flush=True)
            print(f"Case #{t+1:03} q:", q, file=stderr)
        else:
            print(f"Case #{t+1:03} q:", q, " (too many)", file=stderr)
        
