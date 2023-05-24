#!/bin/bash

rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -ainstance=with_len
rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -aseed=327859 -amod=1 -ainstance=simple
rtal connect collage gimme_instance -asource=randgen_1 -aseq_len=30 -anum_col=22 -aseed=327859 -amod=1 -ainstance=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=22 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=22 -ainstance_format=with_len
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=14 -ainstance_format=simple
rtal connect collage gimme_instance -asource=catalogue -ainstance_id=14 -ainstance_format=with_len
