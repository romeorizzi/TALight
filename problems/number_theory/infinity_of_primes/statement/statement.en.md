# infinity_of_primes (The infinite number of primes)

The proof that there exists an infinite number of primes was contained in the [seventh book of Euclid](https://mathcs.clarku.edu/~djoyce/elements/bookVII/bookVII.html).
This is the first known example in history of a proof by absurd. Of course, proofs by absurd may lack of constructive counterparts. We will however maintain our commitment for algorithms and concreteness. A subtitle for this unit could have been:

    Algorithms are proofs and, most often, proofs come with our ability to make, even just virtually (but systematically).

We will see how this truth manifest itself in this very special example of a proof by absurd.

Proving a statement means drawing its thesis starting from its hypothesis. The more hypothesis we have the easier is our job since we have more usable stuff at our disposal. This phenomenon manifests itself very well even when the proof amounts to just a finite case checking, since the length of the case analysis might be significantly shortened.

<details>
  <summary>Here is a nice example with a famous puzzle.</summary>
Three explorers got captured by a tribe of cannibals.
They woke up tied up at three different poles disposed in circuit so that each on of them could see the other two and the hat that was posed on their heads.
The tribal chief explained them that 5 hats, two black ones and three white ones had been sanctified by him, and then two of them had been randomly picked up and burnt, whereas the other three were sitting on their heads. He then proposed to one of the prisoners:

> if you can tell me the color of the hat on your head I will set you free. If you attempt and fail you will die in the most terrible pains and regret. However, you can also give up and in that case I will cut off your head so that no pain will be with you.

The prisoner thought about it attentively but then, in great sweat and despair, asked the grace to be killed but not tortured.

After this, the very same story repeated with the second prisoner.

And then came your turn: you are the third prisoner and know that both hats on the other two prisoners were white.

What shall you answer?

<details>
  <summary>Here is the correct answer:</summary>
The hat on your head is white.
You can be sure of this by assuming that no one would have asked to be killed in case he knew for sure.
Organize then your own proof of the fact that your hat is white, and try to be short.

<details>
  <summary>Here is a short proof:</summary>
  If the hat was black (absurd) then the second man asked would have known for sure his hat was white for othrwise the first man would have known for sure his hat was white.
</details>
</details>

</details>

___
But the advantage of having one extra information can be much bigger than a shortening in the arguments. This happens when we had nothing in our hands to start out for a proof and the false assumption gives us something concrete to start with.


So, back to Euclid, assume to be given _the_ finite set of prime numbers, and let's play with them.

We can really act on them as tools and toys, since, we assumed, they are given to us. Let's input them to automatic machine of your design that will cook them up for some purposes, eventually achieving the suggested tasks through the rising of a contradiction.

For example, here comes your first task.

## Task 1: starting from any given set $S$ of prime numbers, can you construct a natural number which is divisible by each one of the numbers in $S$?

Build a bot (an automatic answering machine) that, when given in input such a set $S$ of prime numbers, returns a common multiple of them all. Mathematicians love to dwell deep enough into problems so that they could be later handled with automatically, setting us free to think to other problems.

### Service

```t
> rtal connect infinity_of_primes common_multiple
```

to play yourself and experiment with the problem and the service.

```t
> rtal connect -e infinity_of_primes common_multiple -- common_multiple_bot
```

to let your bot `common_multiple_bot`, i.e. an executable program of which you provide the full path, to play on your behalf.

Either way, this service will check out that your machine correctly does the job on a few instances. We assume you could give your machine the form of an executable code running on your local device (L). The `TAlight` system will connect your input and output streams or those of your bot acting in your place with those of a checking machine (S) implementing this service and possibly running on an external server in the cloud.

#### Example of interaction between the two codes upon requiring the service

```t
S> 2 3
L> 24
S> 2 3 11 13
L> 66
S> ! I see a problem: 66 is not divisible by 13!
```

#### Another Example

```t
S> 1 3 7
L> 42
S> 2 3 5
L> 60
S> ! Correct: all tests passed!
```

## Task 2: Can you now construct a natural number bigger than any of the numbers in $S$ but also not divisible by any of them?

<details>
<summary>What will you prove as a result of your making</summary>
With your bot (an automatic answering machine) you have proven that there exists an infinite number of primes.

    Fact: there exists an infinite number of primes.

Here is why:

Assume not. Let $P$ be the finite set of prime numbers. Let $n$ be the number that your bot returns when you feed it with $S=P$.
Then $n>1$ and is not divisible by any of the primes in $P$.
We now exploit the following claim (if you are unsure about the truth of the claim we will investigate it more closely in Task 3).

    Claim: every natural $n>1$ is a product of a prime $p$ times another natural.
    
By the above claim, we know we can write $n=pn'$ where $p$ is a prime and $n'$ is some natural.
Clarly, no prime in $P$ divides $p$ otherwise it would also devide $n$.
As such, $p$ is a new prime, different from any prime in $P$.  
</details>


### Service

```t
> rtal connect -e infinity_of_primes common_non_multiple -- common_non_multiple_bot
```

again, this will check out the correct working of your bot, giving you full feedback in case of problems.
And remember that before designing or implementing your bot you can always first directly chat with the service to try it out and get intuitions with the problem at hand.

## Task 3: extracting a prime factor from any natural $n>1$

With this task we make sure to be clear with this claim and its proof.

    Claim: every natural $n>1$ is a product of a prime $p$ times another natural.
    
    Indeed, if $n$ itself is a prime then consider $n$ as the product of itself times $1$. Otherwise $n$ is a composite number, that is, $n=ab$ with $a$ and $b$ natural numbers such that $1 < a,b < n$. Apply induction on $a$: since $1 < a < n$ then we can apply induction on $a$ to conclude that $a=pq$ with $p$ a natural number. At this point $n=ab=(pq)b=p(qb)$ and the claim follows.

Can you turn this proof into a bot that wins the following game:

    The server S proposes a natural $n>1$ to begin a match with you (L):
        you can send a number $n'$ to the server and:
            if $n'$ is a prime divisor of $n$ then you win immidiatly.
            if $n'$ number is not a divisor of $n$ then you loose immidiatly.
            if $n'$ is not prime then S returns you two naturals $a, b > 1$ with $ab=n$.  

### Service

```t
> rtal connect -e infinity_of_primes extract_prime -- extract_prime_bot
```

## General Remark

Lounch

```t
> rtal list infinity_of_primes -v
```

to find our more about the parameters specific to the various services.
If you want to know more about the general possibilities offered by TAlight around the services of the problems then issue

Lounch

```t
> rtal connect --help
```

To know about other TAligh commands and what they offer you then issue

Lounch

```t
> rtal --help
```