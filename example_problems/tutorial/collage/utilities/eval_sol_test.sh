#!/bin/bash

rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bots.py
rtal connect -agoal=time_at_most_2_exp_n -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bots.py
rtal connect -agoal=time_at_most_n_exp_2 -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bots.py
