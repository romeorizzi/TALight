# Tiling of an mxn-board with 1x2-boards

Here is a tiling of the chessboard by sub-boards which are either 1x2-boards or 2x1-boards, i.e., by dominos (pairs of adjacent cells):

![esempio di tiling](figs/Pavage_domino.svg)

Hence the 8x8-board admits a tiling by 1x2-boards (with rotations allowed).

## Goal 1 - deciding
Understand for which pairs of natural numbers $(m,n)$ the mxn-board admits a tiling by 1x2-boards.

The following subtasks, covered by our authomatic feedback service, can guide you in achieving enlightment and conquer the good characterization.

* [subtask 1:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) decidere, $m = 1$
* [subtask 2:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) decidere, $m = 2$
* [subtask 3:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) decidere, $m,n \leq 20$

### Get feedback
You can get feedback either from command line with:
```
ask --problem=tiling_mxn_by_1x2 --goal=1 --subtask=SUBTASK_NUMBER file.txt 
```
or via web, by clicking on the subtask link here above and submitting the same file.

In either case, you should submit a `.txt` file of 20 lines of 20 characters each (not counting the newline characters). All chars should be either 0 or 1, where a 1 in position j of row i represents that the ixj-board admites a tiling.
For the subtask $st = 1,2$, we check out only the first $st$ lines, hence your file needs only to be correct on these first lines and can be shorter than 20 lines.


## Goal 2 - constructing

For those pairs $(m,n)$ where your answer is positive, can you also exhibit a tiling of the mxn-board?

The following subtasks, covered by feedback, can guide you in becoming a master of the tiling composition art.

* [subtask 1:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) construct, $m = 1$
* [subtask 2:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) construct, $m = 2$
* [subtask 3:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) construct, $m,n \leq 20$

The tiling, if you prefer, can be composed by hand.
However, you should pose yourself the goal to identify a general construction procedure, and of the lowest possible complxity, to yield a tiling whenever it exists. Doing this means giving a constructive proof of one of the two implications comprising the good characterization you have conjctured in goal 1. We consider this constuctive proof algorithmic if the procedure takes polynomial time (in this case in the size of the output).


### Get feedback
Again, you can get feedback either from command line with:
```
ask --problem=tiling_mxn_by_1x2 --goal=2 --subtask=SUBTASK_NUMBER file.txt 
```
or via web, by clicking on the pertinent subtask link and submitting the same file.
This time you can submit, one at the time, one or more `.txt` files structured as follows:
the first row comprises two natural numbers $m$ and $n$, both in the interval $[0,20]$, and separated by one space.
Then, with appeal to the Cardinal points (North, South, Est, West), lay down your tiling as follows.
```
8 8
WENWEWEN
WESNWENS
NWESNNSN
SNWESSNS
NSWENNSN
SWENSSNS
WENSWESN
WESWEWES
```
Notice that this example file codes the tiling of the 8x8-board seen in the picture more above.

_Note:_ This service also allows you to further interact on those grids where with goal 1 you have been told no tiling exists but you are positive on the contrary. Submit your tiling to com back in tune with us on way or the other (discover why such a thing is not a tiling or get confirmation you have a bug to signal us (thank you!)). 

In the same spirit, in case of need, you can profit of the [help service that, if you are skeptical on the existence of a tiling for the mxn-board, will dispell one for you](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml).

```
ask --problem=tiling_mxn_by_1x2 -tiling m n 
```

## Goal 3 - saying 'no'

For those pairs $(m,n)$ where your answer is negative, can you identify and possibly express a clear reason why no tiling is possible?
If we had proposed a common and agreed upon language to express the reasons for non-existence we would have inevitably spoilered this exercise.
As such, on this goal, notwithstanding its centrality and preciousness, we can not offer any meaningful authomatic feedback service. We can discuss during our meetings the most elegant and original arguments for assessing non-existence the class will collectively find out.

