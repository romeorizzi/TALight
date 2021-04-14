# Formato `.dat` che proponiamo e supportiamo

Topolino ha numerato da $1$ ad $N$ le righe e le colonne del labirinto per poter trasmettere i dati della piantina ad Archimede. L'idea è che una coppia di numeri $(r, c)$ venga utilizzata per indicare il lastrone che si trova sulla riga $r$ e sulla colonna $c$. Si è deciso di segnare con un '1' i lastroni da evitare nell'attraversamento del labirinto, mentre i rimanenti sono segnalati con uno '0'.

## Esempio di file `.dat` con l'input di un testcase

L'esempio con N=5 del testo troverebbe codifica nel seguente file:

```
param N := 5;  # Numero di righe e colonne della mappa

param MAP :  1 2 3 4 5 :=

         1    0 0 0 1 0

         2    1 0 0 1 1

         3    0 1 0 1 0

         4    1 1 1 0 1

         5    1 0 0 1 0 ;

end;
```

Tale file .dat è scaricabile [da questo link](input_1.dat).

L'intera suite dei testcase, con anche i .dat file inclusi, è scaricabile [da questo link](testcases-dat.zip). Potrai quindi lavorare in locale, individuare eventuali errori o consentire i tempi che vorrai alle tue soluzioni, oppure provare in locale le tue soluzioni in GMPL/AMPL od altri formati o sistemi. Ogni testcase di questa suite è compiutamente descritto da una quadrupla di file (input.txt/input.dat/output.txt/opt_sol.txt). Ad esempio, a fianco del file `input_1.txt` visto sopra trovi anche il file `output_1.txt` che ne contiene la soluzione di riferimento e il file `opt_sol_1.txt` che può venirti utile per consultazione anche se, ovviamente, il più delle volte il percorso ottimo non sarà unico.

Se in locale vuoi sperimentare con ulteriori, o anche più grosse istanze che non nelle assunzioni sopra, la miglior opzione è avvalersi dei servizi TALight. Altrimenti scaricati [queste](testcases-dat-extra.zip).
