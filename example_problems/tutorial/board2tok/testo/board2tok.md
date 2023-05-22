# Tiling di Elle in scacchiera $2^k \times 2^k$ (board2tok)

1. ossevare che 2^k*2^k = 4^k = 1 (mod 3), quindi non puoi coprire tutte le celle, ma puoi porti l'obiettivo di coprirle tutte meno una.

Quale?

2. forniamo un servizio che controlla la bontà di un tiling (così uno può, se vuole, sperimntare per piccoli valori di k)

3. possiamo anche fornire un servizio che controlla la corretteza di una mappa che dice quali celle potrbbero essere l'unica cella lasciata scoperta (tutte, ma potrebbe aiutare farglielo scoprire/intuire/congetturare). (Possono quindi andare per una congettura più alta, dove è l'avverario a scgliere la cella).


# Percorso TALight per giungere a vedere una soluzione

il servizio ti manda k e la scelta di una cella d'angolo.
Quello che devi fare:
anche a mano, oppure il tuo bot, deve costruire un tiling di tutta la scacchiera 2^k x 2^k che eviti la cella d'angolo prefissata.

Puoi farlo scrivendo la soluzione come nel problema per il CMS quì sotto.

Puoi farlo tramite comandi del tipo:

fatina(sottogriglia di dimnsioni 2^{k-1} x 2^{k-1}, sua clla d'angolo da lasciare libera)

che potrai chiamare quante volte vorrai

oppure:

colloca_pezzo (posizione)

task 1:
puoi chiamare la fatina fino a 4 volte

task 2:
per ogni pezzo che metti giù tu guadagni 3 chiamate alla fatina

task 3:
nessuna chiamata alla fatina (in pratica scrivendo la soluzione come nel problema per il CMS quì sotto).

versione dove la cella da lasciare libera non è necessariamente una cella d'angolo.

Dialogo tipo:

> 3 1 1 SW
# ossia k=3 e lascia libera la cella (1,1) che è l'angolo a sud-west della griglia che abbiamo in mente
< trilly 2 1 1 SW
# ossia chiamata ricorsiva k=2 lasciando libera la cella (1,1)vista come angolo in basso a sinista
< trilly 2 5 1 NW
< trilly 2 5 5 SE
< trilly 2 1 5 SW
< trilly 0 4 4 SW


## Descrizione del problema

Con riferimento ad una griglia quadrata, un _tromino_ è quell’unico pezzo ad elle che può essere disposto in modo da ricoprire perfettamente $3$ celle: due disposte in diagonale tra loro e la terza adiacente ad entrambe.  
Quest’ultima è detta _centrale_, le prime due _periferiche_. Una griglia quadrata di $2^k$ righe e colonne ha $4^k$ celle, e poichè $4^k$ non è divisibile per $3$, essa non può ammettere un tiling con tromini (le sue celle non possono essere partizionate in triplette dove ogni tripletta costituisca un tromino).  
Se insistiamo sul fatto che i tromini impiegati non si sovrappongano, allora almeno una cella dovrà rimanere scoperta, e forse $4$, o più. Questo esercizio chiede di dimostrare che si può sempre fare lasciando scoperta una sola cella.  
Di fatto si chiede di verificare se possa essere vera un’affermazione più forte: esiste sempre una soluzione anche quando la cella da lasciare scoperta venga scelta da un avversario?

## File di input

Il programma deve leggere da un file di nome `input.txt` tre interi separati da spazio: $k$, $r$, $c$.  
Il primo ( $k$ ) indica le dimensioni della scacchiara, gli altri due indicano la riga e la colonna della cella che vi si chiede di lasciare scoperta.

## File di output

Il programma deve scrivere in un file di nome `output.txt` la stringa “NONE” qualora nessuna soluzione esista. Altrimenti fornisce descrizione di una soluzione scrivendo nel file `output.txt` una tabella di $2^k × 2^k$ caratteri presi dall’alfabeto {’0’,’1’,’2’,’3’,’4’,’N’,’E’,’S’,’W’}.  
La codifica della soluzione segue la seguente convenzione: lo ’0’ viene collocato sulla cella che resta scoperta, e poi, per ogni pezzo di tromino nel tiling, sulle celle periferiche si riporta un carattere dell’alfabeto {’N’,’E’,’S’,’W’} a seconda che la cella risulti a nord, est, sud, oppure ovest della cella centrale per quel tromino. Sulla cella centrale si riporta un carattere dell’alfabeto {’1’,’2’,’3’,’4’} per indicare in quale dei seguenti casi ci si ritrovi:



- ’1’ se le due celle periferiche sono etichettate ’N’ ed ’E’. Il tromino è:

```
               +---+
               |   |
               | N |
               |   |
               +-------+
               |   |   |
               | 1 | E |
               |   |   |
               +---+---+

```

- ’2’ se le due celle periferiche sono etichettate ’E’ ed ’S’. Il tromino è

```
               +---+---+
               |   |   |
               | 2 | E |
               |   |   |
               +-------+
               |   |
               | S |
               |   |
               +---+
```

- ’3’ se le due celle periferiche sono etichettate ’S’ e ’W’. Il tromino è

```
               +---+---+
               |   |   |
               | W | 3 |
               |   |   |
               +-------+
                   |   |
                   | S |
                   |   |
                   +---+
```

- ’4’ se le due celle periferiche sono etichettate ’W’ e ’N’. Il tromino è

```
                   +---+
                   |   |
                   | N |
                   |   |
               +-------+
               |   |   |
               | W | 4 |
               |   |   |
               +---+---+
```

## Assunzioni

- righe e colonne sono numerate da $0$ a $2^k-1$.
- $k ≤ 10$.

## Subtask

- **Subtask 1 \[0 punti\]:** caso di esempio.
- **Subtask 2 \[10 punti\]:** $k = 2$.
- **Subtask 3 \[40 punti\]:** il buco è collocato in angolo della scacchiera $2^k × 2^k$.
- **Subtask 4 \[10 punti\]:** $k = 3$ (scacchiera $8 × 8$).
- **Subtask 5 \[40 punti\]:** $k ≤ 10$.

## Esempio di input/output

| File input.txt | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | File output.txt |
| :------------  | :----------------------------------: | :-------------- |
| 3 1 1 | &nbsp; | 2EW32EW3<br>S0NSSW3S<br>NW4NW3SN<br>1EW4NSW4<br>2ENW4NW3<br>SN1EW4NS<br>N1ENNW4N<br>1EW41EW4 |
