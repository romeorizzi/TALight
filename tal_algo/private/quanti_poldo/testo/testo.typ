#import "problem_template.typ": template, title, example_file, subtasks, subtasks_list
#show: template

#title("quanti_poldo", "Count, rank e unrank di ombre crescenti")

Per ogni numero naturale $n in NN$ sia $NN_n := {n' in NN : n' < n}$.
Una sequenza $S = s_0, s_1, ..., s_(n-1)$ è detta _(monotona) crescente_ se $s_(i+1) > s_(i)$ per ogni $i in NN_(n-1)$.
Per ogni $k in NN_n$, ogni sequenza crescente $I:NN_(k) --> NN_(n)$
definisce una diversa sottosequenza di $S$ di lunghezza $k$;
più precisamente, la sequenza di $k$ indici $I = i_0, i_1, ..., i_(k-1)$ con $0 <= i_0 < i_1 < ... < i_(k-1) < n$ definisce la sequenza $S circle.small I := s_(i_0), s_(i_1), ..., s_(i_(k-1))$ come una sottosequenza di $S$ di lunghezza $k$.
Se $S circle.small I$ è una sottosequenza crescente di $S$ allora $I$ è detta un _ombra crescente per $S$_, o, più brevemente, un _ombra di $S$_.
Indichiamo con $II_(S)$ l'insieme di tutte le ombre crescenti per $S$. Su $II_(S)$ vige un'ordinamento totale che esemplifichiamo per $n=3$ assumendo una $S$ crescente qualsiasi:

```
sequenza    rango
0 1 2       0
0 1         1
0 2         2
0           3
1 2         4
1           5
2           6
            7
```

Se ti restano dubbi su come le ombre crescenti per $S$ siano ordinate per altre sequenze $S$ puoi interrogare il servizio `list` offerto per questo problema `TALight` fornendo una tua sequenza $S$ in input.

Ti chiediamo di produrre del codice che implementi le seguenti competenze:

/ counting: data $S$, calcolare il numero $f(S)$ di ombre di $S$.
/ ranking: date $S$ e $I in II_(S)$, restituire il rango $r$ di $I$ in $II_(S)$, ossia l'intero nell'intervallo $[0,f(S)-1]$ che specifica la posizione di $I$ nel nostro ordinamento, partendo da $0$.
/ unranking: dati $S$ e $r$, con $r in [0,f(S)-1]$, restituire la sequenza $I$ in $II_(S)$ che, partendo da $0$, appare in posizione $r$ entro il nostro ordinamento su $II_(S)$.

*Nota:* `rank(unrank(S, r)) = r`.

== Assunzioni

+ quando ti chiediamo di computare $f(S)$, in realtà, se vorrai, potrai limitarti a restituire il resto della divisione di $f(S)$ per $1.000.000.007$. Con questo obiettivo puoi acquisire maggiore efficienza che ti è necessaria per risolvere le istanze più grandi.

+ quando ti chiediamo di fare `rank`, è nostra cura fornirti in input una $I in II_(S)$ di rango inferiore a $1.000.000.007$.

+ quando ti chiediamo di fare `unrank`, è nostra cura fornirti in input un $r < 1.000.000.007$.

*NB: per rank e unrank, anche se il rango coinvolto è inferiore $1.000.000.007$, $f(S)$ potrebbe essere maggiore, quindi se utilizzi il modulo potresti doverti ricordare quantomeno se il vero valore di $f(S)$ è maggiore di $1.000.000.007$, per effettuare correttamente i confronti necessari.*

#pagebreak()


== Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema, dove ogni istanza può porre diverse domande per uno stesso valore di $n$.
Per ogni istanza, la prima riga contiene quattro numeri interi separati da uno spazio: $n$, $c$, $r$ ed $u$, dove $c=0,1$ indica se si richiede il valore di $f(S)$, $r$ è il numero di richieste di ranking e $u$ è il numero di richieste di unranking. La seconda riga contiene gli $n$ numeri interi costituenti $S$, nell'ordine $s_0,s_1,...,s_(n-1)$ e separati da spazio.
Seguono $r$ righe, l'$i$-esima delle quali contiene una sequenza $I_i$ di $II_(S)$.
Infine una riga che contiene $u$ numeri interi $r_1,r_2,...,r_u in [0,f(S)-1]$ separati da spazio. (Questa riga sarà vuota del caso $u$ sia $0$.)

