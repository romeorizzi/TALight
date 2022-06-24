## NUMERI REALI
**1.** Ogni insieme finito e non vuoto di numeri reali ammette sempre un massimo. 
<details><summary><strong>Esercizio - dimostrazione: </strong></summary>

	> # proviamo a vedere se in un insieme finito e non vuoto di numeri reali riusciamo a trovare sempre un massimo.
    > # dato l'insieme costituito da:
	> 0, 6.3, 5/4, -14.31, pi, 28.7333, sqrt(2), -9*pi
    > # determina il massimo:
	< 28.7333
	> # bene! vuoi fare un'altra partita o ti senti pronto a passare ad un livello successivo? (another_match/next_level)
	< another_match
    > # dato l'insieme costituito da:
	> 57/13, e, -sqrt(17), pi*0.65, -sin(30)*7, sqrt(5)
    > # determina il massimo:
	< 57/13
	> # bene! vuoi fare un'altra partita o ti senti pronto a passare ad un livello successivo? (another_match/next_level)
	< next_level
    > # ok! ecco una proposta per il livello successivo: 
	> # riusciresti a scrivere un algoritmo ricorsivo che calcoli per te il massimo di un insieme finito? 
	< .......
</details>

**2.** Se un insieme non è finito potrebbe non ammettere massimo.
<details><summary><strong>Esercizio: </strong></summary>

	> # Se un insieme non è finito potrebbe non ammettere massimo.
	> # {x in R | 8 <= x^3 <= 125}
	> # l'insieme ha massimo? (y/n)
	< y
	> # sì? allora dammelo:
	< 5
	> # bene! proviamo con un altro esempio
	> # {x in R | x < 15/2}
	> # l'insieme ha massimo? (y/n)
	< y
	> # sì? allora dammelo:
	< 15/2
	> # guarda che 15/2 non appartiene all'insieme... quindi non è un massimo!
	> # l'insieme ha massimo? (y/n)
	< n
	> # bene! vuoi procedere con un altro esercizio o fermarti? (next/stop)
	< stop
	> # alla prossima!
</details>

**3.** Un insieme limitato (superiormente/inferiormente/entrambi) non sempre ammette massimo/minimo.
<details><summary><strong>Esercizio: </strong></summary>

	> # Un insieme limitato non sempre ammette massimo/minimo. 
	> # {x in R | 8 <= x^3 <= 125}
	> # ha massimo? (y/n)
	< n
	> # esistono numeri in questo insieme maggiori di 5? (y/n)
	< n
	> # 5 appartiene all'insieme? (y/n)
	< y
	> quindi 5 è un massimo, sei d'accordo? (y/n)
	< y
	> # bene! proviamo con un altro esempio
	> # {x in R | x^3 >= 27}
	> # ha massimo? (y/n)
	< n
	> # bene! vuoi procedere con un altro esercizio o fermarti? (next/stop)
	< stop
	> # alla prossima!
</details>

**4.** Un numero k $\in$ X (dove X è un insieme totalmente ordinato) è un **maggiorante** di Y $\subseteq$ X se k >= x per ogni x \in Y.

**5.** L'**estremo superiore**  di Y è il minimo dei maggioranti.
<details><summary><strong>Esercizio: </strong></summary>

	> # Sia Y = {x in R | -27 < x^3 <= 64}
	> # Y ha massimo? (y/n)
	< y
	> # sì? allora dammelo:
	< 4
	> # Y ha (almeno) un maggiorante?
	< y
	> # sì? allora dammelo:
	< 67
	> # determina l'estremo superiore di Y:
	< 5
	> # vedi, basta prendere 4.999999 che è minore di 5 e non è in Y... 5 non può essere estremo superiore, riprova:
	< 4
	> # perfetto! nota infatti che se esiste un massimo, esso coincide con il sup!
	> # vuoi procedere con un altro esercizio o fermarti? (next/stop)
	< stop
	> # ciao, alla prossima!
