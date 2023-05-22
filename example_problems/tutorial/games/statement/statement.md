#PROBLEMA GAMES
Alice e Bob si alternano nell’atto di rimuovere pedine da un certo tavolo di gioco. Ad ogni suo turno, ciascun giocatore deve rimuovere una, oppure due, oppure tre pedine. Il giocatore che non riesce più a muovere (perchè il numero di pedine è ormai sceso a zero) perde la partita.

I servizi disponibili per questo problema sono:  

* game123: dato un numero di pedine ti si chiede di dire quale è la mossa che faresti (1 2 3 o 0 nel caso in cui tu avessi perso a priori)
* game123_interactive: ti permette di capire la dinamica del gioco, giocando con un avversario potente.
* game2stack: variante del gioco game123, ora hai due pile di pedine e puoi rimuovere tutte le pedine che vuoi in una pila alla volta per turno, quale sarà la tua mossa? 
	* (a,0) per togliere a pedine dalla pila 1, 
	* (b,0) per togliere b pedine dalla pila 2,
	* (0,0) se credi di aver perso in partenza. 