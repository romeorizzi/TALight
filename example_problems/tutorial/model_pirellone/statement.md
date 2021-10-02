# Pirellone come problema di programmazione matematica e modeling

preso dalla fase nazionale OII 2005 (Milano)
nome originale in statement italiano: Luci al Pirellone


## Descrizione del problema

Il Pirellone è un noto grattacielo di Milano, in cui le
finestre sono disposte ordinatamente per $M$ righe (piani) e
$N$ colonne. Le righe sono numerate da $1$ a $M$
(dall'alto in basso) e le colonne da $1$ a $N$ (da sinistra a
destra).

Non tutti i dipendenti spengono la luce dei loro uffici, la sera prima
di uscire. Quindi alcune finestre rimangono illuminate e tocca al
custode provvedere a spegnerle.

Per facilitare il compito del custode, sono stati predisposti
$M+N$ interruttori speciali, con un funzionamento
particolare.  Ci sono $M$ interruttori di riga e $N$
interruttori di colonna.  Quando il custode agisce
sull'$i$-esimo interruttore di riga, tutte le luci accese
dell'$i$-esima riga si spengono ma, allo stesso tempo, quelle
spente si accendono! Analogamente alle righe, un interruttore di
colonna spegne le luci accese di quella colonna e accende quelle
spente.

Aiuta il custode a decidere quali degli $M+N$
interruttori azionare al fine di spegnere tutte le luci delle finestre del Pirellone. Data la configurazione iniziale di luci, il custode
deve verificare se sia possibile spegnere le luci con gli interruttori
speciali e, in tal caso, deve specificare anche su quali interruttori
agire.

Elaborare un modello di PLI o di PL che ti consenta di rappresentare questo problema.  
Codificare il modello elaborato in GMPL per risolvere istanze del problema di dimensioni le più grandi possibile.

## File .dat con l'input

Per ogni possibile testcase, TuringArena invocherà il solver opensource `gplsol` utilizzando l'ozione `-m` per passargli il file `.gmpl` da voi sottomesso.

I parametri che descrivono l'istanza (ossia il Pirellone) di ogni singolo testcase si trovano entro un diverso file ASCII di tipo `.dat` che TuringArena passerà a `gplsol` utilizzando l'ozione `-d`.

Il formato di tale file `.dat` è esemplificato nel file [input_1.dat](public/input_1.dat) dove trovi codica del triangolo visualizzato sopra.
Tale codifica d'esempio è anche riportata in fondo al presente documento.

Le prime due righe del file `input.txt` contengono i due parametri $M$ ed $N$,
il numero di righe e di colonne del Pirellone, rispettivamente.

Le successive righe forniscono una descrizione della situazione
riscontrata dal guardiano:
ciascuna delle $M$ righe contiene una sequenza di
$N$ valori binari (0 oppure 1).  La sequenza
contenuta nell'$i$-esima di tali righe rappresenta lo stato
delle luci nell'$i$-esima riga (piano) del Pirellone. In
particolare, il $j$-esimo valore in tale riga indica se la
$j$-esima luce è accesa (valore = 1) oppure spenta
(valore = 0).


## File di output

La risposta va scritta nel file ASCII di nome `output.txt`, in due sole righe:
nella prima riga si specifica su quali interruttori di riga agire,
nella seconda riga si specifica su quali interruttori di colonna agire.
Del caso non fosse possibile spegnere tutte le luci del Pirellone,
allora si specifichi di non azionare alcun interruttore (interruttori tutti a zero sia sulla prima che sulla seconda riga).

Il file `.mod` da te sottomesso alla valutazione deve prescrivere che tale risposta venga scritta entro il file `output.txt` posto nella cartella corrente.


Il file `output.txt` deve contenere due linee per indicare
su quali interruttori deve agire il custode.

La prima linea contiene una sequenza di $M$ valori ($0$ oppure
$1$) separati da uno spazio.
L'$i$-esimo valore della sequenza indica se il custode deve
agire sull'interruttore dell'$i$-esima riga (valore = $1$)
oppure no (valore = $0$).

Analogamente, la seconda linea contiene una sequenza di $N$
valori ($0$ oppure $1$) separati da uno spazio, per rappresentare le
operazioni che il custode deve effettuare sugli interruttori di
colonna.  Il $j$-esimo valore della sequenza indica se il
custode deve agire sull'interruttore della $j$-esima colonna
oppure no.

Nel caso in cui non sia possibile spegnere tutte le luci del Pirellone
con gli interruttori speciali, tutti i valori delle due linee in
`output.txt` devono essere uguali a $0$.


## Assunzioni

* $1 < N \le 500$

## Goals:

*  Goal 1: caso di esempio
*  Goal 2: $2\leq M, N \leq 5$, $M \neq N$, solvable
*  Goal 3: $2\leq M, N \leq 5$, $M \neq N$, not solvable
*  Goal 4: $M = N = 10$
*  Goal 5: $M = N = 20$
*  Goal 6: $M = N = 30$
*  Goal 7: $M = N = 50$
*  Goal 8: $M = N = 100$
*  Goal 9: $M = N = 200$
*  Goal 10: $M = N = 300$

## Esempio di file `.dat` con l'input di un testcase

```
param M := 5;  # Numero di righe del pirellone

param N := 5;  # Numero di colonne del pirellone

param PIRELLONE :  1 2 3 4 5 :=

              1    1 0 1 1 0

              2    0 1 0 0 1

              3    1 0 1 1 0 

              4    0 1 0 0 1

              5    0 1 0 0 1 ;

end;
```

Tale file `.dat` è scaricabile [da questo link](public/input_1.dat).

L'intera suite dei testcase è scaricabile [da questo link](public/testcases.zip). Potrai quindi lavorare in locale, individuare eventuali errori o consentire i tempi che vorrai alle tue soluzioni, oppure provare in locale le tue soluzioni in AMPL od altri formati o sistemi. Ogni testcase è compiutamente descritto da una coppia di file. Ad esempio, a fianco del file `input_1.dat` visto sopra trovi anche il file `output_1.txt` che ne contiene la soluzione di riferimento.

Se in locale vuoi sperimentare con ulteriori, o anche più grosse istanze che non nelle assunzioni sopra, scaricati [queste](public/testcases-extra.zip).

Quando i tempi saranno maturi troverai delle soluzioni più o meno performanti discusse [quì](public/gallery_of_models.zip).


Un statement stampabile del problema in formato `.pdf` è scaricabile [da questo link](public/statement.pdf).
