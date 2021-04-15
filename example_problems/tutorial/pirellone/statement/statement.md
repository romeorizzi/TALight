# Luci al Pirellone 

Questo problema è un revival del problema Pirellone da mè ideato per la Selezione Nazionale 2005 delle OII tenutasi a Milano.
Ho riportato la parte solo descrittiva del testo originale nel file `descrizione_originale_milano.md`.
Il testo integrale può essere trovato nella sottocartella `testo_originale`.


### Percorso didattico che vorremmo proporre sotto TALight (come abbiamo stabilito insieme)

diamo un'istanza, e diamo una soluzione intesa come una sequenza di mosse che spegne l'intero pirellone:

```
1 1 0
0 0 1
1 1 0

r1 c1 
```



Lemma: se una matrice è risolvibile ogni sua sottomatrice è risolvibileà

fornisco soluzione per marice grand,

   devono darmi soluzion per la sottomatrice fatta dalle prime 5 righe e prime 5 colonne

 (+)   devono darmi soluzion per la sottomatrice fatta da uno specificato sottoinsim di righe/di colonne fatta dalle prim 5 righe e prime 5 colonne

Possiamo definire il concetto di cattiva miniamale



fornire un controesmpio alla congettura 0:

   ogni pirellone è rislovibile

fornire un controesmpio "minimale" alla congettura 0:

   1. chidiamo al problem solver di far una soluzion di al più m+n mosse.

   2. chidiamo al problem solver di far una soluzion di al più (m+n)/2 mosse.



risolvere oppure restiture una cattiva minimale che vive dentro di esa  (tempo sponnziale)

risolvere oppure restiture una cattiva minimale che vive dentro di esa  (tempo polinomiale)

## Servizi TALight associati a qusto percorso:

vedere il file `meta.yaml`.

#PROBLEMA PIRELLONE
Il Pirellone è un noto grattacielo di Milano, le cui
finestre sono disposte ordinatamente su $M$  righe (piani) e
$N$ colonne. Le righe sono numerate da $1$ a $M$ (dall'alto in basso)
e le colonne da $1$ a $N$ (da sinistra a destra).

Non tutti i dipendenti spengono la luce dei loro uffici, la sera prima
di uscire. Quindi alcune finestre rimangono illuminate e tocca al
custode provvedere a spegnerle.

Il custode non può entrare nei singoli uffici ma dispono di $M+N$ interruttori speciali, con un funzionamento particolare.
Ci sono $M$ interruttori di riga e $N$ interruttori di colonna.
Quando il custode agisce sull'i-esimo interruttore di riga, tutte le luci accese dell'$i$-esima riga si spengono ma, allo stesso tempo, quelle
spente si accendono! Analogamente alle righe, un interruttore di
colonna spegne le luci accese di quella colonna e accende quelle
spente.
"""
Aiuta il custode a decidere quali degli $M+N$ interruttori azionare al fine di spegnere tutte le luci delle finestre del Pirellone.
Data la configurazione iniziale di luci, il custode deve verificare se sia possibile spegnere le luci con gli interruttori
speciali e, in tal caso, deve specificare anche su quali interruttori
agire. Altrimenti, segnala la situazione di impossibilità."""





