# Ricopertura di una griglia mxn tramite barre hxk

Assegnati due numeri naturali $m$ ed $n$, il tuo programma deve stabilire se un foglio a quadretti mxn possa essere suddiviso in sottogriglie hxk con un paio di forbici. In altre parole, se la griglia mxn ammetta un tiling con barre di dimensioni hxk.

![esempio di tiling con piastrelle hxk](public/figs/Pavage_domino.svg)

Stabilire per quali valori di $m$ ed $n$ esista un tale tiling con barre 1x2 è la competenza che ti chiediamo di costruire ed esibire nell'esercizio tiling_1x2-bars_in_mxn-grids, che ti suggeriamo di considerare come propedeutico a questo, fanno parte di un medesimo percorso che ti proponiamo.

Ogni coppia di numeri naturali $(m,n)$ codifica una diversa istanza della domanda generale sopra formulata, ed è ben possibile che casi diversi meritino diverse risposte. Queste sono le domande che ci chiedono di sviluppare formule che rispondano una volta per tutte, o, con approccio più ampio (Turing completo), metodi ed algoritmi che rispondano per noi.
Non vi è alcun dubbio che il problema posto in questo esercizio sia decidibile: per ogni coppia di naturali fissati m ed n è possibile andare a verificare una per una tutte le possibilità. Tuttavia l'esplosione combinatoria di queste è tale che un tale approccio di fatto non terminerebbe entro la durata del nostro universo e della nostra vita. Questo non ci piace. Va bene ricorrere ad un algoritmo piuttosto che ad una formula, ma solo se ci consegna effettivamente la risposta, e magari più rapido di una formula bella all'apparenza ma di scarsa sostanza algoritmica.

Ok, ci saranno dei casi dove il tiling è possibile ed altri dove invece no. Il problema di decisione chiede: Sai distinguerli?

Nei casi in cui la tua risposta sia affermativa, riesci ad esibire un tale tiling disponendo le tessere una ad una?
Nota: siccome vi è un ovvio algoritmo efficiente che verifica la tua proposta di tiling, la tua proposta di tiling costituisce evidenza (certificato) del fatto che la risposta SI sia corretta. In teoria della complessità, la classe dei problemi di decisione per i quali esista un certificato verificabile del SI si chiama NP.

Nei casi in cui la tua risposta sia negativa, puoi esprimere una ragione per cui un tale tiling non possa esistere? Possiamo pre-accordare un certificato del NO che possa risultare compatto ed umanamente verificabile? (Questo equivarrebbe a collocare il problema anche in coNP, ossia a ben caratterizzarlo).

* goal 1: decidere, $m = 1$, $n \leq 100$
* goal 2: decidere, $m = h$, $n \leq 100$
* goal 3: decidere, $1 \leq m, n \leq 12$
* goal 4: decidere, $1 \leq m, n \leq 100$
* goal 5: decidere, $1 \leq m, n \leq 100.000$
* goal 6: costruire il tiling, $m = 1$, $n \leq 100$
* goal 7: costruire il tiling, $m = h$, $n \leq 100$
* goal 8: costruire il tiling, $1 \leq m, n \leq 10$
* goal 9: costruire il tiling,  $1 \leq m, n \leq 100$