</details>

**6.** Ogni insieme Y $\subset$ X non vuoto e limitato superiormente possiede estremo superiore.

**7.** L'insieme **R** dei numeri reali è un campo ordinato con la proprietà dell'estremo superiore vista al punto precedente.

## ARCHIMEDE
#### Principio:
Per ogni $x \in$ **R**, $x > 0$, esiste $n \in$ **N** tale che $\frac{1}{n} < x$.

<details><summary><strong>Esercizio</strong> ("dimostrazione" del principio di Archimede immediata... giocando solo con x e n...)</summary>

	> #saresti propenso a credere che per ogni numero reale x > 0 esiste un numero naturale n tale che 1/n < x? (y/n)

_1) se il ragazzo risponde di **no**:_

    < n
    > # ah no? proviamo! inserisci un qualsiasi valore x > 0:
    < 0.0034
    > # vedi, per n= 295 vale 1/n= 0.00338 e 0.00338 < 0.0034=x.
    > # mi credi ora? (y/n)
	< n
    > # ah no? proviamo! inserisci un qualsiasi valore x > 0:
    < 26.58
    > # vedi, per n= 1 vale 1/n= 1 e 1 < 26.58=x.
    > # mi credi ora? (y/n)
    > y
    > Bene! Se vuoi provare a convincermi tu ora, invertendo i ruoli, ti consiglio questo esercizio: 
	> rtal connect limiti ....

_2) se il ragazzo ripsonde di **sì**:_

    < y
    > # bene! allora prova a convincermi
	> # la mia proposta per x è:
	> 3*pi
	> # dammi una n tale che 1/n < x:
	< 0.09
    > # vedi, 0.09 non è un numero naturale, riprova:
	> # dammi una n tale che 1/n < x:
    < 1
    > # per n=1 vale 1/n=1 e 1 < 9.424777961=x
	> # mi stai iniziando a convincere, voglio riprovare
	> # la mia proposta per x è:
	> sqrt(2)*1/6
	> # dammi una n tale che 1/n < x:
	< 5
    > # per n=5 vale 1/n=0.2 e 0.2 < 0.2357=x
	> # ok mi hai convinto! ottimo lavoro!
	> # preferisci fermarti qui o ti senti pronto a passare ad un livello successivo? (stop/next_level)
	< next_level
    > # ok! ecco una proposta per il livello successivo: 
	> # scrivi un algoritmo che, dato x, calcoli per te un valore di n che soddisfi il principio di Archimede:
	< ......
</details>

		
CORRELAZIONI:
* Una successione di termini positivi convergente deve avere un limite strettamente positivo?
No, basta prendere la successione 1/n costituita di termini positivi ma convergente a 0
* Dimostrare che la successione 1/n, n=1,2,3,... tende a zero:
usare il fatto che per Archimede preso a piacere x > 0 esiste un numero n naturale tale che n * x > 1. Dunque, 1/n < x.

<details><summary><strong>Esercizio/curiosità - un piccolo salto verso i limiti di successioni</strong></summary>

    > # Il limite di una successione convergente di termini positivi non è sempre strettamente positivo
    > # sei d'accordo con me? (y/n)
    < n
    > # Allora consideriamo la successione 1/n, n=1,2,3,... questa successione è composta da termini positivi? (y/n)
    < y
    > # Ma non converge ad un numero strettamente positivo... converge a 0!
    > # sei d'accordo con me? (y/n)
_se risponde no_

	< n
    > # Stabilisci un numero reale epsilon > 0:
    < 0.4
    > # Ecco il mio N:
    > # 2.5
    > # Proponi una tua x > 2.5:
    < 2.6
    > # vedi: 1/2.6 =0.38, e 0.38 \in [-0.4 , 0.4]=[l-e,l+e], quindi non sei riuscito a confutare la mia affermazione.
    > # Sei convinto ora che la successione converga a 0? (y/n)
    > y
    > # Bene, alla prossima!
