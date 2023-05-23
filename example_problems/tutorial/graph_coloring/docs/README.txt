dal documento cross-over_gadget.pdf interessa solo la figura coi colori. Il gadget di cross-over è meglio spiegato, co suo utilizzo nel doc npcproblems.pdf
Il doc npcproblems.pdf è proprio quelo del Garey&Johnson (1979)

Il succesivo doc planar_4-regular_graphs.pdf è dove sono riusciti ad ottenre il risultato per 4-regular AND planar.
In fondo quel lavoro si basa tutto (se diamo per assodato quello in Garey&Johnson (1979)) sul grafo gadget in Fig. 2. (pag. 292)

costruzione pendaglio:
prendi un esagono che è un grafo planare bipartito
sulle 3 femmine aggiungi i 3 lati di un triangolo posto all'interno, sui tre maschi metti un altro triangolo ma posto all'esterno.
Hai così otteenuto un grafo di 6 nodi che è 4-regolare e 4-colorabile (per il Teorema dei 4 colori)).
Se di questo grafo apri un arco, puoi usarlo come pendaglio tra due nodi consecutivi su una stessa faccia per abbassarne il grado residuo in eccesso.

costruzione famiglia:
del grafo gadget in Fig. 2. (pag. 292) puoi prendere una catena di copie e poi si riducono i gradi in eccesso come accennato sopra.
(Con 2 copie ottieni il grado 4).
(Con 1 sola copia ottieni il grado 2).

Nota: per il lemma delle strette di mano possiamo ottenre grafi con t nodi di grado 3 e tutti gli altri di grado 4 solo se t è pari.

Claim: per ogni t,
   se t è pari posso produrre un grafo (planare) con tutti i nodi di grado 4 tranne t nodi di grado 3 (disposti tutti su una stessa faccia del planar embedding) e di size O(t).
   se t=2h+1 è dispari posso produrre un grafo (planare) con tutti i nodi di grado 4 tranne un noi di grado 2 e h nodi di grado 3 (disposti tutti su una stessa faccia del planar embedding) e di size O(t).
   


