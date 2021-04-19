# Yield the automaton of a regular expression

An alphabet is a finite set of symbols, like, e.g., the binary alphabet {0,1} or the alphabet of the uppercase English characters. A _string_ over an alphabet $\Sigma$ is a finite sequence of symbols taken from $\Sigma$. The length of a string $s$ is denoted by $|s|$. The _empty string_ is denoted with ε and is the only string of length $0$. The set of all possible strings over $\Sigma$ is denoted by $\Sigma^*$. When $r$ and $s$ are strings then $rs$ denotes their concatenation ($s$ is appended after $r$). A language is any subset of $\Sigma^*$. Computer science concerns means to deal with languages at various levels. One first issue is how to conveniently describe a language (most languages are infinite objects and their complexity or even decidability might vary).
_Regular expressions_ provide a fundamental basic tool to represent a class of languages with many nice properties, namely, the class of _regular languages_.  

Definition [regular expressions and languages]

Where $r$ is a regular expression, then $L_r$ denotes the regular language associated to $r$. The regular expressions over an alphabet $\Sigma$ are defined by the following rules:

1. $\emptyset$ is a regular expression and denotes the empty language $L_\emptyset=\{\}$,

2. $\varepsilon$ is a regular expression and denotes the language $L_\varepsilon=\{\varepsilon\}$ comprising only the empty string,

3. for each $e\in E$, $e$ is a regular expression and denotes the language $L_e=\{e\}$,

4. if $r$ and $s$ are regular expressions, then

   4.1. $rs$ is a regular expression and denotes the language $L_{rs}=\{\sigma_r \sigma_s : \sigma_r\in L_r, \sigma_s\in L_s\}$,
   
   4.2. $r+s$ is a regular expression and denotes the language $L_{r+s}=L_r \cup L_s\}$,

5. if $s$ is regular expressions, then

   5.1. $s*$ is a regular expression and denotes the language $L_\varepsilon \cup L_s \cup L_{ss}\cup L_{sss}\cup \ldots $,
   
   5.2. $(s)$ is a regular expression and denotes the language $L_{(s)} = L_s$.


Consider the following two issues:

1. Given a regular expression $r$ over an alphabet $\Sigma$, and a string $\sigma \in \Sigma^*$, can you decide whether $\sigma \in L_r$? 

2. Given a regular expression $r$ over an alphabet $\Sigma$, can you build an automaton (see below)that accepts the languange $L_r$? 

Moreover, regular languages enjoy nice closure properties. Among these:


1. where $L$ is a language over $\Sigma$ then $\overline{L}$ denotes its complementary language $\Sigma^*\setminus L = \{\sigma \in \Sigma^* : \sigma \not \in L\}$.
It is known that $L$ is regular iff $\overline{L}$ is regular.

2. where $L_1$ and $L_2$ are regular languages over $\Sigma$ then $L_1\cap L_2$ is regular as well.
   given a regular expression $r$, obtain a regular expression for the language $\overline{L_r}$.

And so, here are some intriguing challenges:

   given a regular expression $r$, obtain a regular expression for the language $\overline{L_r}$.

   given regular expressions $r$ and $s$, obtain a regular expression for the language $L_r\cap L_s$.

The great thing about regular expressions and languages is that while these tasks are not trivial at first, still they can be performed efficiently and by robust means that exhibit good compositional properties. Automatons offer the tools and conceptual framework to deal with all these problems with ease. 


# Services

I servizi disponibili per questo problema sono:  

* TAL_recognizes:
   you provide a regular expression $r$ and a string $\sigma\in \Sigma^*$. The service tells you whether $\sigma \in L_r$.
   
* you_recognize:
   you provide two natural numbers $m$ and $n$ in order to receive a regular expression $r$ with $|r| \leq m$ and a string $\sigma\in \Sigma^*$ with $|\sigma| \leq n$. You are asked to find out whether $\sigma \in L_r$.

   If you call this service with the argument `subcase=no_union` then $r$ will contain no '+' symbol (this is the dafault).

   If you call this service with the argument `subcase=no_star` then $r$ will contain no '*' symbol.

   If you call this service with the argument `subcase=any` then $r$ is subject to no restriction.

* eval_recognize:
   put your rcognizer under stress to check its correctness and eval its performances.


# Automatons

Automatons ...
blah ...  blah ...

# Services

I servizi disponibili per questo problema sono:  

* equivalenza di due automi deterministici/non deterministici (lo faccia TAL, lo faccia CIF in locale e lo verifichi TAL, scrivano un algoritmo i ragazzi  lo vrifichi TAL).

* da non-deterministico a determinitico equivalente (lo faccia TAL, lo faccia CIF in locale e lo verifichi TAL, scrivano un algoritmo i ragazzi  lo vrifichi TAL).

* da regular expression a non-deterministico (lo faccia TAL, lo faccia CIF in locale e lo verifichi TAL, scrivano un algoritmo i ragazzi lo verifichi TAL).

* accessibilità, coaccessibilità degli stati

* minimizzazione

* bisimulazione

* [un pò tosto ma se si nota un ragazzo] da automa non-dtrministico a espressione regolare

* complemento di linguaggio regolare



# References 

See the following online tool:
https://extendsclass.com/regex-tester.html

Christos G. Cassandras and Stéphane Lafortune, Introduction to Discrete Event Systems Second Edition

