#!/bin/bash

rtal connect vertex_cover check_approx_weighted_vc -asource=randgen_1
rtal connect vertex_cover check_approx_weighted_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=with_info
rtal connect vertex_cover check_approx_weighted_vc -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -ainstance_format=simple
rtal connect vertex_cover check_approx_weighted_vc -asource=catalogue -ainstance_id=32 -ainstance_format=with_info
rtal connect vertex_cover check_approx_weighted_vc -asource=catalogue -ainstance_id=32 -ainstance_format=simple
rtal connect vertex_cover check_approx_weighted_vc -asource=terminal -anum_vertices=10 -anum_edges=15
rtal connect vertex_cover check_approx_weighted_vc -asource=terminal -anum_vertices=10 -anum_edges=15
