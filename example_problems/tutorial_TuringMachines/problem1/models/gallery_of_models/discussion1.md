# How you got access to these reference solutions

If you got here then you submitted a correct solution managing instances up to a certain size.

Let us discuss such a kind of solution, as offered in the files:

`pirellone_ILP-model-gmpl.mod`

An ampl version of this is given in:

`pirellone_ILP-model-ampl.mod`

All these files have now been disclosed to you.

If you got till here based on different ideas, consider sharing them with us. Besides, we should also consider integrating them here among the reference solutions of this level.

You might also have reached this point by an access token, either released by the teacher or bought with credits earned by the credit system.


# Discussion of the reference solutions of this level

Alice pensaci tu cosa/come possa essere buona dare qui. 


# Hint to the next level

When modeling a problem like this as an ILP (Integer Linear Programming) problem, you are then asking the solver (glpsol, CPLEX, Guroby, ... ) to solve an NP-hard problem, which requires a lot of computational power, and, when the size of the instance grows (that is, when N grows), very soon you end up that all the computational power you can ask for is not enough.   

However, problem Pirellone can be solved in polynomial time. In fact you might notice it has a very peculiar structure: either it admits no solutiono or it admits precisely two solutions (once the Pirellone is solved, then every light is also turned off after if you flip every row and every column). Thus the space of feasible solutions is rigidly structured, essentially you have at most one of them and could determine it by propagation after having fixed one switch, which you can always do without lost of generality by the existence of the double solution mentione above. More in general, such a rigid structure suggests the problem is amenable of a linear programming formulation.

Once you have understood the mathematical structure, and possibly the polyhedral structure, of the feasible solutions to the Pirellone problem, you might come up with a mathematical model of the triangle problem that does not throw away its desirable computational properties.
Can you exploit these insights as a push to design a less expensive model in the language of Linear Programming (LP)?
LP is known to be in P and very practical algorithms are known for it and are implemented in all the solvers mentioned above.