_se risponde sì_

	< y
	> # bene, allora non avrai problemi a dimostrarmelo!
	> # il mio valore per epsilon è:
	> 0.15
	> # proponi il tuo N:
	< 6.7
    > # Molto bene! Vale |1/n - 0| < 0.15 per tutti i valori di n > 6.7 che ho utilizzato per verificare la tua proposta.
	> # Alla prossima!
</details>

## DENSITA` DI Q IN R
#### Enunciato (prima forma):
Siano x,y due numeri reali, x < y ; esiste q $\in$ **Q** tale che  x < q < y. Ovvero **Q** è denso in **R**.
<details><summary><strong>Esercizio - dimostrazione</strong></summary>

    > # dimostra che dati x,y due numeri reali, x < y , esiste q razionale tale che  x < q < y. Ovvero Q è denso in R.
    > # il mio valore per la x è:
    > 3.3
    > # il mio valore per la y è:
	> 3.4
	> # scrivi un numero naturale n che soddisfi il principio di Archimede (con argomento y-x):
	< 8
	> # no, 1/8 = 0.125 e 0.125 > 0.1=y-x, riprova!
	< 11
	> # bene, nota ora che 11x vale
	> 36.3
	> # e 11y vale
	> 37.4
	> # dimmi un intero in (36.3 , 37.4):
	< 37
	> # utilizzando questo intero e la n che mi hai proposto, riesci a trovare un numero razionale (della forma a/b) compreso tra 3.3 e 3.4? scrivilo:
	< 37/11
	> # Ben fatto! Abbiamo trovato la q che cercavamo, ovvero 37/11 = 3.36...
	> # vuoi fare un'altra partita o ti senti pronto a passare al livello successivo? (another_match/next_level)
	< next_level
	> # Riusciresti ora a scrivere un algoritmo che dati x e y trovi q?
	< ..............
	
</details>


##### Enunciato (seconda forma):
Ogni numero reale è limite di una successione di razionali (di più, è limite di una successione di numeri decimali)
<details>

**Dimostrazione:**

Prendiamo un numero reale alfa = a_0. a_1 a_2 a_3 a_4..... (esempio: se alfa=3.459 allora a_0=3, a_1=4, a_2=5, a_3=9)

alfa è il limite della successione y_n di numeri razionali (decimali):

y_0 = a_0

y_1 = a_0. a_1

y_2 = a_0. a_1 a_2

............

y_k = a_0. a_1 a_2....a_k 

............

Poichè |y_k - alfa | <= 1/10^k, si ha: lim{n->+inf} y_n = alfa.

**Esempio:**

alfa=sqrt(2)=1.414213562...

y_0=1

y_1=1.4

y_2=1.41

y_3=1.414

............

y_6=1.414213

y_7=1.4142135

............

|y_3 - alfa | = 0.000213562... <= 1/10^3 = 0.001 e per ogni n>3 si ha |y_n - alfa| < 0.001  (infatti ad esempio |y_4 - alfa|=0.000013562 < 0.001 e così via)  dimostrando così che lim{n->inf} y_n = alfa
<details><summary><strong>Esempio di dialogo:</strong></summary>

    > # dimostra che ogni numero reale è limite di una successione di razionali (di più, è limite di una successione di numeri decimali)
    > # dimostra quindi che lim{n->inf} y_n = alfa, dove 
    > alfa = sqrt(2) = 1,414213562373095049...
    > y_0=1
    > y_1=1.4
    > y_2=1.41
    > y_3=1.414
    > y_4=1.4142
    > y_5=1.41421
    > y_6=1.414213
    > y_7=1.4142135
    > ............
    > # ecco il mo epsilon:
    > 0.004
    > # stabilisci una M > 0 :
    < 3
    > # Molto bene! Vale |y_n - alfa| < 0.004 per tutti i valori di n > 3 che ho utilizzato per verificare la tua proposta.
    > # Hai dimostrato che lim{n->inf} y_n = alfa, ottimo lavoro!
