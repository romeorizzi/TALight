# infinity_of_N (the infinity of natural numbers)

Algorithms are proofs and proofs most often come with algorithms.

## Task 1: Prove that there exist infinitely many natural numbers

If you have this competence:

    whenever given a natural number you know how to produce a bigger one

then you are already convinced of two things:

    Fact: there is no such a thing as a biggest natural number.

    Corollary: there is an infinite amount of natural numbers out there.

<details><summary>Where the corollary directly follows from the fact.</summary>

Indeed, we assume that our notion of "bigger" (in symbols, the $>$ relation) enjoys the following two properties:

1. We are not distinguishing the equals: if $a > b$ then $a$ and $b$ are different naturals.

2. Transitivity: if $a > b$ and $b > c$ then $a > c$.
</details>

To start with, we invite you to exhibit the above competence in a race at calling out bigger and bigger numbers. Try playing yourself against [the service `bigger_and_bigger`](#service-bigger_and_bigger) of this didactic problem of the TALight tutorial. And then, once you have gathered enough confidence, you might want to instruct a bot to play on your behalf. See the detailed instructions on the service to see how this can be done.  

<details>
<summary>What will you prove as a result of your making</summary>

When you can effectively teach a competence bearing consequences as the above fact and corollary your prescription will inevitably constitute a proof of both. With your bot (an automatic answering machine) written in some standardized and official language, your proof is formal and precise to the point that it actually runs. Yes, the bot might also fail depending on the limitations of your local system, but this should not be our concern. What matters here are the simple and archetypal ideas you have put into it, their validity transcend these limits. When your bot runs fine within these limitations (no real computer will ever have an infinite amount of memory or CPU's clock ticks), then you should feel reassured enough they constitute a correct algorithmic proof (even better than just a proof) that stands for eternity in the hyperuranion.  
</details>


## Task 2: Let's now prove Archimede's principle: the rationals are dense into the reals.

Did you enjoy the previous challenge? Implement then an automatic machine that, in a never ending loop, whenever given in input a _positive_ real number $\varepsilon > 0$, returns a _positive_ natural number $N_\varepsilon > 0$ such that $\frac{1}{N_\varepsilon} < \varepsilon$.

<details><summary>What will you prove as a result of your making</summary>

With your bot you have proven a basic fact placed at the grounds of the mathematical analysis building:

    Fact: the rationals are dense into the reals.

What is meant with this dense sentence is:

*    however one fixes two different real numbers $a$ and $b$, say $a<b$, then there always exists a rational number $q$ that sits between the two and separates them, namely, $a<q<b$.

This fact is at the basis of [any construction or even definition that has been proposed for the field of the real numbers](https://en.wikipedia.org/wiki/Construction_of_the_real_numbers). Indeed, it occurs as one of the axioms in the synthetic approach.

**A consideration for to the instructor.** The term "construct" has a much stronger meaning to us. We reserve it only to finite representations of objects that can be computed in finite time. A [real number is computable](https://en.wikipedia.org/wiki/Computable_number#:~:text=A%20real%20number%20is%20computable%20if%20its%20digit%20sequence%20can,digits%20following%20the%20decimal%20point.) if its digits can be produced by some algorithm or Turing machine when given the position of the digit as input. As such, the computable reals are countably many and yet,  countably many of them are not constructible in our sense. We ask our problem solvers to build constructive proofs or constructive core features of what could be a proof. By this we mean providing the means for the construction of finite objects, while these means are meant to be applicable in general (on an infinite number of possible calls). Though the checking of these proofs might hardly be a finite task, we observe that most often we can actually content ourselves with checking the validity of the constructions only over rather limited instance spaces. A finite prefix of an infinite dialogue is more than enough for the apprentice to get all the feedback he needs as a check on the validity of his proof and on the comprehension he has got. Of course, the more we go higher in spaces and the more we expect the apprentice to be collaborative and work for the system rather than at breaking it. Since the spaces for non-sense are more widely infinite than those of meaning ("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe." - Albert Einstein), we ought to trust our problem solver to opt for the challenges of meaning. Besides, any didactic or educative effort has to cope with this limit: "If you are not willing to learn, no one can help you. If you are determined to learn, no one can stop you" (Zig Ziglar). Security would kill the cat, so we go for the opposite spectrum.  

You have really constructed your $N_\varepsilon$, at least for those $\varepsilon$ that possessed a finite representation. In fact, you probably came out with solutions that would truly hold for any real $\varepsilon$, even for a non constructible (and even a non computable) one.
Yes, you might be scared your method might not work with a real like $1-0.\overline{9}$.

Does it work here?

We bet not. But ... look, it is not your fault!

The point here is that $1-0.\overline{9} = 0$ since $0.\overline{9}$ equals $1$.

Indeed, assume $0.\overline{9}$ and $1$ where different, then there should be at least one real in the middle, namely $(1+0.\overline{9})/2$. Do you see any space left for this one real? Also, the difference $1-0.\overline{9}$ would be an infinitesially small number. But no single real can be neither infinitum nor infinitesimal.

Both of these arguments are also proofs, since ["once you eliminate the impossible, whatever remains, no matter how improbable, must be the truth"](https://en.wikiquote.org/wiki/Sherlock_Holmes) (Arthur Conan Doyle).

Yes, for puzzling as it might seem at first, you have just discovered that the decimal representations of a real number are not unique. "All truth passes through three stages. First, it is ridiculed. Second, it is violently opposed. Third, it is accepted as being self-evident" (Arthur Schopenhauer).
Now that you know this fact you can be reassured about the generality of your method (the one at the hearth of your bot, its very spirit, its underlying algorithm):

    Fact: every decimal representation of a real $\varepsilon$ which is not an integer has a non-zero digit after the '.'.

 The position of this digit is all what you need to take into account in order to obtain a $N_\varepsilon$ guaranteed to work fine. And this is what you did at the bare bones.
</details>

### Service bigger_and_bigger

Launch

```t
> rtal connect infinity_of_N bigger_and_bigger
```

to play yourself the game to whom shoots out the biggest natural against our service provider program S. A sequence of relentless overtakes will then take place between S and you, where S will have to throw in the sponge soon or later (if you do not make mistakes).
Program S may be located and run on your local machine or in the cloud: which one of the two applies depends on how you instructed the TALight daemon `rtald` when you launched it.

To organize yourself as an ever winner (i.e., to obtain a general proof of something), you can trow in a simple bot of yours to play in your behalf with

```t
> rtal connect -e infinity_of_N bigger_and_bigger -- ./my_bot.py
```

here `./my_bot.py` should be interpreted as the full name of an executable sitting on your local machine. This will involve your bot into a (potentially) never ending play against S.
Your bot is a binary executable code compatible with your architecture, however you obtained it (compilers, assemblers, ...), but can also be a prescription or script in an interpreted language like python or a bytecode (as long as your local machine has the corresponding interpreters or virtual machines installed). Compatibility on your side is your own issue.


### Service archimede

Also for this task we have thought of one single service. However, this time we have registered it under two different names:
use either `rationals_are_dense_into_reals`, or `archimede` for short, at your will.
Also, exploit the possibilities offered by `rtal` and the flexibility of the service according to the general `rtal` usage syntax and the service parameters. You get to know more about all these in the following two expansible points.

<details>
<summary>Want to know more about the general usage of the `rtal` command?</summary>

If you want to know more about `rtal` launch
```t
> rtal --help
```
or 
```t
> rtal connect --help
```
</details>

<details>
<summary>Want to know more about the parameters of the services of a specific problem?</summary>

If you want to know more about the parameters of the services of a problem run

```t
> rtal list infinity_of_N - v
```
</details>


## Examples of interactions

In the examples, the rows sent by the server of the service designed by the problem maker are prefixed with "S> ", whereas those sent by the local agent (either you or your bot) are prefixed with "L> ".

<details>
<summary><strong>Task 1</strong></summary>

Assuming you launched

```bash
rtal connect -a num_rounds=10 -a lang=eninfinity_of_N bigger_and_bigger
```
with the `rtald` daemon correctly activated, then a dialogue like this could take place between the server (S) and you (L):

```t
S> # I will serve: problem=infinity_of_N, service=bigger_and_bigger, num_rounds=10.
S> # Hello! Let's play to whom shoots the biggest natural number.
S> # I'll be the one to start, and then we take turns. You will be given the chance for the last word (always just a number).
S> 15
L> 20
S> 26
L> 30
S> 35
L> 50
! I give up. You won! Nice play :)
```
As you see, lines starting with '#' should be regarded as comments that can be ignored by the two main agents in the conversation. The server immediately drops the connection as soon as it detects a violation of the protocol of the service. The server closes the connection and returns the terminal back to your control also in case the intended dialogue has come to completion. You can easily detect which one of the two drop outs has occurred: a line starting with '!' from the side of the server closes the connection when no error on the protocol level has occurred. The rest of this closing line can once again be an arbitrary comment, as you can see in the example above.

If you write a bot, it does not need to write out any comments (though you might find them fun or useful for debugging purposes) and only needs to skip and ignore those lines starting with '#'. This is good also because other services could be activated through these lines, which opens the possibility of an extensible ecosystem of services and tools. When playing yourself, the comment lines from the server might on the contrary be of some help in many ways.
Back to the specs for your bot: Input from `stdin` and output to `stdout`, each line just one single number. More precisely: the format of each line is a sequence of digits followed by newline; the very first digit in the sequence might be a zero only if it is also the last one, and the represented number is zero.

You can trow in your bot of yours to play in your behalf with

```t
> rtal connect -e infinity_of_N bigger_and_bigger -- ./my_bot.py
```

here `my_bot.py` is just the full name (aka filename with path) of an executable sitting on your local machine. Your bot should either be a binary executable code compatible with your architecture, however you obtained it (compilers, assemblers, ...), or a prescription or script in an interpreted language like python or a bytecode. This also works fine as long as your local machine has the corresponding interpreters or virtual machines installed. Compatibility on your side is your own issue. If the bot works correctly on your machine then it will be correctly connected by `rtal`. You can check/test/debug your both by running it as alone. In the case of our both, we could have issued
```t
> ./my_bot.py
```
and tested the bot in isolation conducting ourselves a dialogue with it through the terminal.
</details>

<details>
<summary><strong>Task 2</strong></summary>

The general structure of the protocol for this service is the same as for Task&nbsp;1. The only difference is that, as you can see, the server S now plays decimal representations of real numbers. Here, at most one single occurrence of the full dot character '.' may be present, all other characters being digits. However, the very first character is guaranteed to be a digit. Moreover, this first digit might be a zero only when immediately followed by the '.'. Finally, the very last digit might be a zero only if the '.' character is not present.


```t
S> # I will serve: problem=infinity_of_N, service=archimede, num_rounds=5.")
S> # Hello! You are in charge of convincing me that rationals are dense into the real."
S> #  We cast this in the form of a game:
S> #     I offer you a positive real and you should reply with a natural whose inverse is strictly smaller than the real.
S> 11.7
L> 1
S> 0.1
L> 11
S> 0.09
L> 50 
S> 0.02
L> 100
S> 0.01
L> 101
! I give up. You won!
```
</details>

All possibilities we have mentioned above for the previous task are also open here, like for any other TALight problem service.
