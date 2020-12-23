# The infinite number of primes

Algorithms are proofs and proofs come with your ability to make, even just virtually (but systematically).

This is the first known example in history of a proof by absurd. 
So, assume to be given a finite set of prime numbers (that, by absurd, could be the whole set of primes), and let's play with them.

We can really act on them as tools and toys, since, we assumed, they are given to us. Let's input them to authomatic machineries of yours that will cook them up for some purpouses, achieving some tasks.

## Task 1: For example, starting from any given set $S$ of positive natural numbers, can you construct a natural number which is divisible by each one of the numbers in $S$? However, if you want this to take part in a proof with ambitions of generality, you better build an automatic answering machine that, in a never ending loop, whenever given in input a set of natural numbers, returns a common multiple of them. Mathematicians love to dwell deep enough into problems so that they could be later handled with authomatically, setting us free to think to other problems.

#### Service:
```
> TAlight connectexe check_my_task1_machine my_task1_machine
```
this will check out that your machine correctly does the job on a few instances. We assume you could give your machine the form of an executable code running on your local device (L). The `TAlight` system will connect your the input and output streams form an to your machine with those of a checking machine on our server (S).

#### Example of interaction between the two codes upon requiring the service:

S> 2 3
L> 24
S> 2 3 11 13
L> 66
S> ! I see a problem: 66 is not divisible by 13!

#### Another Example:

S> 1 3 7
L> 42
S> 2 3 5
L> 60
S> ! Correct: all tests passed!


## Task 2: And can you construct a natural number bigger than any of the numbers in $S$ but also not divisible by any of them? 

#### Service:
```
> TAlight connectexe check_my_task2_machine my_task2_machine
```
again, this will check out the correct working of your machine, giving you full feedback in case of problems.

## Task 3: Finally, given a set $S$ of prime numbers and a natural number $B$ bigger than any of them but also not divisible by any of them, can you exctract form $B$ a new prime number not contained in $S$?

#### Service:
```
> TAlight connectexe check_my_task3_machine my_new_prime_machine
```
again, this will check out the correct working of your machine, giving you full feedback in case any problems had to occur.