</details>
</details>

## LIMITI DI FUNZIONI/SUCCESSIONI

<details><summary><strong>Esercizio ESISTENZA E CORRETTEZZA DI UN LIMITE:</strong></summary>

    rtal connect limiti exist_prover (istanza da catalogo)
    dimostra che il limite lim_{x --> 1} x^2+5
    > # esiste e vale
    > 6
    > # ti ho convinto? (y/n)
    < n
    > # allora stabilisci una tollerenza epsilon > 0
    < # ecco il mio epsilon:
    < 0.1
    > # ecco il mio delta:
    > # 0.04 (opppure più piccolo)
    > # proponi il tuo x nell'intorno [0.96,1.04]
    < 0.77
    > # vedi: 0.77 < 0.96, quindi in realtà sei fuori dell` intervallo, quindi non sei riuscito a confutare la mia affermazione che il limite esista e valga 6.
    > # lo vedi? Sei convinto che il limite esista e valga 6? (y/n)
    < n
    > # allora stabilisci una tollerenza epsilon > 0
    < # ecco il mio epsilon:
    < 0.1
    > # ecco il mio delta:
    > # 0.04 (opppure più piccolo)
    > # proponi il tuo x nell'intorno [0.96,1.04]
    > 0.98
    > # vedi: f(0.98) = y (=5.96), e y in [5.9,6.1]=[l-e,l+e], quindi non sei riuscito a confutare la mia affermazione che il limite esista e valga 6.
    > # lo vedi? Sei convinto che il limite esista e valga 6? (y/n)
    > y
    > # Oh beh, contento te... Alla prossima!
</details>

<details><summary><strong>Esercizio ESISTENZA MA NON CORRETTEZZA DI UN LIMITE:</strong></summary>

    rtal connect limiti exist_prover (istanza da catalogo)
    dimostra se il limite lim_{x --> 1} x^2+5
    > # esiste e vale
    > 9
    > # ho ragione? (y/n)
    < n
    > # ah no? allora stabilisci una tollerenza epsilon > 0
    < # ecco il mio epsilon:
    < 0.1
    > # ecco il mio delta:
    > # 0.05 (opppure più piccolo)
    > # proponimi una x nell'intorno [0.95,1.05]
    < 1.03
    > # oh oh pare che tu mi abbia colto in fallo! f(1.03) = 6.06, e 6.06 non è in [8.9,9.1]=[l-e,l+e]. Quindi, dato che la mia affermazione pare non essere corretta, qual è il vero limite a cui tende questa funzione?
    < 7
    > # non so se mi fido molto, controlliamo insieme:
    > # il mio epsilon è:
    > 0.3
    > # stabilisci un tuo valore per delta > 0:
    < 0.14
    > non va bene, mi è bastato controllare la funzione in x=0.87, valore compreso in (1-0.14 , 1+0.14), ed ho constatato che f(0.87)=5.76 e 5.76 non è in (6.86 , 7.14)=(l+eppsilon , l-epsilon)
    > # vuoi correggere il tua delta o il risultato del limite? (delta/limite)
    < limite
    > # va bene, prova a dirmi il tuo risultato per lim_{x --> 1} x^2+5:
    < 6
    > # vediamo se hai ragione:
    > # il mio epsilon è:
    > 0.06
    > # stabilisci un tuo valore per delta > 0:
    < 0.1
    > # Wow mi hai convinto! Vale |f(x)-6| < epsilon per tutti i valori di x compresi nell` intervallo (x0-delta , x0+delta)=(0.9 , 1.1) che ho utilizzato per verificare il tuo risultato. 
    > # Ben fatto!
</details>

