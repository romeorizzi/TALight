# The unicity of the factorization in primes

The unicity of the factorization in primes, called _the fundamental theorem of natural numbers_, was proven in th 7th book of the _Elements of [Euclides](https://en.wikipedia.org/wiki/Euclid)_ around 300BC.

It states:
> _Every natural number $n$ bigger than $1$ is a product of prime numbers, and this offers an unique representation of $n$._

Among the natural numbers, $0$ and $1$ each have their very special place.
For this reason, $0$ is called the _zero_ and $1$ is called the _unity_. The theorem has nothing to say about them (they are uniquely represented as $0$ and $1$, that is, in terms of themself, and can not play any role in the representation of any other number).
On the contrary, for every other number $n$ we make a distinction into two possibe cases:
  if $n=a\cdot b$ with $a,b>1$, then $n$ is called a _composite_ number,
  otherwise $n$ is called a _prime_. In the second case $n$ can be employed in the representation of other numbers, and, in particuar, $n$ can be represented only in terms of itself.

Clearly, if we are in the first case then we could obtain a represntation of $n$ as a product of primes out such representations for $a$ and $b$, given that $n=a\cdot b$ and working inductively.
As such, the true issue is in proving the uniquness of the representation.

A moment's thought reveals this is equivalent to the following claim (Lemma 2 of the 7th book):

   if a prime $p$ divides $n=a\cdot b$ then $p$ divides either $a$ or $b$.

Indeed, if we had a triple $(a,b,p)$ contradicting the above claim then prepending one $p$ factor to a representation of $n/p$ yields a representation of $n$ including at least one $p$ factor for sure whereas a representation of $n$ including no $p$ factor is obtained joining a representation for $a$ and one for $b$.
Conversely, assuming the claim, then every $p$ factor should show off in every rpresentation of $n$. That is, if $p^k$ divedes $n$ then the number of factors in the representation of $a$ plus the number of factors in the representation of $b$ should be at least $k$.

Therefore, to guide you in producing a proof of the above claim (and discover what Euclide did discover on this track), we pose you a few tasks.

## Task 1: characterize coprimality

Two numbers are coprime iff their only common divisor is $1$.
A certificate of non-coprimality would hance be a common divisor bigger than $1$.
As such, the problem of deciding coprimality belongs to coNP (we can convince King Arthur in the negative case). Actually, we suggest the following formulation embedding a _good conjecture_, i.e., a conjcture that, if it were true, would place the problem in NP $\cap$ coNP:

INPUT: two positive naturals $a$ and $b$.
TASK: in case $a$ and $b$ are NOT coprime, it should answer NO (returning the integer value 0 on the first line of `stdout`) but also provide a certificate returning some common divisor $d > 1$ on the second line of `stdout`.
In case $a$ and $b$ are coprime, it should answer YES (returning the integer value 1 on the first line of `stdout`) but also provide a certificate returning two integers $x$ and $y$ such that $xa+yb = 1$.

To see why we have conjectured a universal and effectively checkable crtificate of YES, consider that if $xa+yb = p > 0$ then every common divisor $d$ to $a$ and $b$ should also divide $p$, and so $d\leq p$.

