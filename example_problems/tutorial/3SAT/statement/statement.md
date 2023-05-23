# 3-SAT is NP-hard (Karp, 1972) 

## Introduction

### SAT

### k-SAT and 3-SAT


### Let's play

Can you represent the 4-clause $C=(x_1 \vee x_2 \vee x_3 \vee x_4 )$
by using only 3-clauses?

The answer might be: it depends on what the hell you mean.

#### Interpretation 1:

Does there exist a conjunction $c$ of 3-clauses over $x_1, x_2, x_3, x_4$ such that the two boolean functions $C(x_1, x_2, x_3, x_4)$ and $c(x_1, x_2, x_3, x_4)$ are equivalent (i.e., C(x_1, x_2, x_3, x_4) = c(x_1, x_2, x_3, x_4)$ for every $(x_1, x_2, x_3, x_4)\in \{0,1\}^4$).

Does such a conjunction $c$ exist?


#### Interpretation 2:

Does there exist a conjunction $c$ of 3-clauses over an extended set $\{x_1, x_2, x_3, x_4, y\}$ such that the following holds for each $(x_1, x_2, x_3, x_4)\in \{0,1\}^4$:

1. if $C(x_1, x_2, x_3, x_4)=0$ then $c(x_1, x_2, x_3, x_4, y)=0$ for every $y\in \{0,1\}$
    
2. if $C(x_1, x_2, x_3, x_4)=1$ then there exists a $y\in \{0,1\}$ such that $c(x_1, x_2, x_3, x_4, y)=1$

Does such a conjunction $c$ exist?

---
x1 x2 xn  y1 y2 y3   ym  m<=n

()

!

and

or

---

Nel primo challenge noi proviamo tutti i possibili max 2^{20} truth assignments per X+Y.

---


### Second challenge

Sustain the following dialogue:

Basic Dialogue:

Step 1. Initial Input:
   1. A 4-SAT formula $f$ over a set of boolean variables $X := \{x_1, x_2, \ldots , x_n\}$. 
   2. optional: a truth assignment $t:X \mapsto \{0,1\}$ such that $f|_t = 1$.

Step 2. Your First Output: A 3-SAT formula $f_3$ over a set of boolean variables $X\cup Y$ such that $f_3$ is satisfyiable iff $f$ is satisfyiable.
In case the optional truth assignment $t$ is provided, then return also a truth assignment $t':X\cup Y \mapsto \{0,1\}$ such that $f_3|_{t'} = 1$.  

Step 3. A possible Come Back of the Server:
The server might now give you a truth assignment $t'':X\cup Y \mapsto \{0,1\}$ such that $f_3|_{t''} = 1$. If this is the case, then you must reply with a satisying truth assignment for $f$.

The server can decide to repat the Basic Dialogue as many times as it needs.

Note: we require that your reduction from 4-SAT to 3-SAT is deterministic. This means that when assigned the sameA 4-SAT formula $f$ in Step 1, you should always return the same formula $f_3$ in Step 2.



(x1 or x2 or x3 or x4) --> (x1 or x2 or y) and (!y or x3 or x4)


(x1 or x2)  --> (x1 or x2 or y) and (x1 or x2 or !y)

(x1) --> (x1 or y) and (x1 or !y)

(x1) = (x1 or x1 or x1)

