#!/bin/bash

rtal connect vertex_cover -asource=randgen_1
rtal connect vertex_cover -asource=randgen_1 -anum_vertices=10 -anum_edges=15
rtal connect vertex_cover -asource=randgen_1 -anum_vertices=10 -anum_edges=15 -aweighted=1
rtal connect vertex_cover -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -ainstance_format=with_info
rtal connect vertex_cover -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -ainstance_format=simple
rtal connect vertex_cover -asource=randgen_1 -anum_vertices=20 -anum_edges=30 -ainstance_format=simple -aweighted=1
rtal connect vertex_cover -asource=terminal -anum_vertices=8 -anum_edges=11 
rtal connect vertex_cover -asource=terminal -anum_vertices=8 -anum_edges=11 -aweighted=1

