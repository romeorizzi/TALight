# Tait colorings

In the year 1880, the distinguished University of Edinburgh professor Peter Guthrie Tait published his own proof of the Four Color theorem. Much like other attempts that have been made over the years, Tait’s proof contained an oversight. However Tait’s efforts resulted in a legitimate and very important contribution to graph theory and its formulation of the Four Color Theorem is the one used in all the proofs currently recognized as correct.

At the time of Tait, the Four Color problem was the following:

Conjecture 4CT: Every planar graph $G = (V, E)$ admits a coloring $c: V \rightarrow \{1,2,3,4\}$ of its nodes assigning different colors to the two endpoints of every edge in $E$.

The target of this exercise is to explore the proof of Tait that the Four Color theorem is equivalent to the following conjecture:

Conjecture Tait: Every planar bridgeless cubic graph $G = (V, E)$ admits a coloring $c: E \rightarrow \{1,2,3\}$ of its edges assigning different colors to any two edges incident with a same node.


The proof is split in two:

1. the conjecture of Tait implies the Four Color theorem

2. the Four Color theorem implies the Conjecture of Tait

## The conjecture of Tait implies the Four Color theorem

Given a planar graph $G_4 = (V_4, E_4)$, Tait showed how to construct a planar cubic graph $G_3 = (V_3, E_3)$ and gave a procedure to transform any possible $3$-edge coloring of $G_3$ into a $4$-coloring of $G_4$.

### We describe in words how to construct $G_3$ given $G_4$

First we add edges to $G_4$ to transform it into a triangulated simple graph $G'_4$, by adding edges as needed.
Graph $G_3$ is just the [dual graph](https://en.wikipedia.org/wiki/Dual_graph) of $G'_4$.


## Servizi offerti

Limitiamo ai 3-connessi non perchè la costruzione di Tait non valga anche al di fuori ma per evitare di complicare le cose per il fatto che alcuni grafi planari (non 3-connessi) ammettono più planar embedding e, di conseguenza, il grafo duale non è univocamente definito. 

G4: Nodi numerati da 0 a n-1, archi numerati da 0 a m-1.

G'4: Nodi numerati da 0 a n-1, archi numerati da 0 a m'-1, dove m'=m+t e sui primi m archi la numerazione è quella di G4.


1. dato un grafo planare 3-connesso G, dire quanti archi t devono essere aggiunti a G per ottenere un grafo planare triangolato e semplice. (il server lo fà | il server lo verifica)

2. Costruttore di un G4' dato G4. (il server lo fà | il server lo verifica)

3. Dati G4' e una 4-colorazione di G4' ottenere una 4-colorazione di G4.

4. Costruttore di G3 dato G4'. (il server lo fà | il server lo verifica)

2+3. Direttamente G4 --> G3. (il server lo fà | il server lo verifica)

5. Dati G4' e  G3, un edge-coloring di G3, e un colore C in {1,2,3} ottenere una 2-colorazione delle facce del planar embedding di G3 tale che ogni due facce adiacenti abbiano colore opposto se e solo se l'arco di bordo tra di loro è diverso da C. (Per rappresentare questo coloring, conviene pensare di colorare i nodi di G4 dato che sono in corrispondenza biunivoca delle facce di G3 che altrimenti non vorremmo dover gestire). (il server lo fà | il server lo verifica)

6. Dati G4' e  G3, un edge-coloring di G3, ottenere una 4-colorazione delle facce del planar embedding di G3 tale che ogni due facce adiacenti abbiano colore diverso. (Come sopra, usiamo i nodi di G4' come nomi delle facce nel planar embedding di G3). (il server lo fà | il server lo verifica)

7. Dati G4' e  G3, un edge-coloring di G3, ottenere una 4-colorazione di G4'



## Four Color theorem implies the Conjecture of Tait



### Servizi di gioco

```t
> rtal connect -a num_rounds=10 morra play
```
Per farsi una partitina di 10 raggi. Per meglio conoscere i parametri di questo servizio:  
```t
rtal list -v morra 
```
Per scoprire come far giocare un bot al proprio posto:
```t
rtal connect --help
```
In future versioni di `TALight` vorremo introdurre il supporto multi-giocatore.