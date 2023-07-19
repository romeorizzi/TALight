#import "problem_template.typ": template, title, example_file, subtasks, subtasks_list
#show: template

#title("mutually_unreachable", "Insiemi massimali di nodi mutualmente incomunicanti")

In un grafo _non-orientato_ $G=(V,E)$ vi è un cammino $p$ che porta da un nodo $u$ a un nodo $v$ se e solo se vi è un cammino da $v$ ad $u$ (basta percorrere $p$ a ritroso). Quando esiste, un tale cammino _connette_ i nodi $u$ e $v$. Su $V$, la relazione binaria _essere connessi_ è una relazione di equivalenza (riflessiva, simmetrica e transitiva).
Dato un grafo non-orientato $G=(V,E)$, il tuo obiettivo è individuare un sottoinsieme $S$ di $V$ tale che nessun cammino in $G$ connetta due diversi nodi in $S$.

== Input

Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema, dove ogni istanza è un diverso grafo $G=(V,E)$. Per ogni istanza, la prima riga contiene due numeri interi separati da uno spazio:
il numero di nodi $n=|V|$, e il numero di archi $m=|E|$.
Seguono $m$ righe ciascuna delle quali riporta un diverso arco di $G$. Ciascun arco viene specificato fornendo i nomi dei due nodi che collega (due numeri interi nell'intervallo $[0, n-1]$, separati da uno spazio).

== Output

Per ciascuna istanza, prima di leggere l'istanza successiva, scrivi su `stdout` il tuo output così strutturato:

- la prima riga contiene un numero intero $s$, la massima cardinalità di un insieme di nodi di $G$ tale che nessun cammino in $G$ connetta due diversi nodi in $S$.

- la riga seguente contiene $s$ numeri interi separati da spazio. Tali interi, tutti contenuti nell'intervallo $[0, n-1]$, sono i nomi dei nodi contenuti in $S$.

== Esempio

=== Input
#example_file("example.in.txt")

=== Output
#example_file("example.out.txt")

*Spiegazione:* il primo grafo è connesso e quindi non è possibile includere in $S$ più di un singolo nodo (gli insiemi $S$ ottimi sono quanti i nodi, si sarebbe potuto ritornare un qualsiasi altro nodo in $V$ al posto del nodo di nome $3$). Nel caso del secondo grafo è facile verificare che tra i nodi $0$ e $5$ non è presente alcun cammino. Al tempo stesso, comunque si scelgano tre nodi almeno due di essi saranno connessi da un qualche cammino. Era pertanto corretto rispondere con una qualsiasi delle $3 times 4 = 12$ coppie di nodi incomunicanti.

== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

+ *[2 istanze] `esempi_testo`:* i due esempi del testo

+ *[12 istanze] `small`:* $N \leq 10$, $M \leq 20$

+ *[18 istanze] `medium`:* $N \leq 100$, $M \leq 500$

+ *[18 istanze] `big`:* $N \leq 5\,000$, $M \leq 20\,000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

#let example_size = "medium"

#align(center,
   raw("rtal -s <URL>  connect -x <token> -a size=EXAMPLE_SIZE \nmutually_unreachable  -- python my_solution.py".replace("EXAMPLE_SIZE", example_size), lang: "bash")
)
vengono valutati, nell'ordine, i subtask:

#h(0.6cm)#subtasks(top_size: example_size).

Il valore di default per l'argomento `size` è #raw(subtasks_list.at(-1)) che include tutti i testcase.


____________________________________________________________
server esame <URL>: wss://ta.di.univr.it/esame
server esercitazioni e simula-prove <URL>: wss://ta.di.univr.it/algo

cosa vogliamo che faccia il Makefile:
aggiorna il file .../testo/testo.pdf a .../testo/*.txt testo.typ, manager.py

ragionevole l'idea di creare un file yaml che definisca i subtask in un posto unico poi usato da manager e da testo

io aggiungo nei file meta una camera per ogni subtask che consenta di mettere un tetto sul numero di istanze
- aggiornare tc.rs e tc.py per implementare il tetto 
- modificare rtal per dargli un flag che scriva i due file o il file impiallaciatto con (<, >)


da ragionare anche con Dario:
  come eventualmente organizzare una verifica automatica su un testbed di soluzioni

