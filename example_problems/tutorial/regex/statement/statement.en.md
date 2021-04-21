# Regular expressions and languages - automata theory

This unit offers:

1. an hands-on introduction to regular expressions and languages,

2. an hands-on introduction to deterministic and non-deterministic automata,

3. actual opportunities to explore the relations among them, their working, the most important operations on them, and some of their possible purposes. 

## Regular expressions and languages

An alphabet is a finite set of symbols, like, e.g., the binary alphabet $\{0,1\}$ or the alphabet $E$ of the uppercase English characters which we take as reference in all our exercises of this unit. A _string_ over an alphabet $\Sigma$ is a finite sequence of symbols taken from $\Sigma$. The length of a string $s$ is denoted by $|s|$. The _empty string_ is denoted with $\varepsilon$ and it is the only string of length $0$. The set of all possible strings over $\Sigma$ is denoted by $\Sigma^*$. When $s$ and $t$ are strings then $st$ denotes their concatenation ($t$ is appended after $s$). A language is any subset of $\Sigma^*$. Computer science concerns means to deal with languages at various levels. One first and important issue is how to conveniently describe a language (most languages are infinite objects and their complexity or even decidability might vary).
_Regular expressions_ provide a fundamental basic tool to represent a class of languages with many nice properties, namely, the class of _regular languages_.  

<strong>Definition [regular expressions and languages]</strong>

 Let $\widehat{\Sigma}$ be an alphabet containing the 5 symbols: $+$, $*$, $\emptyset$, $($, and $)$. Let $\Sigma := \widehat{\Sigma} \setminus \{+, *, (, )\}$. We denote by $R_\Sigma$ the set of all regular expressions over $\Sigma$. These are strings over $\widehat{\Sigma}$ (that is, $R\subset \widehat{\Sigma}^*$) and every regular expression $r\in R$ describes a regular language $L_r$ over $\Sigma$. The set $R$ and the map $L:R\mapsto 2^{\Sigma^*}$ are recursively defined by the following rules:

 1. $\emptyset$ is a regular expression and denotes the empty language $L_\emptyset=\{\}$,

 2. $\varepsilon$ is a regular expression and denotes the language $L_\varepsilon=\{\varepsilon\}$ comprising only the empty string,

 3. for each $\sigma \in \Sigma$, $\sigma$ is a regular expression and denotes the language $L_\sigma=\{\sigma\}$,

 4. if $s$ and $t$ are regular expressions, then

   4.1. $st$ is a regular expression and denotes the language $L_{st}=\{\omega_s \omega_t : \omega_s\in L_s, \omega_t\in L_t\}$,
   
   4.2. $r+s$ is a regular expression and denotes the language $L_{r+s}=L_r \cup L_s$,

 5. if $s$ is regular expressions, then

   5.1. $s*$ is a regular expression and denotes the language $L_\varepsilon \cup L_s \cup L_{ss}\cup L_{sss}\cup \ldots $,
   
   5.2. $(s)$ is a regular expression and denotes the language $L_{(s)} = L_s$.


Consider the following two issues:

1. Given a regular expression $r\in R_{\Sigma}$ and a string $s \in \Sigma^*$, can you decide whether $s \in L_r$? 

2. Given a regular expression $r$, can you build an automaton (see below) that accepts the languange $L_r$? 

Moreover, regular languages enjoy nice closure properties. Among these:

0. where $L_1$ and $L_2$ are regular languages over $\Sigma$ then $L_1\cup L_2$ is regular as well by definition. Indeed, consider the + operation in 4.2. In fact, each operation introduced in the definition comes with its own closure property in the family of regular languages. But here follow some more nice properties ...

1. where $L$ is a language over $\Sigma$ then $\overline{L}$ denotes its complementary language $\Sigma^*\setminus L = \{\sigma \in \Sigma^* : \sigma \not \in L\}$.
It is known that $L$ is regular iff $\overline{L}$ is regular.

2. where $L_1$ and $L_2$ are regular languages over $\Sigma$ then $L_1\cap L_2$ is regular as well.

And so, here are some intriguing challenges:

   given a regular expression $r$, obtain a regular expression for the language $\overline{L_r}$.

   given regular expressions $r$ and $s$, obtain a regular expression for the language $L_r\cap L_s$.

A great thing about regular expressions and languages is that while these tasks are not trivial at first, still they can be performed efficiently and by robust means that exhibit good compositional properties. Automatons offer the tools and conceptual framework to deal with all these problems with ease. The equivalences among automata and regular languages that we will actively explore in this journey will offer us a robust framework to address sevral problems with a standard and compositional approach. 


### Services

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


## Automatons

Automata ...

## Deterministic Automata (DFA)

blah ...  blah ...

#### Challenges

Prove that the family of languages for which there exists a DFA recognizing them is closed under:

1. union

2. complementation

3. intersection


## Deterministic Automata with $\varepsilon$ arcs (DFA$_\varepsilon$)

blah ...  blah ...

Prove that the family of languages for which there exists a DFA recognizing them is closed under:

1. union

2. complementation

3. intersection

4. composition

Now that we also have 4, it follows that the class of languages for which a DFA$_\varepsilon$ exists strictly contains the class of reguar languages.

## Non-deterministic Automata (NFA)

blah ...  blah ...


The three classes of automata introduced above (DFA, DFA$_\varepsilon$, NFA) are considered equivalent in the sense that each of them can express the very same class of languages: the class of regular languages.

Our services allow the problem solver to assess her comprehension of these equivalences. She can try to find representations equivalent to a given one by hand or by means of an algorithm (coded by herself or taken from a library). Our services will check the equivalence and provide feedback.

Example of services are:

DFA2DFAe: the problem solver is given a DFA and returns an equivalent DFA$_\varepsilon$ 

DFAe2DFA: the problem solver is given a DFA$_\varepsilon$ and returns an equivalent NFA

DFAe2DFA: the problem solver is given an NFA and returns an equivalent DFA


### Services

I servizi disponibili per questo problema sono:  

* 

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

