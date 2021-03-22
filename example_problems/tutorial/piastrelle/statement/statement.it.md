# piastrelle

![image](../figs/.jpg)

Pippo ha un corridoio di dimensione $1 \times N$ da piastellare. Lui ha a disposizione solo piastrelle di dimensioni $1 \times 1$ e $1 \times 2$. Essendo questo il corridoio dell'ingresso di casa sua, lui vorrebbe che fosse il più bello possibile, quindi ha bisogno di conoscere tutte le possibili disposizioni delle piastrelle che potrebbe usare per completare il lavoro.
Qusti sarebbero i possibili modi di piastrellare il bagno quando $N=4$.

```t
[][][][]
[][][--]
[][--][]
[--][][]
[--][--]
```

Se ti restano dubbi su cosa sia una piastrellatura valida e di come abbiamo stabilito di rappresentarla, prova il servizio `check_one_sol`.

Ti invitiamo a lavorare con le mani: prova a identificare tutte le piastrellature possibili per $N=5$ oppure per $N=3$ o $N=2$ (se hai dei dubbi o cerchi conferme sulla risposta, prova i servizi `check_num_sol` oppure `check_sol_set`).

In questo problema, che mira a sviluppare/potenziare competenze nell'approccio ricorsivo ai problemi, ti proponiamo di affrontare varie questioni come:

1. saper riconoscere se una piastrellatura è ben formata.

2. dato $N$, saper calcolare in quanti modi può essere piastrellato un corridoio di dimensione $1 \times N$.

3. listare tutte le piastrellature ben formate per un certo $N$.

4. ed altre questioni (come ad esempio generazione della prossima piastrellatura secondo un ordine prestabilito, ranking ed unranking, varie forme di efficienza negli algoritmi prodotti in risposta alle varie domande, ...) che incontrerai se andrai ad esplorare i servizi offerti.

Ricordiamo per altro che un problema TALight rappresenta più un percorso che non un oggetto chiuso, pertanto l'insieme dei servizi resta sempre estensibile e potremo aricchirlo anche insieme o in vostri progetti per il corso, su questioni e/o congetture che siano saltate fuori ed abbiano richiamato il nostro interesse e curiosità.    

<details>
Potresti cominciare prima affinando e poi formalizzando in codice la tua capacità di riconoscere le piastrellature ben formate. 

Per allenarti potresti sperimentare il seguente servizio:

```
> rtal connect -a input_formula="[][--]" piastrelle check_one_sol
```

La primissima questione che vorremmo tu affrontassi è

#### Dato $N$, sapresti dire quante potrebbero essere le piastrellature ben formate?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

Puoi chiedere verifica di quale possa essere il numero di piastrellature ben formate per un certo corridoio $1 \times N$ attraverso chiamate del tipo:

```
> rtal connect -a num_pairs=4 -a risp=5  piastrelle check_num_sol
```

Dopo aver verificato che la logica ti torna con delle sottomissioni spot a questo servizio, od al servizio che gestisce una dialogo di domande e risposte:

```
> rtal connect piastrelle evaluate_num_sol
```

potrai poi realizzare un tuo bot che sostenga tale dialogo in tua vece.


L'efficienza computazionale della logica risolutiva che avrai inserito al suo interno potrà così essere valutata dal seguente servizio. 
```
> rtal connect piastrelle evaluate_num_sol -- python mybot_risp.py
```
Quì `mybot_risp.py` potrà essere un qualsiasi eseguibile (un codice binario o anche un'interpretato) che gira sulla tua macchina.

Entro TAlight puoi sempre sapere di più sui parametri e le possibilità dei servizi con

```
> rtal list piastrelle -v
```

Puoi inoltre richiamare la schermata di aiuto sulle varie possibilità del comando `connect` con 

```
> rtal connect --help
```
</details>

___
Proposte successive:
vorremmo tu ti avvalessi dello stesso schema ricorsivo impiegato per affrontare il punto precedente al fine di ottenere una soluzione ricorsiva al seguente task:

#### Dato $N$, produrre la lista di tutte le possibili piastrellature ben formate per un corridoio $1 \times N$.
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a num_pairs=4 -a=spot_wrong_consec_if_sorted piastrelle check_sol_list
```

Potrai quindi controllare se dovresti considerare e venire a conoscere tecniche ed approcci algoritmici più efficaci (ossia asintoticamente più veloci) con:

```
> rtal connect piastrelle evaluate_sol_list
```

Se visualizzi i possibili argomenti del servizio come insegnato sopra scoprirai che puoi scegliere tra due tipologie di ordinamento naturale sostanzialmente diversi (nota che non sono uno l'inverso dell'altro). 

</details>

___
Per il listing ti proponiamo di ricercare anche un approccio iterativo:

#### *Next:* dato una piastrellatura ben formata, sapresti produrre direttamente quella che le seguirbbe nella tua lista?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a current_sol=[][][--] -a next_sol=[][--][] piastrelle check_nextcheck_next_sol_gen
```
Di nuovo, se visualizzi i possibili argomenti del servizio scoprirai che puoi ancora scegliere tra le stesse due tipologie di ordinamento già proposte. 
</details>

___
Ma per affrontare efficientemente e pur sempre in semplicità il ranking e l'unranking (combinando i quali otterresti il computo della prossima soluzione) ti suggeriamo di tornare ad un approccio ricorsivo.

#### *Ranking:* dato una piastrellatura ben formata, sapresti dire in che posizione si colloca entro la tua lista senza percorrerla?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>
Ormai saprai cercare da solo, avvalendoti di comandi quali

```
> rtal list piastrelle -v
```
i servizi offerti e relativi parametri. Questo vale anche per altri problemi entro TALight: ove un esplorazione diretta dei servizi, magari corroborata da un paio di interazioni di prova al terminale non sia sufficiente, forniamo allora un ulteriore servizio di help
```
> rtal list help
```
che ha come parametri la specifica di eventuali pagine di aiuto, tipicamente dedicate ai servizi del problema che possano beneficiarne. 

</details>

___
#### *Unranking:* dato $N$ ed un numero naturale positivo $i$, sapresti produrre direttamente la piastrellatura ben formata che nella tua lista compare in posizione $i$?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>
Ormai sarai autonomo nel raccogliere le possibilità offerte.
</details>

</details>
