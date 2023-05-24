#!/bin/bash

## clean everything
make clean

## generate instances
make

## gimme_instance

rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -ainstance=with_len
rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -aseed=327859 -amod=1 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -aseed=327859 -amod=1 -ainstance=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=22 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=22 -ainstance_format=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=14 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=14 -ainstance_format=with_len

## solve

rtal connect collage -asource=randgen_1
rtal connect collage -asource=randgen_1 -aseq_len=20 -anum_col=15 -aseed=347609 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -aseq_len=20 -anum_col=15 -aseed=347609 -ainstance_format=with_len
rtal connect collage -asource=randgen_1 -amod=1 -aseed=459912 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -amod=1 -aseed=459912 -ainstance_format=with_len
rtal connect collage -asource=randgen_1 -amod=2 -aseed=246891 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -amod=2 -aseed=246891 -ainstance_format=with_len

## check_sol

rtal connect collage check_sol -asource=terminal -ainstance_format=simple
rtal connect collage check_sol -asource=terminal -ainstance_format=with_len
rtal connect collage check_sol -asource=catalogue -ainstance_id=15 -ainstance_format=simple
rtal connect collage check_sol -asource=catalogue -ainstance_id=15 -ainstance_format=with_len
rtal connect collage -asource=randgen_1 -aseqlen=50 -anum_col=40 -aseed=668822 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -aseqlen=50 -anum_col=40 -aseed=668822 -ainstance_format=with_len

## eval_sol

rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bot.py 
rtal connect -e collage eval_sol -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
rtal connect -e collage eval_sol -agoal=seq_from_1_to_50 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --recursive
rtal connect -e collage eval_sol -agoal=seq_from_1_to_50 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
rtal connect -e collage eval_sol -agoal=seq_from_50_to_200 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --recursive
rtal connect -e collage eval_sol -agoal=seq_from_50_to_200 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
rtal connect -e collage eval_sol -agoal=seq_from_200_to_1000 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --recursive
rtal connect -e collage eval_sol -agoal=seq_from_200_to_1000 -- ~/TALight/example_problems/tutorial/collage/bots/bot.py --dynprog
