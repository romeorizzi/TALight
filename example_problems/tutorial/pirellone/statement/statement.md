#PROBLEMA PIRELLONE
Il Pirellone è un noto grattacielo di Milano, le cui
finestre sono disposte ordinatamente su *M*  righe (piani) e
*N* colonne. Le righe sono numerate da *1* a *M* (dall'alto in basso)
e le colonne da *1* a *N* (da sinistra a destra). Il grattacielo quindi è rappresentabile con una matrice *M* x *N* dove vi è 1 se la luce è accesa, 0 se spenta.

Non tutti i dipendenti spengono la luce dei loro uffici, la sera prima
di uscire. Quindi alcune finestre rimangono illuminate e tocca al
custode provvedere a spegnerle.

Il custode non può entrare nei singoli uffici ma dispono di *M* + *N* interruttori speciali, con un funzionamento particolare.
Ci sono *M* interruttori di riga e *N* interruttori di colonna.
Quando il custode agisce sull'*i*-esimo interruttore di riga, tutte le luci accese dell'*i*-esima riga si spengono ma, allo stesso tempo, quelle
spente si accendono! Analogamente alle righe, un interruttore di
colonna spegne le luci accese di quella colonna e accende quelle
spente.

I servizi disponibili per questo problema sono:  

* compact_solution: data una matrice e una soluzione troppo lunga che la spegne  ti si chiede di accorciarla in base al goal e al livello di difficoltà che puoi settare tu. 
* sub_closure: data una matrice e la sua soluzione per spegnerla ti si chiede di trovare la soluzione di una sua sottomatrice che puoi sceglierla consecutiva o non, scegliendo se dare la soluzione più corta o una qualsiasi.
* check_unsolvability: puoi verificare se una tua matrice è non risolvibile, se è la più piccola con questa carratteristica.
* check_sol: puoi verificare se una soluzione è corretta di una tua istanza o di una randomica e il formato in cui darla: se come sequenza di mosse tipo `r1 c3 r4` o dare gli interruttori di riga `1 0 1 0` e colonna `0 1 1 0`.
* trilly: chiedi aiuto alla fatina che farà un numero di passi da te deciso per risolvere un'istanza random. 

