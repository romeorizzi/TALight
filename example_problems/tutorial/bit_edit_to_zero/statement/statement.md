#PROBLEMA BIT\_EDIT\_TO_ZERO
Ricevi in input un numero *n* e devi trasformarlo nel numero *0* impiegando il minor numero possibile di mosse.

Hai a disposizione due possibili mosse, entrambe meglio descritte guardando alla rappresentazione in binario del numero *n*:

* Mossa 1: inverte il valore del bit più a destra, ossia il bit di parità
* Mossa 2: inverte il valore del bit alla immediata sinistra del bit posto più a destra tra quelli settati ad uno. (Subito a destra del bit che si modifica deve esserci un bit settato ad *1*, e non vi è alcun bit settato ad uno a destra di questo).

I servizi disponibili per questo problema sono:  

* decimal\_to_binary: dato un numero decimale (random o scelto da te) ti viene chiesto trasformarlo nella sua forma binaria.
* total_steps: dato un numero binario (random o scelto da te) ti si chiede quale è il minimo numero di mosse (tra la 1 e 2) per farlo diventare *0*.
* next_step: dato un numero binario ti si chiede quale è la migliore mossa successiva  (tra la 1 e 2) avvicinare il numero allo zero. 
* trilly: chiedi aiuto alla fatina che ti dirà qual è la mossa successiva migliore.
