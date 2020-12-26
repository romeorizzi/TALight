# The infinity of natural numbers

Algorithms are proofs and proofs most often come with algorithms.

## Task 1: Implement an automatic machine (an executable code) that, in a never ending loop, whenever given in input a natural number, returns a bigger one

This machine will prove two things:

1. there is no such a thing as the biggest natural number;

2. there is an infinite amount of natural numbers out there.

Input from `stdin` and output to `stdout`, each line just a number, the format of each line is a sequence of digits followed by newline. The very first digit might be a zero if and only it the represented number is zero.

### Service

```t
> TAlight connectexe bigge_and_bigger my_machine
```

will play the game to whom shoots out the biggest natural against your machine.
A sequence of relentless overtakes where the server will have to throw in the sponge soon or later.


## Task 2: After implementing the above procedure, you might also be tempted to prove Archimede's principle that states that, given any positive real number $\varepsilon$, there exists a natural $N_\varepsilon$ such that $\frac{1}{N_\varepsilon} < \varepsilon$

Implement then an automatic machine that, in a never ending loop, whenever given in input a natural number, returns a bigger one.
Input and output as above, only that in the representation of a real number, one single occurrence of the full dot character '.' might sneak in somewhere inbetwen two digits. The very first digit might be a zero if and only it is not immidiately followed by another digit.

### Service

```t
> TAlight connectexe rationals_are_dense_into_reals my_Archimede
```

