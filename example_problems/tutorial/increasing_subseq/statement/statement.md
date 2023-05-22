# Massima sottosequenza crescente 

Questo problema è noto come [Poldo](https://training.olinfo.it/#/task/poldo/statement) in ambito olimpiadi di informatica.

Sia $T$ una sequenza di oggetti di un dato tipo (ad esempio caratteri o numeri). Quando dalla sequenza si rimuovano alcuni dei suoi elementi quella che resta è una __sottosequenza__.

Ad esempio, le sottosequenze di $T= 1,2,3$ sono le seguenti $8$ sequenze:

```
1,2,3
1,2
1,3
2,3
1
2
3

```

Invece, le sottosequenze diverse di $T= A,B,B$ sono solamente le seguenti $7$ sottosequenze: 

```
A,B,B
A,B
B,B
A
B

```

Una sequenza $T= t_1, t_2, \ldots, t_n$ di numeri naturali si dice __strettamente crescente__ se $t_j > t_i$ per ogni $i,j$ con $1\leq i < j \leq n$. Quì $n$ è la __lunghezza__ della sequenza.
La sequenza è detta __non-decrescente__ se $t_j \geq t_i$. Quindi strettamente-crescente implica non-decrescente ma non il contrario.

In questo problema assumiamo ti venga fornita una sequenza $T$ di numeri naturali. Il tuo compito è reperire una sottosequenza (strettamente) crescente di $T$ della massima lunghezza possibile. 


## Servizi offerti e competenze che potresti assicurarti di avere

Date due sequenze $s$ e $T$, sapresti stabilire se $s$ è sottosequenza di $T$? 

Se ti venisse detto che gli $n$ elementi di una sequenza sono tutti diversi, sapresti dire quante sono le sue sottosequenze diverse?

Se ti viene specificata una sequenza di numeri naturali, sapresti calcolare quante sono le sue sottosequenze diverse? Sapresti generarle tutte o listarle in ordine lessicografico e farne ranking ed unranking?

<details><summary>In questo contesto __ordine lssicografico__ significa ... </summary>

Partiamo dall'ordine totale ovvio sui numeri, dove ad esempio abbiamo:
\[
   0<1<2<3<4<5<6<7<8<9<10
\]

Sulla base di questo, l'ordine tra due sequenze è determinato dalla segunte procedura:

INPUT: due sequenze $a=a_1, \ldots, a_m$ e $b=b_1, \ldots, b_m$ di numeri naturali.

<code>
for i:=1 to min(m,n):
  if a<sub>i</sub> < b<sub>i</sub>:
    return "a<b"
  elif b<sub>i</sub> < a<sub>i</sub>:
    return "b<a"
if m > n:
    return "b<a"
elif n > n:
    return "a<b"
else:
    return "a=b"
</code>

</details>


Data in input una sequenza $T$, sapresti calcolarne una sottosequenza di massima lughezza?

Quanto efficiente è il tuo metodo? (Esponenziale, polinomiale, quadratico, meno di quadratico, .... (nella lunghezza di $T$) ).

## Caratterizzare l'ottimalità.

Supponiamo di assegnare $k$ colori agli $n$ elementi di $T$ (tramite una funzione $c:\{1,\ldots, n\}\mapsto \{1,\ldots, k\}$).
Un tale __$k$-coloring__ è __valido__ se per ogni colore $j\in \{1,\ldots, k\}$, la sottosequenza di $T$ che ne ricomprende gli elementi di colore $j$ è strettamente decrescente.

    Può una sottosequenza non-decrescente di $T$ contenere due elementi dello stesso colore?

Se la tua risposta è un chiaro NO, allora fornirti un $k$-coloring è un modo per convincerti che nessuna sottosequenza non-decrescente di $T$ può avere lunghezza maggiore di $k$.

## Servizi offerti e competenze che potresti assicurarti di avere

Data in input una sequenza di naturali $T$, sapresti riconoscere se essa è strettamente crescente/decrescente? Sapresti riconoscere se essa è non-crescente/non-decrescente?
Sapresti ritornare un eventuale certificato di NO nella forma di due indici a elementi di $T$?

Data in input una sequenza di naturali $T$, sapresti ritornare una $k$-colorazione degli elementi di $T$ dove $k$ sia il più piccolo possibile?

Sapresti ritornare sia una $k$-colorazione ottima (col minimo numero di colori) che una sottosequenza strettamente crescente ottima (di massima lunghezza)?

