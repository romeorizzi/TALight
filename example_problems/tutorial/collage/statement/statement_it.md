# Arcobaleno e Collage

### Descrizione del problema

Nel pianeta Wobniar ogni mattina splende un bellissimo e caratteristico **arcobaleno**. La particolarità consiste nella disposizione dei colori, che possono presentarsi più volte all'interno dell'arco in una sequenza sempre nuova e sorprendente. 

Ogni giorno all'alba il famoso artista Ed Esor cattura lo splendore del nuovo arco in un **collage di strisce colorate**. Per risparmiare sui materiali e meglio consentirne il riciclo, Ed Esor cerca sempre di **minimizzare il numero di fogli di carta colorata** da sovrapporre nella composizione del collage, senza mai rinunciare a riprodurre fedelmente la sequenza apparsa in cielo.

Aiuta Ed Esor a minimizzare il numero di fogli impiegati nel suo collage! Se, ad esempio, l'arcobaleno fosse composto da 3 strisce di 2 colori diversi alternati, Ed Esor riuscirebbe a fare un collage usando due soli fogli di carta: uno, disposta come base, dello stesso colore delle due strisce alle estremità dell'arcobaleno, l'altro posato sul centro del primo.

### Dati di input

L'istanza del problema ha **due righe**.

La prima riga contiene solo un numero naturale ***N*** che specifica il **numero di strisce** dell'arcobaleno.
La seconda riga riporta *N* numeri interi ***C\_1*, *C\_2*, ..., *C\_N*** separati da spazio che specificano la **sequenza di colori** dell'arcobaleno odierno.

Ogni colore *C\_i* è un numero intero compreso tra **0** e **255**.
Ampie strisce uniformi nel colore sono indicate da più numeri uguali disposti consecutivamente.

### Dati di output

L'output è composto di un unico numero: il **numero minimo di strisce** per riprodurre l'arcobaleno

### Esempi di input/output

| Input                | Output     |
| -------------------- | ---------- |
| 3<br />1 2 1         | 2          |
| **Input**            | **Output** |
| 7<br />1 1 2 3 1 2 1 | 4          |

