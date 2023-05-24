#!/bin/bash

rtal connect -e vertex_cover eval_minimum_vc -agoal=feasible -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --minimum
rtal connect -e vertex_cover eval_minimum_vc -agoal=minimum -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --minimum
