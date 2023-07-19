#import "problem_template.typ": template, title, example_file, subtasks, subtasks_list
#show: template

#title("FBF_trasparenti", "Count, rank e unrank delle formule di parentesi ben formate trasparenti")

Ricordiamo che una formula di parentesi ben formata (FBF) è una stringa sull'alfabeto $Sigma = {$#h(2pt)*(*$#h(1pt),#h(3pt)$*)*$#h(2pt)}$ che può essere generata partendo dal simbolo non-terminale *S* tramite applicazione non-deterministica delle seguenti regole di sostituzione:

+ *S $-->$ (S)*

+ *S $-->$ SS*

+ *S $--> epsilon$*

dove *$epsilon$* indica la stringa vuota, e la terza regola è quindi necessaria per sbarazzarsi del simbolo non-terminale *S*.
Ad esempio, le formule *()()* e *(())* vengono entrambe ottenute dalla stringa iniziale *S* con una singola applicazione della regola 2, seguita da due applicazioni sia della 1 che della 3.

Una FBF è detta _trasparente_ se ammette una derivazione in cui la regola 2 non viene mai applicata ad un simbolo *S* che è stato introdotto a sua volta con la regola 2 ($-->$ essere trasparenti è una *NP*-property).

Equivalentemente, una FBF è detta _trasparente_ se *non* contiene una sottostringa che ricada nel template *(*$A$*)(*$B$*)(*$C$*)* dove $A$, $B$ e $C$ sono FBF ($-->$ essere trasparenti è una *coNP*-property).

La più piccola FBF non trasparente è appunto:

*()()()*

ed ogni FBF non trasparente in un certo qual senso la contiene.

Prese insieme, queste due definizioni equivalenti vorrebbero caratterizzare il concetto, ossia offrirti un'idea abbastanza chiara di cosa sia una FBF trasparente. Ma in realtà, ai nostri scopi, dovrebbe in tutto bastarti una comprensione anche solo intuitiva, che puoi ad esempio raccogliere guardando al seguente listing delle FBF trasparenti per $n=4$. Poichè siamo interessati nel gestire le FBF trasparenti adottando un preciso criterio di ordinamento lessicografico sull'applicazione delle regole di generazione, cerca di estrapolare dall'esempio il criterio di ordinamento quì adottato (l'esempio dovrebbe bastarti, e anzi ti conviene assicurarti di spremerlo, ma in caso contrario puoi sempre avvalerti dei servizi TALight messi a disposizione col problema):

```
   (((())))
   ((()()))
   ((())())
   (()(()))
   ((()))()
   (()())()
   (())(())
   ()((()))
   ()(()())
```
Ti chiediamo di produrre del codice che implementi le seguenti competenze:

/ counting: dato $n$, calcolare il numero $f(n)$ delle FBF trasparenti con $n$ coppie di parentesi.
/ ranking: data una FBF trasparente $t$, restituire il suo rango $r$, ossia il numero intero nell'intervallo $[0,f(n)-1]$ che specifica la posizione di $t$ entro il nostro ordinamento, partendo da $0$.
/ unranking: dati $n$ ed $r$, con $r in [0,f(n)-1]$, restituire la FBF trasparente che, partendo da $0$, appare in posizione $r$ entro il nostro ordinamento delle FBF trasparenti con $n$ coppie di parentesi.

*Nota:* `rank(unrank(n, r)) = r`.

#pagebreak()

== Assunzioni

+ quando ti chiediamo di computare $f(n)$, in realtà, se vorrai, potrai limitarti a restituire il resto della divisione di $f(n)$ per $1.000.000.007$. Con questo obiettivo puoi acquisire maggiore efficienza che ti è necessaria per risolvere le istanze più grandi.

+ quando ti chiediamo di fare `rank`, è nostra cura fornirti in input una FBF di rango inferiore a $1.000.000.007$.

+ quando ti chiediamo di fare `unrank`, è nostra cura fornirti in input un $r < 1.000.000.007$.

*NB: per rank e unrank, anche se il rango coinvolto è inferiore $1.000.000.007$, $f(n)$ potrebbe essere maggiore, quindi se utilizzi il modulo potresti doverti ricordare quantomeno se il vero valore di $f(n)$ è maggiore di $1.000.000.007$, per effettuare correttamente i confronti necessari.*



== Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema, dove ogni istanza può porre diverse domande per uno stesso valore di $n$.
Per ogni istanza, la prima riga contiene quattro numeri interi separati da uno spazio: $n$, $c$, $r$ ed $u$, dove $c=0,1$ indica se si richiede il valore di $f(n)$, $r$ è il numero di richieste di ranking e $u$ è il numero di richieste di unranking.
Seguono $r$ righe, l'$i$-esima delle quali contiene una FBF trasparente $t_i$ che ha $n$ coppie di parentesi.
Infine una riga che contiene $u$ numeri interi $r_1,r_2,...,r_u in [0,f(n)-1]$ separati da spazio. (Questa riga sarà vuota del caso $u$ sia $0$.)

== Output
Per ciascuna istanza, prima di leggere l'istanza successiva, scrivi su `stdout` il tuo output così strutturato:

 + la prima riga contiene il numero $f(n)$. Per le istanze con $c=0$, essa viene di fatto ignorata dal correttore, ma devi comunque stampare una riga (puoi ad esempio stampare la riga vuota, oppure stampare comunque il numero corretto di formule). Quando invece $c=1$ teniamo buona come risposta sia $f(n)$ che $f(n) % 1.000.000.007$ ma col primo potresti non riuscire a risolvere le istanze più grandi.

 + la seconda riga contiene $r$ numeri nell'intervallo $[0,f(n)-1]$ separati da spazio, l'$i$-esimo di questi numeri vuole essere il rango di $t_i$, ossia dell'$i$-esima FBF trasparente ricevuta in input per questa istanza. (Di nuovo, il contenuto di questa riga verrà ignorato per le istanza con $r=0$.)

 + seguono $u >= 0$ righe l'$i$-esima delle quali contiene l'FBF trasparente di $n$ coppie di parentesi di rango $r_i$, dove $r_i$ è l'$i$-esimo numero contenuto nell'ultima riga ricevuta in input per questa istanza.

== Esempio

=== Input
#example_file("example.in.txt")

=== Output
#example_file("example.out.txt")

== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

+ **[ 3 istanze] `esempi_testo`:** i due esempi del testo

+ **[ 9 istanze] `small_c`:** $n <= 10$, $c=1$, $r=0$, $u=0$

+ **[11 istanze] `small_r`:** $n <= 10$, $c=0$, $u=0$, $r <= 20$

+ **[11 istanze] `small_u`:** $n <= 10$, $c=0$, $r=0$, $u <= 20$

+ **[11 istanze] `medium_c`:** $n <= 20$, $c=1$, $r=0$, $u=0$

+ **[11 istanze] `medium_r`:** $n <= 20$, $c=0$, $u=0$, $r <= 50$

+ **[11 istanze] `medium_u`:** $n <= 20$, $c=0$, $r=0$, $u <= 50$

+ **[11 istanze] `big_c`:** $n <= 200$, $c=1$, $r=0$, $u=0$

+ **[11 istanze] `big_r`:** $n <= 200$, $c=0$, $u=0$, $r <= 200$

+ **[11 istanze] `big_u`:** $n <= 200$, $c=0$, $r=0$, $u <= 500$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

#let example_size = "medium_c"

#align(center,
   raw("rtal -s wss://ta.di.univr.it/esame  connect -x <token> -a size=EXAMPLE_SIZE \nmutually_unreachable  -- python my_solution.py".replace("EXAMPLE_SIZE", example_size), lang: "bash")
)
vengono valutati, nell'ordine, i subtask:

#h(0.6cm)#subtasks(top_size: example_size).

Il valore di default per l'argomento `size` è #raw(subtasks_list.at(-1)) che include tutti i testcase.



=== Servizi TALight a tua disposizione

Se reputi ti serva chiarire la nozione di trasparenza, puoi chiedere a TALight se una certa FBF sia trasparente, ad esempio:

```
    rtal -s wss://ta.di.univr.it/esame  connect FBF_trasparenti is_transparentFBF -a FBF="(()(()())())"
```

Il servizio non solo ti risponderà con un valore di verità, ma cercherà anche di certificarlo ai tuoi occhi.

Ulteriori servizi di supporto alla tua esplorazione del problema (esempi di chiamate):

```
    rtal -s wss://ta.di.univr.it/esame  connect FBF_trasparenti check_num_transparentFBFs -a n_pairs=4 -a risp=9
```

```
    rtal -s wss://ta.di.univr.it/esame  connect FBF_trasparenti check_rank -a input_FBF="(()(()))"  -a right_rank=3
```

```
    rtal -s wss://ta.di.univr.it/esame  connect FBF_trasparenti check_unrank -a input_rank=3  -a right_FBF="(()(()))"
```

*Nota:* questi ulteriori servizi ti risponderanno con un certo ritardo per non avere un effetto controproducente sul piano della tua esplorazione autonoma del problema.
