1. Consentire di effettuare l'esplorazione a livello di singolo servizio di un problema. 

Esempio:
INPUT:
> rtal/target/debug/rtal list sum sum_and_difference -v
OUTPUT:
- sum
  * sum_and_difference
    # numbers [onedigit] { ^(onedigit|twodigits|big)$ }
    # lang [it] { ^(en|it)$ }

2. del servizio offrire su richiesta (con specifica della lingua) anche una descrizione semantica. Tale descrizione semantica si trova nel file nomeservizio-en.md se in inglese, nel file nomeservizio-it.md se in italiano che, ove presenti, potrebbero anche essi trovarsi nella cartella att come i testi nelle varie lingue.

3. Al momento rtald rileva nuovi problemi o nuove versioni di problema come immessi (plug-and-play a caldo). Questo va bene anche se in parte sacrificabile:
andrebbe bene anche dover ricorrere a dei comandi di load (=reload) di un problema se questo dovesse essere necessario per sveltire le risposte del server ed alleggerirne il carico. Questo anche in considerazione del punto successivo. 

4. A mè farebbe piacere avere diverse decine di problemi indirizate da centinaia di nomi diversi (con nomi che emulano una navigazione in una tassonomia). 
L'organizzazione ad albero delle risore (in realtà a DAG con unica sorgente se si possono impiegare anche i simlink) renderebbe più facile scoprire ed accedere ai vari problemi accorpati per categorie e sotto-percorsi, guidando più efficacemente lo studente nella sua esplorazion autonoma.

5. Per altro su questo DAG io vagheggiavo di poter introdurre dei meccanismi di sblocco di livelli come nei videogiochi (per competenze a prerequisito).


