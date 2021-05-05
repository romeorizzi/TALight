# Magic Indexes

### Nostre prime riflessioni sul problema:

PROBLEMA PROPOSTO:
    Input: un vettore ordinato A di n numeri interi/pari distinti
    Def:  ogni posizione i=0, ..., n-1, tale che A[i]=i è un magix-index.
    Task: trovare i magic index/il magic index se ce ne sono.
    
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

