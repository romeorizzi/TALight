# Possibili quesiti

1. data una tripla (k, r, c), e un (k, r, c)-tiling, il servizio lo verifica.

2. data una tripla (k, r, c), il servizio risponde sì se esiste un tiling della scacchiera 2^k x 2^k che lascia sgombra solo la cella (r,c). Se chiamato con l'argomento gimme_first_rows_of_sol=n restituisce le prime n righe di un tiling certificante.

Analisi delle griglie con perfect tiling di L:

1. se il numero delle celle non è divisibile per 3, non si può fare.

2. se una dimensione è divisibie per 2 e l'altra per 3 allora SI (si può tilare con sottogriglie 2x3, e una griglia 2x3 è fatta di 2 L.

3. m x 1 non è tilable

4. 6 x 5 è tilable

5. 6k x 5 è tilable (segue da 4)

6. 6k x n, n > 1 è tilable (proof: se non fosse tilable allora, poichè n > 1 e considerato 2, n non sarebbe nè pari nè divisibile per 3. Quindi n >= 5. Per 5, n>5 nè pari nè divisibile per 3. Allora decompongo 6k x n in 6k x 2 + 6k x (n-2).

7. 3 x (2n + 1) non è tilable

8. quindi 3k x n si può fare se e soo se n è pari. Resta da capire k disari > 1.

8. 9 x 5 è tilable

9. 9 x n, n >= 5 è tilable

10. 3k x n, k dispari > 1, n > 3 è tilable

QED

========




8. dare suggerimenti su come procedere
  -  vedere il problema come tanti sottoproblemi di dimensioni minori
  - chiamata ricorsiva a k-1 e via dicendo

Si, sarebbe ottimo.
E' anche quanto crchiamo di fare coi servizi di tipo trilly.

9. è TALight a decidere quale cella lasciare libera, quindi è TALight a fornire il problema nel formato (k, r, c) e quindi l'utente fornirà una possibile soluzione
  - se l'utente non è in grado, TALight può aiutare, suggerendo come procedere
  - la prima riga (livello principiante)
  - il primo tromino (livello intermedio)
  - utilizzare la fatina (livello avanzato, l'utente viene aiutato a ragionare, tipo colloquio con una persona)
