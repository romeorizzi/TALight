#!/bin/bash

rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bots.py 
rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bots.py --dynprog
rtal connect -e collage eval_sol -agoal=time_at_most_2_exp_n -- ~/TALight/example_problems/tutorial/collage/bots/bots.py --recursive
rtal connect -e collage eval_sol -agoal=time_at_most_2_exp_n -- ~/TALight/example_problems/tutorial/collage/bots/bots.py --dynprog
rtal connect -e collage eval_sol -agoal=time_at_most_n_exp_2 -- ~/TALight/example_problems/tutorial/collage/bots/bots.py --recursive
rtal connect -e collage eval_sol -agoal=time_at_most_n_exp_2 -- ~/TALight/example_problems/tutorial/collage/bots/bots.py --dynprog
