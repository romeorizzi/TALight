Costrire un grafo planare G=(V,E) con x1,y1,x2,y2 in V e tale che:
1. il grafo aumentato G'=(V,E + x1y1,y1x2,x2y2,y2x1) sia ancora planare;
2. G sia 3-colorabile ma per ogni 3-coloring c di G valga che:
   c(x1)=c(x2), e
   c(y1)=c(y2)
   

tra i suoi nodi con un planar ebedding dove i nodi
x1,y1,x2,y2


2 opzioni:
  o proponiamo un percorso che li accompagna su una riduzione già nota come quella sopra oppure (da valutare) quella di Lovasz
paper Lovasz: https://web.cs.elte.hu/~lovasz/scans/covercolor.pdf
esposizione Chvatal: https://users.encs.concordia.ca/~chvatal/notes/color.html
illustrative picture: https://cs.stackexchange.com/questions/37967/4-color-to-3-color-polynomial-reduction

 oppure a fronte di una riduzione pensata da loro li invitiamo a scrivere del codice per verificarla. Ad esempio, per il caso 3-colorability --> planar 3-colorability:

task1: scrivere una procedura che dato un grafo G costruisca un grafo planare G' che è 3-colorabile se e solo se lo è G

task2: scrivere una procedura che dato un grafo G ed una sua 3-colorazione produca una 3 colorazione del grafo planare G' di cui al punto 1

potremmo dare un servizio noi di eval per questo task (ha valenza piena)

task3: scrivere una procedura che dato un grafo G ed una sua 3-colorazione del grafo planare G' di cui al punto 1 produca una 3 colorazione di G

potremmo dare un qualche servizio di eval per questo task ma con valenza discutibile



