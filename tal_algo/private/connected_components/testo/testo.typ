#import "problem_template.typ": template, title, example_file, subtasks, subtasks_list
#show: template

#title("connected_components", "Le componenti connesse di un grafo non orientato")

Un grafo $G=(V,E)$ è detto _connesso_ se per ogni due nodi $u,v\in V$ ammette un cammino tra $u$ e $v$.
Un grafo $G'=(V',E')$ è un _sottografo_ di $G$ se $V'$ è un sottoinsieme di $V$ e $E'$ è un sottoinsieme di $E$.
Dato un qualsiasi sottoinsieme $S$ di $V$, indichiamo con $G[S]$ il _sottografo di $G$ indotto da $S$_, ossia il sottografo $G'=(S,E')$ di $G$ dove $E'$ contiene tutti gli archi di $G$ con entrambi gli estremi in $S$.
Le _componenti connesse di $G$_ sono gli insiemi massimali nella famiglia di quei sottoinsiemi $S$ di $V$ per cui $G[S]$ è connesso.

Dato un grafo $G=(V,E)$, lista le sue componenti connesse.

== Input

Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema, dove ogni istanza è un diverso grafo $G=(V,E)$. Per ogni istanza, la prima riga contiene due numeri interi separati da uno spazio:
il numero di nodi $n=|V|$, e il numero di archi $m=|E|$.
Seguono $m$ righe ciascuna delle quali riporta un diverso arco di $G$. Ciascun arco viene specificato fornendo i nomi dei due nodi che collega (due numeri interi nell'intervallo $[0, n-1]$, separati da uno spazio).

== Output

Per ciascuna istanza, prima di leggere l'istanza successiva, scrivi su `stdout` il tuo output così strutturato:

- la prima riga contiene un numero intero $c$, il numero di componenti connesse di $G$.

- ciascuna della seguenti $c$ righe contiene una diversa componente connessa $C$ di $G$, ossia $|C|$ numeri interi separati da spazio. Tali interi, tutti contenuti nell'intervallo $[0, n-1]$, sono i nomi dei nodi contenuti in $C$.

== Esempio

=== Input
#example_file("example.in.txt")

=== Output
#example_file("example.out.txt")


*Spiegazione:* il primo grafo è connesso e quindi abbiamo un unica componente connessa che contiene tutti i nodi. I nodi del secondo grafo sono partizionati in due componenti connesse, una di $4$ nodi e l'altra coi rimanenti $3$ nodi.

== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

- *[2 istanze] esempi_testo:* i due esempi del testo
- *[12 istanze] small:* $N <= 10$, $M <= 20$
- *[18 istanze] medium:* $N <= 100$, $M <= 500$
- *[18 istanze] big:* $N <= 5\,000$, $M <= 20\,000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

#let example_size = "medium"

#align(center,
   raw("rtal -s wss://ta.di.univr.it/esame  connect -x <token> -a size=EXAMPLE_SIZE \nmutually_unreachable  -- python my_solution.py".replace("EXAMPLE_SIZE", example_size), lang: "bash")
)
vengono valutati, nell'ordine, i subtask:

#h(0.6cm)#subtasks(top_size: example_size).

Il valore di default per l'argomento `size` è #raw(subtasks_list.at(-1)) che include tutti i testcase.
