# Individuare la Moneta Leggera (light_coin)

## Descrizione del problema

Devi scrivere una procedura che individui l'unica moneta falsa in un set di *n* monete numerate da *0* ad *n-1*. Il file da sottomettere deve avere la seguente struttura:

```cpp
#include "ourLibToPlay.h"

void individua(long int n) {
   ...
} 
```

Il parametro *n* che viene passato alla funzione `individua()` è il numero di monete sotto esame. Tutte le *n* monete hanno lo stesso peso, tranne quella falsa, che è più leggera delle altre. 

Potrai servirti di una bilancia a braccia eguali invocando, dalla tua implementazione della procedura `individua()`, la seguente funzione: 

```cpp
int piatto_con_peso_maggiore();
```



La funzione prevede i seguenti 3 possibili valori di ritorno:

- **NONE:** se i due piatti della bilancia sono in perfetto equilibrio;

- **LEFT:** se il carico è maggiore sul piattto sinistro;

- **RIGHT:** se il carico è maggiore sul piatto destro;

dove `LEFT = -1`, `NONE = 0` e `RIGHT = 1`sono 3 costanti intere deﬁnite per voi in *ourLibToPlay.h*. 

Per portare una certa moneta da dove si trova attualmente ad un certo piatto (`LEFT`, `RIGHT`, oppure anche `NONE` nel caso si voglia togliere la moneta dalla bilancia) si invoca la procedura:

```cpp
void collocaMoneta(long int, int moneta, int piatto);
```

Quando trova la moneta falsa, la tua procedura deve consegnarla alla zecca invocando:

```cpp
void denuncia(long int monetaFalsa);
```

## Assunzioni

- Il programma termina dopo la prima chiamata alla funzione denuncia oppure allo scadere del tempo limite.

- $1 <= n <= 1,000,000$

## Obbiettivi

1. Trovare la moneta falsa.

2. Trovare la moneta falsa tra 7 monete ($n = 7$) con al massimo 6 pesate.

3. Trovare la moneta falsa tra 7 monete ($n = 7$) con al massimo 4 pesate.

4. Trovare la moneta falsa tra 7 monete ($n = 7$) con al massimo 3 pesate.

5. Trovare la moneta falsa tra 8 monete ($n = 8$) con al massimo 3 pesate.

6. Trovare la moneta falsa con al più $n - 1$ pesate.

7. Trovare la moneta falsa con al più $\lfloor n/2 \rfloor$ pesate.

8. Trovare la moneta falsa con al più $\lfloor log_2 n \rfloor$ pesate.

9. Viene permesso solo quel minimo numero di pesate che, se impiegato, sapientemente, consenta sempre di individuare la moneta falsa.
