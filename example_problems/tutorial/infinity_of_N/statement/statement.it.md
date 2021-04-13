# infinity_of_N (un'infinità di numeri naturali)

Gli algoritmi offrono dimostrazioni e alle dimostrazioni, il più delle volte, perveniamo tramite algoritmi.

## Task 1: Dimostare che esiste un'infinità di numeri naturali.

Se possiedi questa competenza:

    ogniqualvolta ti viene dato un numero naturale sai come restituirne uno più grande 

allora sei già ben convinto di due cose:

    Fatto: non esiste una cosa come il numero naturale più grande;

    Corollario: vi è una moltitudine infinita di numeri naturali là fuori.

<details><summary>Il corollario è conseguenza dal fatto.</summary>

Assumiamo infatti che la nostra nozione di "maggiore" (in simbolo, la relazione di $>$) goda di queste due proprietà:

1. Non distinguiamo tra eguali: se $a > b$ allora i numeri naturali $a$ e $b$ sono distinti.

2. Transitività: se $a > b$ e $b > c$ allora $a > c$.
</details>

Per partire, ti invitiamo ad esibire la detta competenza in una gara allo sparare numeri sempre più grossi. Mettiti alla prova giocando tu stesso contro [il servizio `bigger_and_bigger`](#service-bigger_and_bigger) di questo problema didattico del TALight tutorial. E poi, quando avrai acquisito confidenza e preso le misure, potresti istruire un bot a giocare in tua vece. Nelle istruzioni sui servizi trovi i dettagli su come realizzare queste cose.  

<details>
<summary>Cosa dimostrerai col tuo costruire</summary>

Quando puoi effettivamente trasmettere una competenza che ha per conseguenze cose come il fatto ed il corollario visti sopra, allora le tue prescrizioni o insegnamenti costituiranno inevitabilmente dimostrazione di entrambi. Col tuo bot (un automatismo che sempre ributta indietro la palla) scritto in un qualche linguaggio standardizzato e ufficiale, la tua dimostrazione è formale e precisa al punto di essere eseguibile ed operativa. Sì, il bot potrebbe anche dare malfunzionamenti a causa di limitazioni reali del sistema su cui posto in esecuzione, ma questo non dovrebbe riguardarci qui. Ciò che conta sono le semplici idee archetipali che hai inserito dentro di esso, la loro validità trascende tali limiti. Se il tuo bot non manifesta problemi entro questi limiti (nessun computer ti potrà mettere a disposizione memoria o un numero di operazioni infiniti), puoi già essere fiducioso che esse costituiscono una dimostrazione corretta, e per di più algoritmica, che trova il suo posto eterno nell'iperuranio.
</details>


## Task 2: Dimostriamo ora il principio di Archimede: i razionali sono densi nei reali.

Ti è piaciuta la sfida precedente? Realizza allora un meccanismo automatico che, ogniqualvolta assegnato un numero reale _positivo_ $\varepsilon > 0$, ritorna un numero naturale _positivo_ $N_\varepsilon > 0$ tale che $\frac{1}{N_\varepsilon} < \varepsilon$.


<details><summary>What will you prove as a result of your making</summary>

With your bot you have proven a basic fact placed at the grounds of the mathematical analysis building:

    Fact: the rationals are dense into the reals.

What is meant with this dense sentence is:

*    however one fixes two different real numbers $a$ and $b$, say $a<b$, then there always exists a rational number $q$ that sits between the two and separates them, namely, $a<q<b$.

This fact is at the basis of [any construction or even definition that has been proposed for the field of the real numbers](https://en.wikipedia.org/wiki/Construction_of_the_real_numbers). Indeed, it occurs as one of the axioms in the synthetic approach.

**A consideration for to the instructor.** The term "construct" has a much stronger meaning to us. We reserve it only to finite representations of objects that can be computed in finite time. A [real number is computable](https://en.wikipedia.org/wiki/Computable_number#:~:text=A%20real%20number%20is%20computable%20if%20its%20digit%20sequence%20can,digits%20following%20the%20decimal%20point.) if its digits can be produced by some algorithm or Turing machine when given the position of the digit as input. As such, the computable reals are countably many and yet,  countably many of them are not constructible in our sense. We ask our problem solvers to build constructive proofs or constructive core features of what could be a proof. By this we mean providing the means for the construction of finite objects, while these means are meant to be applicable in general (on an infinite number of possible calls). Though the checking of these proofs might hardly be a finite task, we observe that most often we can actually content ourselves with checking the validity of the constructions only over rather limited instance spaces. A finite prefix of an infinite dialogue is more than enough for the apprentice to get all the feedback he needs as a check on the validity of his proof and on the comprehension he has got. Of course, the more we go higher in spaces and the more we expect the apprentice to be collaborative and work for the system rather than at breaking it. Since the spaces for non-sense are more widely infinite than those of meaning ("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe." - Albert Einstein), we ought to trust our problem solver to opt for the challenges of meaning. Besides, any didactic or educative effort has to cope with this limit: "If you are not willing to learn, no one can help you. If you are determined to learn, no one can stop you" (Zig Ziglar). Security would kill the cat, so we go for the opposite spectrum.  

You have really constructed your $N_\varepsilon$, at least for those $\varepsilon$ that possessed a finite representation. In fact, you probably came out with solutions that would truly hold for any real $\varepsilon$, even for a non constructible (and even a non computable) one.
Yes, you might be scared your method might not work with a real like $1-0.\overline{9}$.

Does it work here?

We bet not. But ... look, it is not your fault!

The point here is that $1-0.\overline{9} = 0$ since $0.\overline{9}$ equals $1$.

Indeed, assume $0.\overline{9}$ and $1$ where different, then there should be at least one real in the middle, namely $(1+0.\overline{9})/2$. Do you see any space left for this one real? Also, the difference $1-0.\overline{9}$ would be an infinitesially small number. But no single real can be neither infinitum nor infinitesimal.

Both of these arguments are also proofs, since ["once you eliminate the impossible, whatever remains, no matter how improbable, must be the truth"](https://en.wikiquote.org/wiki/Sherlock_Holmes) (Arthur Conan Doyle).

Yes, for puzzling as it might seem at first, you have just discovered that the decimal representations of a real number are not unique. "All truth passes through three stages. First, it is ridiculed. Second, it is violently opposed. Third, it is accepted as being self-evident" (Arthur Schopenhauer).
Now that you know this fact you can be reassured about the generality of your method (the one at the hearth of your bot, its very spirit, its underlying algorithm):

    Fact: every decimal representation of a real $\varepsilon$ which is not an integer has a non-zero digit after the '.'.

 The position of this digit is all what you need to take into account in order to obtain a $N_\varepsilon$ guaranteed to work fine. And this is what you did at the bare bones.
</details>

### Servizio bigger_and_bigger


Lancia

```t
> rtal connect infinity_of_N bigger_and_bigger
```

per giocare tu stesso al gioco di chi spara il numero più grande contro il nostro programma S che eroga il servizio.
Una sequenza di sorpassi inarrestabili in cui il server S dovrà gettare la spugna prima o poi (se non sbaglierai).
Il programma S potrà risiedere in local sulla tua macchina oppure nel cloud: quale dei due casi si applichi dipende da come hai istruito il daemon `rtald` al suo avvio. 


Per assicurarti di vincere sempre (cioè per ottenere una prova di qualcosa), puoi usare un tuo semplice bot da far giocare al tuo posto

```t
> rtal connect infinity_of_N bigger_and_bigger -- ./my_bot.py
```

Qui `my_bot.py` dovrebbe essere interpretato solo come a titolo esemplificativo di un nome di file con percorso completo di un eseguibile che si trova sulla tua macchina locale. Ciò coinvolgerà il tuo bot in una partita (potenzialmente) infinita contro S.

Il tuo bot è un binario eseguibile compatibile con la tua architettura, non importa come generato (compilatori, assemblers, ...), ma può essere anche una prescrizione od uno script in un linguaggio interpretato come python o un bytecode (purchè la tua macchina abbia installati l'interprete o la macchina virtuale). La compatibilità sulla tua macchina è una questione solo tua e per altro sotto il tuo pieno controllo.


### Service archimede

Anche per questo task offriamo un singolo servizio. Tuttavia, questa volta abbiamo scelto di dare a questo stesso servizio due nomi diversi:
usa `rationals_are_dense_into_reals` oppure `archimede`, a tuo piacimento, e combina le possibilità offerte dalla sintassi d'uso generale di `rtal` con la flessibilità del servizio introdotta coi parametri da esso previsti nello specifico.

<details>
<summary>Vuoi sapere di più riguardo all'uso generale del comando `rtal`?</summary>

Se vuoi conoscere meglio il comando `rtal` lancia
```t
> rtal --help
```
oppure
```t
> rtal connect --help
```
</details>

<details>
<summary>Vuoi sapere di più sui parametri e le possibilità previste da un servizio di uno specifico problema?</summary>

Se vuoi saperne di più sui parametri dei servizi di un problema lancia

```t
> rtal list infinity_of_N - v
```
</details>


## Esempi di interazioni

Negli esempi, le righe inviate dal server del servizio realizzato dal problem maker sono prefissate con "S> ", mentre quelle inviate dall'agente in locale (tù oppure il tuo bot) sono prefissate con "L> ".

<details>
<summary><strong>Task 1</strong></summary>

Se da riga di comando immetti

```bash
rtal connect -a num_rounds=10 -a lang=eninfinity_of_N bigger_and_bigger
```
Col daemon `rtald` correttamente attivato, allora il seguente dialogo potrebbe prender piede tra tè (L) ed il server (S):

```t
S> # Servirò: problem=infinity_of_N, service=bigger_and_bigger, num_rounds=10.
S> # Ciao! Giochiamo a chi dice il numero più grande.
S> # Parto io e poi andiamo a turno, sempre scrivendo un singolo numero e sempre crescndo. Lascerò a tè l'ultima parola.
S> 15
L> 20
S> 26
L> 30
S> 35
L> 50
! Rinuncio. Hai vinto!
```

Come vedi, le linee che iniziano in '#' vanno considerate commenti che possono essere ignorate dai due agenti impegnati nella conversazione. Il server chiude immediatamente la connessione non appena rileva una violazione del protocollo del servizio. Il server chiude inoltre il canale e rilascia il terminale non appena il dialogo giungesse alla sua naturale terminazione. Puoi facilmente distinguere in quale dei due modi S ha chiuso il canale: il server invia una linea che inizia con '!' quando chiude il canale per terminazione naturale. Il resto di quella linea può di nuovo offrire un commento arbitrario, come vedi nell'esempio sopra.

If you write a bot, it does not need to write out any comments (though you might find them fun or useful for debugging purposes) and only needs to skip and ignore those lines starting with '#'. This is good also because other services could be activated through these lines, which opens the possibility of an extensible ecosystem of services and tools. When playing yourself, the comment lines from the server might on the contrary be of some help in many ways.
Back to the specs for your bot: Input from `stdin` and output to `stdout`, each line just one single number. More precisely: the format of each line is a sequence of digits followed by newline; the very first digit in the sequence might be a zero only if it is also the last one, and the represented number is zero.

You can trow in your bot of yours to play in your behalf with

```t
> rtal connect -e infinity_of_N bigger_and_bigger -- ./my_bot.py
```

here `my_bot.py` is just the full name (aka filename with path) of an executable sitting on your local machine. Your bot should either be a binary executable code compatible with your architecture, however you obtained it (compilers, assemblers, ...), or a prescription or script in an interpreted language like python or a bytecode. This also works fine as long as your local machine has the corresponding interpreters or virtual machines installed. Compatibility on your side is your own issue. If the bot works correctly on your machine then it will be correctly connected by `rtal`. You can check/test/debug your both by running it as alone. In the case of our both, we could have issued
```t
> ./my_bot.py
```
and tested the bot in isolation conducting ourselves a dialogue with it through the terminal.
</details>

<details>
<summary><strong>Task 2</strong></summary>

La struttura generale del protocollo di questo servizio è la stessa che per il Task&nbsp;1. La sola differenza è che, come puoi vedere, il server S ora gioca rappresentazioni decimali di numeri reali. In esse, al più una singola occorrenza del carattere '.' può presentarsi, tutti gli altri caratteri devono essere cifre. Tuttavia, il primissimo carattere deve essere una cifra. Inoltre, la prima cifra può essere uno zero solo se immediatamente seguita dal '.'. Infine, l'ultima cifra può essere uno zro soo se il carattere '.' not è presente.


```t
S> # Servirò: problem=infinity_of_N, service=archimede, num_rounds=5.")
S> # Ciao! Sei chiamato a convincermi che i razionali sono densi nei reali."
S> #  La impostiamo nella forma di un gioco:
S> #     Io ti propongo un numero reale positivo e tu dovresti rispondere con un numero naturale i cui inverso sia strettamente più piccolo del numero reale proposto.
S> 11.7
L> 1
S> 0.1
L> 11
S> 0.09
L> 50 
S> 0.02
L> 100
S> 0.01
L> 101
! Rinuncio. Hai vinto!
```
</details>

Tutte le possibilità di impiego menzionate sopra sono aperte anche per questo secondo servizio, come per ogni altro servizio TALight.