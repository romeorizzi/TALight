#import "problem_template.typ": template, title, paired_files, example_file, display_subtasks_table, subtasks_usage
#show: template

#title

#text(style:"italic", size:11pt, [Questo problema è preso dalla fase nazionale delle Oii (Olimpiadi Italiane di Informatica, fase nazionale tenutasi in Fisciano, 18 – 20 settembre 2014).])

In aula alpha ci sono $N$ computer contrassegnati coi numeri naturali da $1$ ad $N$. Al momento solo alcuni di essi sono accesi, e Romeo e Andrea devono accenderli tutti prima dell’inizio della prima lezione (che è già un laboratorio)!
La nuova centralina offre $N$ pulsanti, anch’essi numerati da $1$ a $N$.
Il pulsante $i$ ha l'effetto di cambiare lo stato di tutti i computer il cui numero identificativo sia un divisore di $i$. Ad esempio, il pulsante $12$ cambia lo stato dei computer $1$, $2$, $3$, $4$, $6$, e $12$.
I pulsanti vanno premuti in ordine strettamente crescente (non si può premere il pulsante $i$ dopo aver premuto il pulsante $j$ , se $i <= j$).
Pertanto, nessun pulsante può essere premuto più di una volta.
Inizialmente tutti i pulsanti sono in posizione di OFF.
Un computer può venire acceso e/o spento anche varie volte; l’importante è che alla fine tutti i computer risultino accesi. Sapendo quali sono i computer inizialmente accesi, dovete stabilire se accenderli tutti sia possibile e, del caso, decidere quali pulsanti premere per ottenere tale obiettivo.
Ad esempio, se i computer sono $N = 6$ ci saranno $N = 6$ pulsanti, che cambiano lo stato dei computer secondo la tabella seguente.

#align(center, grid(
  columns: 3,
  gutter: 30pt,
  table(
   columns: (auto, auto),
   inset: 10pt,
   align: horizon,
    [*Pulsante*], [*Agisce su*],
     [1], [Computer 1],
     [2], [Computer 1 e 2]
  ),
  table(
   columns: (auto, auto),
   inset: 10pt,
   align: horizon,
    [*Pulsante*], [*Agisce su*],
     [3], [Computer 1 e 3],
     [4], [Computer 1,2 e 4]
  ),
  table(
   columns: (auto, auto),
   inset: 10pt,
   align: horizon,
    [*Pulsante*], [*Agisce su*],
     [5], [Computer 1 e 5],
     [6], [Computer 1,2,3 e 6]
  ),
))

Assumendo che lo stato acceso/spento (1/0) dei computer sia inizialmente quello codificato dalla riga
```
   0 1 0 1 0 0
```
ossia che la configurazione iniziale dei computer e dei pulsanti sia la seguente:

#figure(
  image("figs/conf_iniziale.png", width: 60%),
  caption: [
    Configurazione iniziale dei computer e dei pulsanti.
  ],
)

allora potremmo portarci allo stato in cui tutti i computer sono accesi pigiando prima il Pulsante 2, poi il Pulsante 5, e infine il Pulsante 6. Con queste azioni attraverseremo le seguenti configurazioni.

#figure(
  image("figs/mosse.png", width: 80%),
  caption: [
    Configurazioni attraversate per accendere tutti i computer del laboratorio alpha.
  ],
)




== Input

Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema, dove ogni istanza presenta un diverso stato iniziale per i computer dell'aula alpha. Ogni istanza è descritta in due righe, dove la prima riga contiene il numero $N$ di computer presenti quel giorno, e la seconda riga specifica quali computer siano inizialmente accesi (1) oppure spenti (0). Le $N$ cifre contenute in questa seconda ed ultima riga sono separate da spazi.

== Output

Per ciascuna istanza, prima di leggere l'istanza successiva, scrivi su `stdout` il tuo output così strutturato:

- la prima riga contiene il numero di diverse configurazioni sui pulsanti con le quali tutti gli $N$ computer siano accesi, e raggiungibili pigiando i pulsanti in ordine strettamente crescente.

- la riga seguente codifica una configurazione dei pulsanti, ossia contiene $N$ numeri interi nell'intervallo $[0, 1]$ separati da spazio con l'$i$-esimo di questi numeri a specificare se Pulsante $i$ è pigiato (1) nella soluzione oppure no $0$. Se nella riga precedente si è stampato uno $0$, si stampino $N$ zeri separati da spazio. Altrimenti si stampi la codifica per una configurazione dei pulsanti con la quale tutti gli $N$ computer siano accesi quando raggiunta pigiando i pulsanti in ordine strettamente crescente. 

Nella descrizione dei subtask è specificato quanti punti si acquisiscono su ciascuna istanza di quel subtask, vuoi per la correttezza del valore riportato nella prima riga, vuoi per la correttezza della configurazione finale dei pulsanti.

== Esempio di Input/Output
#paired_files("example.in.txt","example.out.txt","Input da `stdin`","Output su `stdout`", left_margin:1cm, interspace:2cm)

*Spiegazione:* la prima istanza è l'esempio utilizzato già sopra nel testo. Nella seconda istanza tutti i computer sono inizialmente spenti ed è possibile verificare che l'unica configurazione dei pulsanti con cui tutti i computer sono accesi è quella in cui il Pulsante 3 è l'unico a non essere pressato (posizione di OFF). Nella terza istanza tutti i computer sono inizialmente accesi e non serve fare nulla.

#pagebreak()
== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

#display_subtasks_table

#subtasks_usage

