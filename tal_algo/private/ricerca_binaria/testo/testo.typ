#import "problem_template.typ": template, title, example_file, subtasks, subtasks_list
#show: template

#title("ricerca_binaria", "Ricerca binaria tra bugiardi incalliti")

In principio era il logos, e ti vennero comunicati due numeri interi positivi $n$ e $k$.
Miliardi di anni dopo, rinchiuso in un qualche laboratorio, credi che nell'intervallo chiuso $[1,n]$ sia ricompreso un misterioso numero intero $x$ che devi assolutamente individuare.
Puoi porre domande del tipo "l'è miga $y$?" con $y$ un intero in $[1,n]$. Sai che alla tua $i$-esima domanda risponderà lo strumento $i % k$, ossia lo strumento che ha per nome il resto della divisione di $i$ per $k$. In altre parole, le domande vengono smistate in round robin sui $k$ strumenti. 
Le risposte constano di un singolo carattere nell'alfabeto ${<,>,=}$. Otterrai '$=$' se e solo se $y=x$.
Altrimenti, dipende ...
Se davvero vuoi risolvere tutti i subtask allora devi sapere che, in alcuni di essi, alcuni strumenti dicono ancora sempre il vero, ma altri sono _bugiardi incalliti_ e rispondono _consistentemente_ '$<$' *quando invece* $x>y$ e '$>$' *quando invece* $x<y$.

In ogni caso, vedi di non sprecare domande (riferisciti al criterio del caso peggiore).


== Protocollo di comunicazione

Il tuo programma interagirà col server leggendo dal proprio canale `stdin` e scrivendo sul proprio canale `stdout`.
La prima riga di `stdin` contiene $T$, il numero di testcase da affrontare.
All'inizio di ciascun testcase, trovi sulla prossima riga di `stdin` i tre numeri $n$, $k$ e $b$ separati da spazio. Il valore $b=0$ indica che tutti gli strumenti dicono il vero, mentre $b=1$ significa che ciascuno di loro (presi indipendentemente) potrebbe o dire sempre il vero o essere un mentitore seriale (deve ammettere il vero solo quando gli si chiede se $x=x$, come se lavorasse ad ordinamento invertito).
Inizia ora un loop che durerà fino a quando tu non sia sicuro di conoscere il numero misterioso $x$.
Non appena conoscerai con certezza l'identità di $x$ puoi chiudere il testcase in corso scrivendo su `stdout` una stringa che inizi per "!" seguito dal numero $x$. Altrimenti puoi sottoporre la tua prossima domanda per il testcase corrente scrivendo su `stdout` una stringa che inizi per "?" seguito da un numero ricompreso nell'intervallo chiuso $[1,n]$. In questo secondo caso dovrai raccogliere da `stdin` la risposta del server:
una riga di un singolo carattere nell'alfabeto ${<,>,=}$.

**Nota 1:** Ogni tua comunicazione verso il server deve essere collocata su una riga diversa di `stdout` e ricordati di forzarne l'invio immediato al server effettuando un flush del tuo output!

**Nota 2:** Il dialogo diretto col server, non mediato da un tuo programma, può aiutarti ad acquisire il corretto protocollo di comunicazione tra il server e il tuo programma, incluso l'eventuale feedback che viene rilasciato sul file di oucome generato alla fine dell'interazione (se la porti a completamento o la chiudi con Ctrl-D). Verrai anche a meglio conoscere come gioca il server, il quale adotta una strategia adattiva per metterti alla prova secondo il criterio del caso peggiore. Per promuovere il dialogo diretto offriamo un servizio aggiuntivo che puoi chiamare con:

```
    rtal -s <URL>  connect -x <token> ricerca_binaria umano -a t=1 -a n=10 <inserisci_qua_altri_argomenti>
```

Non solo ti darà agio di dialogare nei tuoi tempi ma il suo comportamento può essere meglio parametrizzato attraverso i parametri aggiuntivi opzionali:
```
  -a t=1      per settare ad 1 (o altri valori) il numero di testcase
  -a n=1      per settare ad 1 (o altri valori) l'estremo destro n
  -a k=1      per settare ad 1 (o altri valori) il numero di strumenti k
  -a extra=1  per settare ad 1 (o altri valori) l'eccesso di domande concesso
  -a bugiardi=b  con b=0: nessun bugiardo; b=1: tutti bugiardi; b=2: sceglie il server con strategia adattiva
```

#pagebreak()


== Esempio

Le righe che iniziano con '?' o '!' sono quelle inviate dallo studente o da suo programma, le altre sono quelle inviate dal server. Inoltre: di ciascuna riga è di mero commento quella parte che comincia col primo carattere di cancelletto '\#'.

#example_file("example.int.txt") 

== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

+ **[ 5 istanze] `small0`:** $n <= 15$, nessun strumento è bugiardo, ti è concessa una query extra
+ **[10 istanze] `small1`:** $n <= 15$, nessun strumento è bugiardo, non puoi regalare
+ **[ 5 istanze] `small2`:** $n <= 15$, $k=1$, non puoi regalare
+ **[10 istanze] `small3`:** $n <= 15$, nessuna assunzione, non puoi regalare

+ **[ 5 istanze] `medium0`:** $n <= 100$, nessun strumento è bugiardo
+ **[10 istanze] `medium1`:** $n <= 100$, nessun strumento è bugiardo, non puoi regalare
+ **[ 5 istanze] `medium2`:** $n <= 100$, $k=1$, non puoi regalare
+ **[10 istanze] `medium3`:** $n <= 100$, nessuna assunzione, non puoi regalare

+ **[ 6 istanze] `big0`:** $n <= 10^9$, nessun strumento è bugiardo
+ **[ 6 istanze] `big1`:** $n <= 10^9$, nessun strumento è bugiardo, non puoi regalare
+ **[ 6 istanze] `big2`:** $n <= 10^9$, $k=1$, non puoi regalare
+ **[ 6 istanze] `big3`:** $n <= 10^9$, nessuna assunzione, non puoi regalare


In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando
#footnote[`<URL>` server esame: `wss://ta.di.univr.it/esame`]#super[,]#h(2pt) <fn_server_esame>
#footnote[`<URL>` server esercitazioni e simula-prove: `wss://ta.di.univr.it/algo`] <fn_server_simula>:

#let example_size = "medium0"

#align(center,
   raw("rtal -s <URL>  connect -x <token> -a size=EXAMPLE_SIZE \nricerca_binaria  -- python my_solution.py".replace("EXAMPLE_SIZE", example_size), lang: "bash")
)

vengono valutati, nell'ordine, i subtask:

#h(0.6cm)#subtasks(top_size: example_size).

Il valore di default per l'argomento `size` è #raw(subtasks_list.at(-1)) che include tutti i testcase.




