#!/bin/bash

rtal connect collage -asource=randgen_1
rtal connect collage -asource=randgen_1 -aseq_len=20 -anum_col=15 -aseed=347609 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -aseq_len=20 -anum_col=15 -aseed=347609 -ainstance_format=with_len
rtal connect collage -asource=randgen_1 -amod=1 -aseed=459912 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -amod=1 -aseed=459912 -ainstance_format=with_len
rtal connect collage -asource=randgen_1 -amod=2 -aseed=246891 -ainstance_format=simple
rtal connect collage -asource=randgen_1 -amod=2 -aseed=246891 -ainstance_format=with_len
