# How you got access to these reference solutions

If you got here then you submitted a correct solution managing large instances. What lessons can we learn at this point?

Let us discuss a few solutions for large instances, as offered in the files:

`pirellone_ILP-model-gmpl.mod`

`pirellone_LP-model-gmpl.mod`

These file have now been disclosed to you since you essentially reached the same goals they can reach.
Of the above solutions, the second shows that a compact linear programming formulation is possible for this problem. However, the IPL formulation in the first solution is almost as fast as the second. This is because the linear programming relaxation for this first model is an integral polytope.

If you got till here (or beyond?) based on different ideas, consider sharing them with us. Besides, we should also consider integrating them here among the reference solutions of this level.

You might also have reached this point by an access token, either released by the teacher or bought with credits earned by the credit system.


# Discussion of the reference solutions of this level

Alice pensaci tu cosa/come possa essere buona cosa dare qui. 

# How to address larger instances

You should first find out a good characterization for what a solvable pirellone is. Based on that, you might realize that, based only on the first row and column, you can produce a solution which is feasible iff the pirellone is solvable.
Actially, if the pirellone is solvable then the two possible solutions are precisely two. Decide for one of the two, compute it by O(m+n) propagation, and spend O(m*n) only for the checking.