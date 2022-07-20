#!/bin/bash

rtal connect collage check_sol -asource=terminal -ainstance_format=simple
rtal connect collage check_sol -asource=terminal -ainstance_format=with_len
rtal connect collage check_sol -asource=catalogue -ainstance_id=15 -ainstance_format=simple
rtal connect collage check_sol -asource=catalogue -ainstance_id=15 -ainstance_format=with_len
rtal connect collage -asource=randgen_1 -aseqlen=50 -anum_col=40 -aseed=668822 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -aseqlen=50 -anum_col=40 -aseed=668822 -ainstance_format=with_len