== Output
Per ciascuna istanza, prima di leggere l'istanza successiva, scrivi su `stdout` il tuo output così strutturato:

 + la prima riga contiene il numero $f(S)$. Per le istanze con $c=0$, essa viene di fatto ignorata dal correttore, ma devi comunque stampare una riga (puoi ad esempio stampare la riga vuota, oppure stampare comunque il numero corretto di formule). Quando invece $c=1$ teniamo buona come risposta sia $f(S)$ che $f(S) % 1.000.000.007$ ma col primo potresti non riuscire a risolvere le istanze più grandi.

 + la seconda riga contiene $r$ numeri nell'intervallo $[0,f(S)-1]$ separati da spazio, l'$i$-esimo di questi numeri vuole essere il rango di $I_i$, ossia dell'$i$-esima sequenza di $II_(S)$ ricevuta in input per questa istanza. (Di nuovo, il contenuto di questa riga verrà ignorato per ogni istanza con $r=0$.)

 + seguono $u >= 0$ righe l'$i$-esima delle quali contiene l'ombra di $S$ di rango $r_i$, dove $r_i$ è l'$i$-esimo numero contenuto nell'ultima riga ricevuta in input per questa istanza.

== Esempio

=== Input
#example_file("example.in.txt")

=== Output
#example_file("example.out.txt")

== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

+ *[ 3 istanze] `esempi_testo`:* i due esempi del testo

+ *[ 9 istanze] `small_c`:* $n <= 10$, $c=1$, $r=0$, $u=0$

+ *[11 istanze] `small_r`:* $n <= 10$, $c=0$, $u=0$, $r <= 20$

+ *[11 istanze] `small_u`:* $n <= 10$, $c=0$, $r=0$, $u <= 20$

+ *[11 istanze] `medium_c`:* $n <= 20$, $c=1$, $r=0$, $u=0$

+ *[11 istanze] `medium_r`:* $n <= 20$, $c=0$, $u=0$, $r <= 50$

+ *[11 istanze] `medium_u`:* $n <= 20$, $c=0$, $r=0$, $u <= 50$

+ *[11 istanze] `big_c`:* $n <= 200$, $c=1$, $r=0$, $u=0$

+ *[11 istanze] `big_r`:* $n <= 200$, $c=0$, $u=0$, $r <= 200$

+ *[11 istanze] `big_u`:* $n <= 200$, $c=0$, $r=0$, $u <= 500$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

#let example_size = "medium_c"

#align(center,
   raw("rtal -s wss://ta.di.univr.it/esame  connect -x <token> -a size=EXAMPLE_SIZE \nmutually_unreachable  -- python my_solution.py".replace("EXAMPLE_SIZE", example_size), lang: "bash")
)
vengono valutati, nell'ordine, i subtask:

#h(0.6cm)#subtasks(top_size: example_size).

Il valore di default per l'argomento `size` è #raw(subtasks_list.at(-1)) che include tutti i testcase.


=== Servizi TALight a tua disposizione

Se reputi ti serva disambiguare meglio l'ordine da noi stabilito su $II_(S)$, puoi chiedere a TALight, ad esempio:

```
    rtal -s wss://ta.di.univr.it/esame  connect -x <token> quanti_poldo list  -a S="4 2 15 3 7"
```

Ulteriori servizi di supporto alla tua esplorazione del problema (esempi di chiamate):

```
    rtal -s wss://ta.di.univr.it/esame  connect -x <token> quanti_poldo check_count  -a S="4 2 15 3 7" -a risp=5
```

```
    rtal -s wss://ta.di.univr.it/esame  connect -x <token> quanti_poldo check_rank  -a S="4 2 15 3 7" -a input_shadow="1 3" -a right_rank=8
```

```
    rtal -s wss://ta.di.univr.it/esame  connect -x <token> quanti_poldo check_unrank -a input_rank=3  -a S="4 2 15 3 7" -a input_rank=2 -a right_shadow="2 4 5"
```

*Nota:* questi ulteriori servizi ti risponderanno con un certo ritardo per non avere un effetto controproducente sul piano della tua esplorazione autonoma del problema.
