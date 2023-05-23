# parentheses

![image](../figs/photo_2021-03-08_14-00-15.jpg)

Hai già un'idea di cosa sia una formula di parentesi ben formata: una stringa sui caratteri '(' e ')' dove è possibile stabilire un accoppiamento chiaro tra le parentesi aperte e quelle chiuse. Avremo pertanto che le chiuse sono esattamente quante le aperte, ma non solo, perchè ad esempio le seguenti non ci piacciono:

```t
)(
())(
)(()
)()(
))((
```

Invece queste sono tutte quelle ok per $n=3$:

```t
((()))
(()())
(())()
()(())
()()()
```

Se ti restano dubbi su quali formule siano ben formate, prova il servizio `check_a_sol`.

Ti invitiamo a lavorare con le mani: prova a identificare tutte quelle ok per $n=4$ oppure per $n=2$ (se hai dei dubbi o cerchi conferme sulla risposta, prova i servizi `check_num_sol` oppure `check_sol_set`).

In questo problema, che mira a sviluppare/potenziare competenze nell'approccio ricorsivo ai problemi, ti proponiamo di affrontare varie questioni come:

1. saper riconoscere se una formula di parentesi è ben formata.

2. dato $n$, saper calcolare quante sono le formule con $n$ coppie di parentesi che siano ben formate.

3. listare tutte le formule ben formate per un certo $n$.

4. ed altre questioni (come ad esempio generazione della prossima formula secondo un ordine prestabilito, ranking ed unranking, varie forme di efficienza negli algoritmi prodotti in risposta alle varie domande, ...) che incontrerai se andrai ad esplorare i servizi offerti.

Ricordiamo per altro che un problema TALight rappresenta più un percorso che non un oggetto chiuso, pertanto l'insieme dei servizi resta sempre estensibile e potremo aricchirlo anche insieme o in vostri progetti per il corso, su questioni e/o congetture che siano saltate fuori ed abbiano richiamato il nostro interesse e curiosità.    

<details>
Potresti cominciare prima affinando e poi formalizzando in codice la tua capacità di riconoscere le formule ben formate. 

Per allenarti potresti sperimentare il seguente servizio:

```
> rtal connect -a input_formula="()(()())" parentheses check_one_sol
```

La primissima questione che vorremmo tu affrontassi è

#### Dato $n$, sapresti dire quante potrebbero essere le formule benformate di $n$ coppie di parentesi?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

Puoi chiedere verifica di quale possa essere il numero di formule benformate per un certo numero di coppie $n$ attraverso chiamate del tipo:

```
> rtal connect -a n_pairs=3 -a risp=4 parentheses check_num_sol
```

Modificando alcuni parametri, ad esempio aggiungendo `-a more_or_less_hint_if_wrong`, puoi capire se la risposta che hai dato è maggiore o minore di quella esatta.

Dopo aver verificato che la logica ti torna con delle sottomissioni spot a questo servizio, od al servizio che gestisce una dialogo di domande e risposte:

```
> rtal connect parentheses eval_num_sol
```

potrai poi realizzare un tuo bot che sostenga tale dialogo in tua vece.


L'efficienza computazionale della logica risolutiva che avrai inserito al suo interno potrà così essere valutata dal seguente servizio. 
```
> rtal connect -e parentheses eval_num_sol -- python TALight/example_problems/tutorial/parentheses/bots/mybot_risp.py num_sol  
```
Quì `mybot_risp.py` potrà essere un qualsiasi eseguibile (un codice binario o anche un'interpretato) che gira sulla tua macchina.

Entro TALight puoi sempre sapere di più sui parametri e le possibilità dei servizi con

```
> rtal list parentheses -v
```

Puoi inoltre richiamare la schermata di aiuto sulle varie possibilità del comando `connect` con 

```
> rtal connect --help
```
</details>

___
Proposte successive:
vorremmo tu ti avvalessi dello stesso schema ricorsivo impiegato per affrontare il punto precedente al fine di ottenere una soluzione ricorsiva al seguente task:

#### Dato $N$, produrre la lista di tutte le possibili formule ben formate di $n$ parentesi.
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect parentheses check_sol_list
```

Potrai quindi controllare se dovresti considerare e venire a conoscere tecniche ed approcci algoritmici più efficaci (ossia asintoticamente più veloci) con:

```
> rtal connect parentheses eval_sol_list
```

Se visualizzi i possibili argomenti del servizio come insegnato sopra scoprirai che puoi scegliere tra due tipologie di ordinamento: `loves_opening_par` (fissato di default) e `loves_closing_par`. 

</details>

___
Per il listing ti proponiamo di ricercare anche un approccio iterativo:

#### *Next:* dato una formula ben formata, sapresti produrre direttamente quella che le seguirbbe nella tua lista?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect parentheses check_next_sol -a current_sol="()()()" -a next_sol="()(())" -asorting_criterion=loves_closing_par
```
Di nuovo, se visualizzi i possibili argomenti del servizio scoprirai che puoi ancora scegliere tra le stesse due tipologie di ordinamento già proposte (in questo caso è stata scelta `loves_closing_par`; se non viene specificato l'ordinamento, come visto sopra è previsto `loves_opening_par` di default). 
</details>

___
Ma per affrontare efficientemente e pur sempre in semplicità il ranking e l'unranking (combinando i quali otterresti il computo della prossima soluzione) ti suggeriamo di tornare ad un approccio ricorsivo.

#### *Ranking:* dato una formula ben formata, sapresti dire in che posizione si colloca entro la tua lista senza percorrerla?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>
  
Ormai saprai cercare da solo, avvalendoti di comandi quali ` > rtal list parentheses -v ` i servizi offerti e relativi parametri. Questo vale anche per altri problemi entro TALight: ove un esplorazione diretta dei servizi, magari corroborata da un paio di interazioni di prova al terminale non sia sufficiente, forniamo allora un ulteriore servizio di help

```
> rtal list help
```

che ha come parametri la specifica di eventuali pagine di aiuto, tipicamente dedicate ai servizi del problema che possano beneficiarne. 

</details>

___
#### *Unranking:* dato $n$ ed un numero naturale positivo $i$, sapresti produrre direttamente la formula ben formata che nella tua lista compare in posizione $i$?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>
  
Ormai sarai autonomo nel raccogliere le possibilità offerte.

</details>

</details>
