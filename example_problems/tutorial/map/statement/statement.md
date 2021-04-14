# Mappa Antica

preso dalle Selezioni territoriali OII, 2008


## Descrizione del problema

Topolino è in missione per accompagnare una spedizione archeologica che richiede il superamento di diverse difficoltà tra cui l'attraversamento di un pericoloso labirinto con trappole mortali dislocate come raffigurato in un'antica mappa ritrovata presso il museo di Topolinia:

<style type="text/css">
<!---  body {
    color: purple; -->
    background-color: #d8da3d }
  td.celle {
    width: 56px;
    height: 56px;
    align="center";
  }
</style>
<table>
<tr align="center">
<td class="celle"><IMG SRC="figs/stone3.jpeg" width="70%" height="60%"></td><td class="celle"><b>1</td><td class="celle"><b>2</td><td class="celle"><b>3</td><td class="celle"><b>4</td><td class="celle"><b>5</td>
</tr>

<tr>
<td class="celle"><b>1&nbsp;</td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td>
</tr>

<tr>
<td class="celle"><b>2&nbsp;</td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td>
</tr>

<tr>
<td class="celle"><b>3&nbsp;</td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td>
</tr>

<tr>
<td class="celle"><b>4&nbsp;</td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td>
</tr>

<tr>
<td class="celle"><b>5&nbsp;</td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="58%"></td><td class="celle"><IMG SRC="figs/fire1.gif" width="100%" height="106%"></td><td class="celle"><IMG SRC="figs/stone1.jpeg" width="92%" height="106%"></td>
</tr>

<table>


Il labirinto ha la forma di una gigantesca scacchiera quadrata di NxN lastroni di pietra alcuni dei quali sono da evitare in quanto ricoperti di lava o altre trappole mortali.

Topolino deve partire dal lastrone (1,1) in alto a sinistra e raggiungere il lastrone (N,N) in basso a destra; li assumiamo essere entrambi liberi. Per fare questo può passare di lastrone in lastrone, ma solo se questi condividono un lato o uno spigolo (quindi può procedere in direzione orizzontale, verticale o diagonale ma non saltare). Ovviamente, tutti i lastroni visitati da Topolino nel suo percorso dovranno essere liberi da impedimenti.

Il labirinto resta comunque un luogo pericoloso e pieno di insidie e pertanto Topolino intende calpestare il minor numero possibile di lastroni (tutti comunque liberi). Aiutate Topolino a calcolare tale numero minimo e a trovare un percorso ottimo.

## Assunzioni

* $1 \le N \le 100$
* righe e colonne sono numerate da $1$ a $N$


## Goals:

*  Goal 1: caso di esempio
*  Goal 2: non vi è alcuna trappola mortale
*  Goal 3: $2\leq N \leq 5$
*  Goal 4: $N = 10$
*  Goal 5: $N = 20$
*  Goal 6: $N = 30$
*  Goal 7: $N = 50$
*  Goal 8: $N = 100$


## Servizi di supporto alla valutazione di un tuo modello contenuto in un file `.mod`

Forniamo diversi testcase di dimensioni diverse. Supportiamo due diversi formati per il file di input:

1. il formato `.txt` adottato nella gara territoriale delle OII;

2. un formato `.dat` che proponiamo qui per evitarti un lavoro di riscrittura delle istanze. Il formato di tale file `.dat` (un file di testo semplice, ASCI) è esemplificato nel file [input_1.dat](input_1.dat) dove trovi codifica della mappa vista sopra.

Tali codifiche per l'esempio del testo (la mappa vista sopra) sono riportate in fondo al presente documento.

## Servizi TALight

1. Valutazione di una coppia (istanza,soluzione). In particolare: correttezza della soluzione, ottimalità della soluzione.

2. Dialogo dove TALight aggiunge delle trappole una alla volta ed un tuo bot tiene aggiornato il valore dell'ottimo ma anche comunica, sempre ad ogni iterazione, quali sono quelle celle dove l'aggiunta di una trappola aumenterebbe di 1 la distanza o renderebbe il problema inammissibile.


## Formati per i file in gioco

Secondo i formati per l'input e l'output come originariamente proposti in sede della Selezione territoriale OII 2008, l'istanza del testo avrebbe comportato i seguenti file:

| `input.txt` | `output.txt` | 
|---|---|
|5     |5|
|***+* | |
|+**++ | |
|*+*+* | |
|+++*+ | |
|+**+* | |

Noi preferiamo tuttavia lavorare coi seguenti 3 file

| `input.txt` | `output.txt` | `opt_sol.txt` ("output esteso") | 
|---|---|
|5         |5|5|
|0 0 0 1 0 | |1 1 |
|1 0 0 1 1 | |2 2 |
|0 1 0 1 0 | |3 3 |
|1 1 1 0 1 | |4 4 |
|1 0 0 1 0 | |5 5 |

### File input.txt

Il nuovo formato è più conveniente perché facilita il parsing del file. In particolare, leggendo interi invece che caratteri si eviteranno problemi coi caratteri di fine linea o spuri.

### File output.txt

La risposta alla domanda originale (in questo caso $5$) va scritta nel file ASCII di nome `output.txt` dove si stampa il minimo numero di lastroni (devono essere tutti rigorosamente innocui, ossia indicati con '0') che Topolino deve attraversare a partire dal lastrone in posizione $(1, 1)$ per arrivare incolume al lastrone in posizione $(N, N)$. Notare che i lastroni $(1, 1)$ e $(N, N)$ vanno inclusi nel conteggio dei lastroni attraversati.

Il file `.mod` da te sottomesso alla valutazione deve prescrivere che tale risposta venga scritta entro il file `output.txt` posto nella cartella corrente. Il file, di una sola riga, deve contenere solo tale numero (un numero naturale).


### File opt_sol.txt

L'output esteso è inteso a codificare un percorso ottimo. (Si noti che `output.txt` è la sola prima riga di `opt_sol.txt`.) Quando produrrai un'output esteso potrai più facilmente prendere verifiche sui tuoi modelli e soluzioni. Ad esempio, quando lanci lo script `check_feasibility.py` (o richiedi l'omonimo servizio TALight dal cloud) su una coppia (input, output esteso) esso potrà confermarti che il percorso da tè computato è quantomeno ammissibile, o segnalarti e chiarire ogni problema in caso contrario. Per avere verifica dell'ottimalità sul set di istanze che abbiamo reso disponibili ti basterà confrontare l'output non-esteso (ovvero la sola prima riga dell'output esteso) con quello di riferimento. Abbiamo predisposto degli script che effettuano la generazione di tutti gli output a partire dal tuo modello, o che confrontano tutti i tuoi output non estesi con quelli di riferimento, o verificano l'ammissibilità di quelli estesi, o il complesso di queste varie cose anche in dipendenza dai formati prescelti.
Puoi altresì chiamare i servizi TALight nel cloud per ottenere validazioni e feedback più approfonditi o su insiemi più estesi di istanze.

L'intera suite dei testcase in formato `.txt` è scaricabile [da questo link](testcases.zip). Potrai quindi lavorare in locale, individuare eventuali errori o consentire i tempi che vorrai alle tue soluzioni, oppure provare in locale le tue soluzioni in GMPL/AMPL od altri formati o sistemi. Ogni testcase di questa suite è compiutamente descritto da una tripla di file (input.txt/output.txt/opt_sol.txt). Ad esempio, a fianco del file `input_1.txt` visto sopra trovi anche il file `output_1.txt` che ne contiene la soluzione di riferimento e il file `opt_sol_1.txt` che può venirti utile per consultazione anche se, ovviamente, il più delle volte il percorso ottimo non sarà unico.

Se in locale vuoi sperimentare con ulteriori (o anche più grosse) istanze che non come da assunzioni sopra, la miglior opzione è avvalersi dei servizi TALight. Altrimenti scaricati [queste](testcases-extra.zip).


### Formato di file `.dat` che proponiamo e supportiamo

E'specificato in un documento a parte poiché a seconda degli obiettivi didattici tuoi o del tuo docente di riferimento il progetto del `.dat` file potrebbe voler essere parte del percorso, o magari invece si preferisce rendervi accessibili delle utility già pronte per la transcodifica delle istanze. In questo caso potrai concentrarti sulla realizzazione del solo file `.mod` col modello e così sia la realizzazione del modello che il suo testing (sia in locale che nel cloud) dovrebbe venirti più pratico e veloce.


### La gallery dei modelli

Quando i tempi saranno maturi troverai delle soluzioni più o meno performanti discusse [quì](gallery_of_models.zip). Evita di consultarle troppo presto per non spoilerarti il problema.

### Altri formati e maggiori info sugli script

Prevediamo di supportare anche il formato ODS (OpenDocument Spreadsheet) sia per l'input che per l'output.


Forniamo inoltre vari script che possono aiutarti nel compiere di tali transcodifiche delle istanze. Abbiamo cercato di comporli con un occhio alla loro modificabilità. In particolare: del caso tu decida di stabilire un altro formato per i tuoi file di input dovrebbe esserti facile adattare questi script.

Forniamo inoltre un generatore di istanze a partire da un seed ed alcuni parametri ($N$).

Forniamo inoltre uno script che prenda in input un vostro file `.gmpl` o `.ampl` contenente un vostro modello da valutare e lo confronti sulle varie istanze per validarne correttezza ed efficienza. Lo script intende esprimere un feedback molto puntuale. In particolare, per la correttezza valuteremo l'ammissibilità delle tue soluzioni ma ti faremo anche sapere se esse sono ottime. In funzione dell'efficienza stimata per la tua soluzione potremo anche consigliarti approcci più potenti.
Ma in linea di massima lo script opera quanto segue: per ogni possibile testcase, lo script invoca i software che possano interpretare il vostro modello. Assumiamo quindi che tali software siano correttamente installati sulla tua macchina. Pertanto, anche senza lanciare lo script, assumiamo che ti sia sempre possibile testare direttamente il tuo modello su singole istanze; il nostro script si propone solo di orchestrare la sperimentazione e aiutarti nel tirare le somme.

Se il tuo modello è contenuto in un file `.gmpl` lo script invocherà il solver opensource `gplsol` utilizzando l'opzione `-m` per passargli il file `.gmpl` da voi sottomesso e l'opzione `-d` per passargli il file `.dat` dell'istanza. Le varie istanze saranno affrontate una alla volta in chiamate diverse tutte orchestrate da un'unica chiamata allo script.

Se il tuo modello è contenuto in un file `.ampl` lo script invocherà il software commerciale `ampl` per ottenere direttamente una soluzione oppure una istanziazione del vostro modello astratto in un modello di PL o PLI concreto che incorpora la singola istanza. Nel secondo caso sarete di nuovo liberi di scegliere il solver per il modello di PL o di PLI ottenuto.
In ogni caso la configurazione deve essere tale da produrre un file `output.txt` come da formato richiesto.
