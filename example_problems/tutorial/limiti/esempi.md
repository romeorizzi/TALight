## Esempio ESISTENZA E CORRETTEZZA DI UN LIMITE:

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
    > # vedi: 0.77 < 0.96, quindi in realtà sei fuori dell'intervallo, quindi non sei riuscito a confutare la mia affermazione che il limite esista e valga 6.
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

## Esempio ESISTENZA MA NON CORRETTEZZA DI UN LIMITE:
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
    > # Wow mi hai convinto! Vale |f(x)-6| < epsilon per tutti i valori di x compresi nell'intervallo (x0-delta , x0+delta)=(0.9 , 1.1) che ho utilizzato per verificare il tuo risultato. 
    > # Ben fatto!


## Esempio di NON ESISTENZA DI UN LIMITE: (guidato)
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

Lo stesso esercizio si potrebbe fare in modo meno guidato, ovvero chiedendo se il limite non esiste proprio o se è sbagliato solo il risultato, nel primo caso poi si potrebbe chiedere se il problema sia che:
- i limiti destro e sinistro esistono finiti ma sono diversi (discontinuità prima specie)
- uno tra i limiti destro e sinistro è infinito o non esiste (discontinuità seconda specie)
- i limiti destro e sinistro esistono finiti e sono uguali tra loro ma non coincidono con la valutazione della funzione in x0 (discontinuità terza specie)
- i limiti destro e sinistro sono infiniti ma hanno segno opposto 

E poi continuare come visto sopra.



## Esempio SOMMA di successioni:
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
    > # Oh beh, contento te... Alla prossima!
  