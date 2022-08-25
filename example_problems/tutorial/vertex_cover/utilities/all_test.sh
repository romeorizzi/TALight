#!/bin/bash

## clean everything
make clean

## generate instances
make

## gimme_instance
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance=with_info
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -aweighted=1 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -aweighted=1 -ainstance=with_info
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -ainstance=with_info
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -aweighted=1 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -aweighted=1 -ainstance=with_info
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=9 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=9 -ainstance_format=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=15 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=15 -ainstance_format=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=30 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=42 -ainstance_format=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=42 -ainstance_format=simple

## chech_minimum_vc
rtal connect vertex_cover check_minimum_vc -asource=randgen_1
rtal connect vertex_cover check_minimum_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=with_info
rtal connect vertex_cover check_minimum_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=simple
rtal connect vertex_cover check_minimum_vc -asource=catalogue -ainstance_format=with_info
rtal connect vertex_cover check_minimum_vc -asource=catalogue -ainstance_format=simple
rtal connect vertex_cover check_minimum_vc -asource=terminal -anum_vertices=8 -anum_edges=11

## check_minimum_weight_vc
rtal connect vertex_cover check_minimum_weight_vc -asource=randgen_1
rtal connect vertex_cover check_minimum_weight_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=with_info
rtal connect vertex_cover check_minimum_weight_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=simple
rtal connect vertex_cover check_minimum_weight_vc -asource=catalogue -ainstance_format=with_info
rtal connect vertex_cover check_minimum_weight_vc -asource=catalogue -ainstance_format=simple
rtal connect vertex_cover check_minimum_weight_vc -asource=terminal -anum_vertices=8 -anum_edges=11

## check_approx_vc
rtal connect vertex_cover check_approx_vc -asource=randgen_1
rtal connect vertex_cover check_approx_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=with_info
rtal connect vertex_cover check_approx_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=simple
rtal connect vertex_cover check_approx_vc -asource=catalogue -ainstance_id=32 -ainstance_format=with_info
rtal connect vertex_cover check_approx_vc -asource=catalogue -ainstance_id=32 -ainstance_format=simple
rtal connect vertex_cover check_approx_vc -asource=terminal -anum_vertices=10 -anum_edges=15
rtal connect vertex_cover check_approx_vc -asource=terminal -anum_vertices=10 -anum_edges=15

## check_approx_weighted_vc
rtal connect vertex_cover check_approx_weighted_vc -asource=randgen_1
rtal connect vertex_cover check_approx_weighted_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=with_info
rtal connect vertex_cover check_approx_weighted_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=simple
rtal connect vertex_cover check_approx_weighted_vc -asource=catalogue -ainstance_id=32 -ainstance_format=with_info
rtal connect vertex_cover check_approx_weighted_vc -asource=catalogue -ainstance_id=32 -ainstance_format=simple
rtal connect vertex_cover check_approx_weighted_vc -asource=terminal -anum_vertices=10 -anum_edges=15
rtal connect vertex_cover check_approx_weighted_vc -asource=terminal -anum_vertices=10 -anum_edges=15

## eval_minimum_vc
rtal connect -e vertex_cover eval_minimum_vc -agoal=feasible -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --minimum
rtal connect -e vertex_cover eval_minimum_vc -agoal=minimum -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --minimum

## eval_minimum_weight_vc
rtal connect -e vertex_cover eval_minimum_weight_vc -agoal=feasible -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --minimum
rtal connect -e vertex_cover eval_minimum_weight_vc -agoal=minimum -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --minimum

## eval_approx_vc
rtal connect -e vertex_cover eval_approx_vc -agoal=small_instances -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --approx
rtal connect -e vertex_cover eval_approx_vc -agoal=big_instances -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --approx

## eval_approx_weighted_vc
rtal connect -e vertex_cover eval_approx_weighted_vc -agoal=small_instances -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --approx
rtal connect -e vertex_cover eval_approx_weighted_vc -agoal=big_instances -- ~/TALight/example_problems/tutorial/vertex_cover/bots/bot.py --approx
