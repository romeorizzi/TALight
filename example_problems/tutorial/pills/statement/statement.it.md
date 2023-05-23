# pills

![image](../figs/pills.jpeg)


Zia Lucilla deve assumere ogni giorno mezza pillola di una certa medicina. Lei inizia il trattamento con una bottiglia che contiene $N$ pillole.
La sera del primo giorno, zietta prende una pillola dalla bottiglia, la spezza in due e ne ingerisce una delle due metà rimettendo l’altra nella bottiglia.
Le sere successive, prende un pezzo a caso della bottiglia (potrebbe essere una pillola intera o una mezza pillola). Se ha pescato una mezza pillola la ingerisce. Se ha pescato una pillola intera la spezza a metà, rimette una delle due mezze pillole nella bottiglia e ingerisce l’altra metà.
Lucilla può quindi svuotare il flacone in tanti modi diversi. Rappresentiamo il trattamento come una stringa il cui carattere $i$-esimo è 'I' se la sera del giorno $i$-esimo zietta ha pescato una pillola intera, oppure 'H' altrimenti.
Ad esempio, del caso la bottiglia originariamente contenga $N=3$ pillole, allora le possibili sequenze sono le seguenti:
```t
IIIHHH
IIHIHH
IIHHIH
IHIIHH
IHIHIH
```
La primissima questione che vorremmo tu affrontassi è

#### Dato $N$, sapresti dire quanti potrebbero essere i modi diversi di condurre il trattamento?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

Puoi chiedere verifica di quale possa essere il numero di trattamenti per un certo $N$ attraverso chiamate del tipo:

```
> rtal connect -a num_pills=3 -a risp=4 pills check_num_sol
```

Dopo aver verificato che la logica ti torna con delle sottomissioni spot a questo servizio, potrai realizzare un tuo bot che sostenga un dialogo di domande e risposte. L'efficienza computazionale della logica risolutiva che avrai inserito al suo interno potrà così essere valutata dal seguente servizio. Per comprendere il protocollo prova prima a sostenere tu stesso dei dialoghi anche di un solo paio di domande:

```
> rtal connect pills evaluate_num_sol
```
e poi chiama lo stesso servizio come segue per ridirigere il dialogo sul tuo bot ed ottenerne validazione e valutazione delle performance:

```
> rtal connect pills evaluate_num_sol -a mybot_risp.py
```
Quì `mybot_risp.py` potrà essere un qualsiasi eseguibile (un codice binario o anche un'interpretato) che gira sulla tua macchina.

Entro TALight puoi sempre sapere di più sui parametri e le possibilità dei servizi con

```
> rtal list pills -v
```

Puoi inoltre richiamare la schermata di aiuto sulle varie possibilità del comando `connect` con 

```
> rtal connect --help
```
</details>

___
Proposte successive:
vorremmo tu ti avvalessi dello stesso schema ricorsivo impiegato per affrontare il punto precedente al fine di ottenere una soluzione ricorsiva al seguente task:

#### Dato $N$, produrre la lista di tutti i possibili modi di svuotare un flacone di $N$ pillole.
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a num_pills=3 -a=spot_wrong_consec_if_sorted pills check_sol_list
```

Potrai quindi controllare se dovresti considerare e venire a conoscere tecniche ed approcci algoritmici più efficaci (ossia asintoticamente più veloci) con:

```
> rtal connect pills evaluate_sol_list
```

Se visualizzi i possibili argomenti del servizio come insegnato sopra scoprirai che puoi scegliere tra due tipologie di ordinamento naturale sostanzialmente diversi (nota che non sono uno l'inverso dell'altro). 

</details>

___
Per il listing ti proponiamo di ricercare anche un approccio iterativo:

#### *Next:* dato un trattamento, sapresti produrre direttamente il prossimo trattamento nella tua lista?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a current_sol=IIHIHH -a next_sol=IIHHIH pills check_nextcheck_next_sol_gen
```
Di nuovo, se visualizzi i possibili argomenti del servizio scoprirai che puoi ancora scegliere tra le stesse due tipologie di ordinamento già proposte. 
</details>

___
Ma per affrontare efficientemente e pur sempre in semplicità il ranking e l'unranking (combinando i quali otterresti il computo della prossima soluzione) ti suggeriamo di tornare ad un approccio ricorsivo.

#### *Ranking:* dato un trattamento, sapresti dire in che posizione si colloca entro la tua lista senza percorrerla?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>
Ormai saprai cercare da solo, avvalendoti di comandi quali
```
> rtal list pills -v
```
i servizi offerti e relativi parametri. Questo vale anche per altri problemi entro TALight: ove un esplorazione diretta dei servizi, magari corroborata da un paio di interazioni di prova al terminale non sia sufficiente, forniamo allora un ulteriore servizio di help
```
> rtal list help
```
che ha come parametri la specifica di eventuali pagine di aiuto, tipicamente dedicate ai servizi del problema che possano beneficiarne. 

</details>

___
#### *Unranking:* dato $N$ ed un $i$, sapresti produrre direttamente il trattamento $i$-esimo nella tua lista?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>
Ormai sarai autonomo nel raccogliere le possibilità offerte.
</details>

