#!/bin/bash

rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bot.py 
rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
rtal connect -e collage eval_sol -agoal=seq_from_1_to_50 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --recursive
rtal connect -e collage eval_sol -agoal=seq_from_1_to_50 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
rtal connect -e collage eval_sol -agoal=seq_from_50_to_200 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --recursive
rtal connect -e collage eval_sol -agoal=seq_from_50_to_200 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
rtal connect -e collage eval_sol -agoal=seq_from_200_to_1000 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --recursive
rtal connect -e collage eval_sol -agoal=seq_from_200_to_1000 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
