# Rainbow and Collage

### Problem description

On the planet Wobniar every morning a beautiful and distinctive ** rainbow ** shines. The peculiarity consists in the arrangement of the colors, which can appear several times inside the arch in an ever new and surprising sequence.

Every day at dawn, famed artist Ed Esor captures the splendor of the new arch in a **collage of colored stripes**. To save on materials and allow them to be recycled better, Ed Esor always tries to **minimize the number of sheets of colored paper** to be superimposed in the composition of the collage, without ever giving up on faithfully reproducing the sequence that appeared in the sky.

Help Ed Esor minimize the number of sheets used in his collage! If, for example, the rainbow were composed of 3 strips of 2 different alternating colors, Ed Esor would be able to make a collage using only two sheets of paper: one, arranged as a base, of the same color as the two strips at the ends of the rainbow , the other placed on the center of the first.

### Input data

The problem instance has **two lines**.

The first line contains only a natural number ***N*** which specifies the **number of stripes** in the rainbow.
The second line reports *N* integers ***C\_1***, ***C\_2***, ..., ***C\_N*** separated by spaces that specify the **color sequence** of today's rainbow.

Each color *C\_i* is an integer between **0** and **255**.
Wide, uniform stripes in color are indicated by several identical numbers arranged consecutively.

### Output data

The output consists of a single number: the **minimum number of stripes** to reproduce the rainbow

### Input/Output examples

| Input                | Output     |
| -------------------- | ---------- |
| 3<br />1 2 1         | 2          |
| **Input**            | **Output** |
| 7<br />1 1 2 3 1 2 1 | 4          |