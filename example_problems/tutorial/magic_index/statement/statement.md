# Magic Indexes

Per ora quanto stiamo componendo su:

https://etherpad.wikimedia.org/p/Luca&Deborah

### Nostre prime riflssioni sul problema:

PROBLEMA PROPOSTO:
    Input: un vettore ordinato A di n numeri interi/pari distinti
    Def:  è un magix-index ogni i tale che A[i]=i.
    Task: trovare i magic index/il magic index se ce ne è.
    
    Voglia di log n checks
    
    se ce ne sono formano un intervallo consecutivo

==================================================================

PROBLEMA DA RICERCA BINARIA: 

Input: ho un vettore di palline bianche e nere dove a sinista di una pallina nera tutte le palline sono nere.

Trovare dove avvine l'eventuale transizione.

==================================================================

Nel vettore avete che i numeri sono disposti in modo ordinato e sono numeri interi diversi (tra uno e l'altro c'è un salto di almeno uno).

BIANCO = sono più grande della posizione che occupo
NERO = sono più piccolo della posizione che occupo
GRIGIO = sono magic index

