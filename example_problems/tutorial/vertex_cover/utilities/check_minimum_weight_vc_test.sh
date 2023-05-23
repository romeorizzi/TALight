#!/bin/bash

rtal connect vertex_cover check_minimum_weight_vc -asource=randgen_1
rtal connect vertex_cover check_minimum_weight_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=with_info
rtal connect vertex_cover check_minimum_weight_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=simple
rtal connect vertex_cover check_minimum_weight_vc -asource=catalogue -ainstance_format=with_info
rtal connect vertex_cover check_minimum_weight_vc -asource=catalogue -ainstance_format=simple
rtal connect vertex_cover check_minimum_weight_vc -asource=terminal -anum_vertices=8 -anum_edges=11
