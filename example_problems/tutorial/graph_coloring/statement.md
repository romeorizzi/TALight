Diamo per scontata l'NP-completezza del seguente problema:

INPUT: un grafo qualsiasi G
TASK: decidere se G sia 3 colorabile


Obiettivo alto-livello, cosa devono riuscire a fa re infine loro:

task1: scrivere una procedura che dato un grafo 4-regolare G costruisca un grafo planare (4-regolare) G' che è 3-colorabile se e solo se lo è G

task2: scrivere una procedura che dato un grafo 4-regolare G ed una sua 3-colorazione produca una 3 colorazione del grafo planare (4-regolare) G' di cui al punto 1

potremmo dare un servizio noi di eval per questo task (ha valenza piena)

task3: scrivere una procedura che dato un grafo 4-regolare G ed una 3-colorazione del grafo planare G' di cui al punto 1 produca una 3 colorazione di G

Internamente, possiamo avere più goals:
  gradi di G': i gradi dei nodi sono arbitrari | i gradi sono tutti <= 4 | i gradi sono tutti 4

Esternamente:
possiamo concatenare questa riduzione alla riduzione da grafo con grada massimo 4 a grafo 4-regolare (basata sulla farfalla del lavoro che abbiamo visto)
possiamo concatenare questa riduzione alla riduzione da grafo generico a grafo con grado massimo 4:
per rappresentare un nodo di grado 4+k si prende una catena di k farfalle. Probabilmente usando il numero preciso di farfalle necessarie si sbarca direttamente su un 4-regolare (se si opera anche sui nodi di grado inferiore a 4)


Siccome temiamo che lo studente non sappia da dove partire, gli proponiamo delle sfide intermedie con cui andrà ad esplorare autonomamente il problema da un lato e dall'altro si ritrova poi con de gadget già fatti.

Tra queste:

Costrire un grafo planare G=(V,E) con x1,y1,x2,y2 in V e tale che:
1. il grafo aumentato G'=(V,E + x1y1,y1x2,x2y2,y2x1) sia ancora planare;
2. G sia 3-colorabile ma per ogni 3-coloring c di G valga che:
   c(x1)=c(x2), e
   c(y1)=c(y2)
   
Ricordiamoci di segnalare loro che possono anche ricevere supporto in merito a riduzioni pensata più o meno interamente da loro, o lette da letteratura che gli segnaliamo o trovata autonomamente anche altrove. Infatti, se scrivono del codice (la riduzione e le proof dei lemmi easy ed hard) per verificarla, oltre a poterla sempre verificare in autonomia per il problema generico, possono verificarla almeno parzialmente con noi per questo probblema specifico (supporto sulle istanze, su dei verificatori e su degli script).
Ad esempio, per il caso 3-colorability --> planar 3-colorability  avremo anche qualche servizio di tipo eval per questo task (anche se con valenza discutibile)

letteratura con riduzioni già note:
quella sopra legata al Garey&Johnson
quella di Lovasz per la k-colorability con k generico:
paper Lovasz: https://web.cs.elte.hu/~lovasz/scans/covercolor.pdf
esposizione Chvatal: https://users.encs.concordia.ca/~chvatal/notes/color.html
illustrative picture: https://cs.stackexchange.com/questions/37967/4-color-to-3-color-polynomial-reduction

