#!/bin/bash

rtal connect collage
rtal connect collage -aseq_len=20 -anum_col=15 -aseed=347609 -ainstance_format=simple
rtal connect collage -aseq_len=20 -anum_col=15 -aseed=347609 -ainstance_format=with_len
rtal connect collage -amod=1 -aseed=459912 -ainstance_format=simple
rtal connect collage -amod=1 -aseed=459912 -ainstance_format=with_len
rtal connect collage -amod=2 -aseed=246891 -ainstance_format=simple
rtal connect collage -amod=2 -aseed=246891 -ainstance_format=with_len
