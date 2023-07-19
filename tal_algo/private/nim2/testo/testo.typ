#import "problem_template.typ": template, title, example_file, subtasks, subtasks_list
#show: template

#title("nim2", "Fino all'ultimo quadretto")

Flavonoidi e precursori di endorfine a parte, una tavola di cioccolato è una griglia di $m times n$ quadretti.
Considera due giocatori che si alternano nell'effettuare la seguente mossa:
    Spezza la tavoletta in due sotto-griglie, con taglio secco a ghigliottina (un taglio orizzontale, oppure verticale, ma comunque da parte a parte). Mangia una delle due tavolette più piccole così ottenute e riconsegna all'avversario l'altra (riconsegnerai quindi una tavola di $m' times n$ quadretti con $1 <= m' < m$, oppure di $m times n'$ quadretti con $1 <= n' < n$).
    
Chi si ritrova con una tavola $1 times 1$ non può più muovere, quindi perde mangiandosi l'ultimo quadretto come premio di consolazione: il suo avversario ha vinto!

Ogni istanza di questo problema comincia con la proposta di una partitina da parte del server (una coppia di numeri $m$ ed $n$). Accetta la proposta scegliendo se vuoi essere il primo o il secondo a muovere, e quindi gioca ogni tua mossa rispettando i turni, assicurandoti di non perdere la partita!

== Interazione

Il tuo programma interagirà col server leggendo dal proprio canale `stdin` e scrivendo sul proprio canale `stdout`.
La prima riga di `stdin` contiene $T$, il numero di partite che verrà giocato.
All'inizio di ogni partita, trovi sulla prossima riga di `stdin` una coppia di numeri $m$ ed $n$ separati da spazio; essi costituiscono la proposta di una posizione di gioco avanzata dal server.
A questo punto devi rispondere alla proposta dichiarando se preferisci giocare per primo (scrivere $1$ su `stdout`) oppure per secondo (scrivere $2$ su `stdout`). Dopo di chè inizia la partita vera e propria, che inizia con una mossa da parte del giocatore che tu hai stabilito muova per primo, e poi i giocatori si alternano a giocare finché la configurazione $(1,1)$ non viene consegnata da un giocatore (il vincente) all'altro (il perdente).
In generale, se la configurazione corrente è $(m, n)$, la mossa consiste nel consegnare all'avversario una configurazione $(m', n)$ con $1 <= m' < m$, oppure una configurazione $(m, n')$ con  $1 <= n' < n$. Per fare questo, il giocatore di turno scrive nella prossima riga del proprio `stdout`, separati da spazio, i due numeri che descrivono la configurazione prodotta dalla sua mossa e che egli intende consegnare all'avversario.

**Nota 1:** Potendo tu scegliere chi debba giocare per primo, potrai sempre vincere ogni partita, indipendentemente da quello che farà l'avversario.

**Nota 2:** Affinchè il server non possa tirare la partite per le lunghe per far scadere il time limit, il server si impegna a fare solo mosse in cui almeno una delle due coordinate venga almeno dimezzata in tutte le situazioni in cui questo non gli significa ragalare una partita altrimenti vinta.

**Nota 3:** Ogni tua comunicazione verso il server deve essere collocata su una riga diversa di `stdout` e ricordati di forzarne l'invio immediato al server effettuando un flush del tuo output! 


== Esempio

Le righe che iniziano con '<' sono quelle inviate dallo studente o da suo programma, quelle che iniziano con `>` sono quelle inviate dal server. Inoltre: di ciascuna riga è di mero commento quella parte che comincia col primo carattere di cancelletto '\#'.

#block[
  #set text(
    font: "New Computer Modern",
    size: 8pt
  )
  #example_file("example.int.txt") 
]

== Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.


+ *[12 istanze] tiny:* $m, n <= 6$
+ *[12 istanze] small:* $m, n <= 10$
+ *[12 istanze] medium:* $m, n <= 100$
+ *[12 istanze] skewed:* $m<= 3$, $n <= 1\,000\,000\,000$
+ *[12 istanze] big:* $m, n <= 1\,000\,000\,000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

#let example_size = "medium"

#align(center,
   raw("rtal -s wss://ta.di.univr.it/esame  connect -x <token> -a size=EXAMPLE_SIZE \nricerca_binaria  -- python my_solution.py".replace("EXAMPLE_SIZE", example_size), lang: "bash")
)

vengono valutati, nell'ordine, i subtask:

#h(0.6cm)#subtasks(top_size: example_size).

Il valore di default per l'argomento `size` è #raw(subtasks_list.at(-1)) che include tutti i testcase.


