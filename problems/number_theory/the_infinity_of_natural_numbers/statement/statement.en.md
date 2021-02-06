# infinity_of_N (the infinity of natural numbers)

Algorithms are proofs and proofs most often come with algorithms.

## Task 1: Implement an automatic machine (an executable code) that, in a never ending loop, whenever given in input a natural number, returns a bigger one

This machine will prove two things:

1. there is no such a thing as the biggest natural number;

2. there is an infinite amount of natural numbers out there.

Input from `stdin` and output to `stdout`, each line just a number, the format of each line is a sequence of digits followed by newline. The very first digit might be a zero if and only it the represented number is zero.

### Services

Lounch

```t
> rtal connect infinity_of_N bigge_and_bigger
```

to play yourself the game to whom shoots out the biggest natural against your machine.
A sequence of relentless overtakes where the server S will have to throw in the sponge soon or later (if you do not make mistakes).

To make sure you can not make mistakes (i.e., to obtain a proof of something), you can trow in a simple bot of yours to play in your place with

```t
> rtal connect infinity_of_N bigge_and_bigger -- my_bot.py
```

here `my_bot.py` is just the full name of an executable sitting on your local machine. This will involve your bot into a (potentially) never ending play against S.


## Task 2: After implementing the above procedure, you might also be tempted to prove Archimede's principle that states that, given any positive real number $\varepsilon$, there exists a natural $N_\varepsilon$ such that $\frac{1}{N_\varepsilon} < \varepsilon$.

Implement then an automatic machine that, in a never ending loop, whenever given in input a positive real number $\varepsilon$, returns such a natural $N_\varepsilon$ such that $\frac{1}{N_\varepsilon} < \varepsilon$.
Input and output as above, only that in the representation of a real number, one single occurrence of the full dot character '.' might sneak in somewhere inbetwen two digits. The very first digit might be a zero if and only it is not immidiately followed by another digit.

### Services

We have choosen to give two different names to this service:
use either `rationals_are_dense_into_reals` or `archimede`, to your will,
and use the flexible syntax of the TAlight command `rtal` introduced above to call for this service.
If you want to know more about `rtal` lounch
```t
> rtal --help
```
or 
```t
> rtal connect --help
```

If you want to know more about the parameters of the services of a problem run

```t
> rtal list infinity_of_N - v
```

## Examples of interactions (possible plays)

In the examples, the rows sent by the server of the service designd by the problem maker are prefixed with "S> ", whereas those sent by the local agent (either you or your bot) are prefixed with "L> "):


### Task 1

```t
S> # hello! Let's play to whom shoots the biggest natural number.
S> # I'll be the one to start, and then we take turns.
S> 42
L> 50
S> 55
L> 60
S> # good shot!
S> 1000
L> 2000
S> ok! vero! 42=11+31
S> ! I throw the sponge. Nice play :)
```
As you see, lines starting with '#' should be treated as comments and are just ignored by the two main agents in the conversation (the bots).
A line starting with '!' from the side of the server closes the connection when no error on the protocol level occurs. The rest of this closing line can once again be an arbitrary comment.

### Task 2

The general structure of the protocol is the same as above.

```t
S> # hello! You are in charge to prove me that rationals are dense into the real. We could cast this in the form of a game. Now it is time for a play!
S> # I'll be the one to start, and then we take turns.
S> 42
L> 50
S> 55
L> 60
S> # good shot!
S> 1000
L> 2000
S> ok! vero! 42=11+31
S> ! I throw the sponge. Nice play :)
```
