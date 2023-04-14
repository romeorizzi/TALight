#!/bin/bash

rtal connect -e vertex_cover eval_approx_weighted_vc -agoal=small_instances -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --approx
rtal connect -e vertex_cover eval_approx_weighted_vc -agoal=big_instances -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --approx