<details><summary><strong>Esercizio di NON ESISTENZA DI UN LIMITE: (guidato)</strong></summary>

    rtal connect limiti exist_prover  (istanza da catalogo)
    dimostra se il limite lim_{x --> 0} 1/x
    > # esiste e vale
    > + inf
    > # mi credi? (y/n)
    < n
    > ah no? allora stabilisci una tolleranza N > 0
    < 5
    > # studiamo il limite destro e sinistro
    > # ecco il mio delta:
    > # 0.2
    > # proponi il tuo x nell'intorno (0 , 0.2)
    < 0.08
    > # ok, f(0.08) = 12.5 e 12.5 > N, quindi per ora vale la mia affermazione che il limite esista e valga +inf.
(si può fare una prova su due tre valori di x prima di passare al limite sinistro)

    > # proponi ora il tuo x nell'intorno (-0.2 , 0)
    < -0.15
    > # Oh no! f(-0.15) = -0.6666 e -0.6666 < N 
    > # Mi hai smentito! Non è vero che il limite esiste e vale +inf.
    > # Questo limite non esiste proprio, ben fatto!
</details>

Lo stesso esercizio appena visto si potrebbe fare in modo meno guidato, ovvero chiedendo se il limite non esiste proprio o se è sbagliato solo il risultato, nel primo caso poi si potrebbe chiedere se il problema sia che:
- i limiti destro e sinistro esistono finiti ma sono diversi (discontinuità prima specie)
- uno tra i limiti destro e sinistro è infinito o non esiste (discontinuità seconda specie)
- i limiti destro e sinistro esistono finiti e sono uguali tra loro ma non coincidono con la valutazione della funzione in x0 (discontinuità terza specie)
- i limiti destro e sinistro sono infiniti ma hanno segno opposto 

E poi continuare come visto sopra.



<details><summary><strong>Esercizio SOMMA di successioni:</strong></summary>

    rtal connect limiti sum_prover (istanza da catalogo)
    > # dimostra che se lim_{x --> inf} (x-1)/x = 1 e lim_{x --> inf} x/(2x+3) = 1/2 
    > # allora lim_{x --> inf} (x-1)/x + x/(2x+5)
    > # esiste e vale
    > 3/2
    > # ti ho convinto? (y/n)
    < n
    > # allora consideriamo i due limiti singolarmente e poi la loro somma:
    > # stabilisci una tollerenza epsilon > 0 che varrà per tutto l'esercizio:
    < # ecco il mio epsilon:
    < 0.3
    > # il mio M_1, che vale per la funzione (x-1)/x e dipende da epsilon/2, è:
    > # 7
    > # proponi il tuo x > 7
    < 8
    > # vedi: f(8) = 0.875, e 0.875 in [0.85 , 1.15]=[l-epsilon/2,l+epsilon/2], quindi non sei riuscito a negare la mia affermazione che lim_{x --> inf} (x-1)/x = 1.
    > # Sei convinto che il limite esista e valga 1? (y/n)
    < y
    > # bene, passiamo al secondo limite
    > # ho ragione ad affermare che lim_{x --> inf} x/(2x+3) = 1/2? (y/n)
    < y
    > # ok, allora non avrai problemi a dimostrarlo insieme a me:
    > # proponi il tuo M_2 > 0 dipendente da epsilon/2:
    < 3.5
    > # Perfetto! Vale |g(x)-1/2| < 0.15 per tutti i valori di x > 3.5 che ho utilizzato per verificare la tua proposta.
    > # Cerchiamo quindi di concludere la nostra dimostrazione: per (x-1)/x + x/(2x+5)
    > # ecco il mio M_3:
    > # 7
    > # proponi il tuo x > 7
    < 9
    > # vedi: f+g (9) = 1.3175, e 1.3175 in [1.2 , 1.8]=[l-epsilon,l+epsilon], quindi non sei riuscito a confutare la mia affermazione che  lim_{x --> inf} (x-1)/x + x/(2x+5) esiste e vale 3/2.
    > # lo vedi? Sei convinto che il limite esista e valga 6? (y/n)
    < y
    > # Perfetto, alla prossima!

</details>
