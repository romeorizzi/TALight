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

```
> rtal connect -a num_pills=3 -a risp=4 pills check_risp
```

Dopo aver verificato che la logica ti torna con delle sottomissioni spot a questo servizio, potrai realizzare un tuo bot che sostenga un dialogo di domande e risposte al seguente servizio. Per comprendere il protocollo prova prima a sostenere tu stesso dei dialoghi:

```
> rtal connect pills score_risp
```
e poi chiama lo stesso servizio come segue per ridirigere il dialogo sul tuo bot ed ottenerne validazione e valutazione delle performance:

```
> rtal connect pills score_risp -a mybot_risp.py
```
Quì `mybot_risp.py` potrà essere un qualsiasi eseguibile (un codice binario o anche un'interpretato) che gira sulla tua macchina.

Entro TAlight puoi sempre sapere di più sui parametri e le possibilità dei servizi con

```
> rtal list pills -v
```

Puoi inoltre richiamare la schermata di aiuto sulle varie possibilità del comando `connect` con 

```
> rtal connect --help
```
</details>

___
Successivamente, vorremmo tu ti avvalessi dello stesso schema ricorsivo che hai utilizzato per affrontare il punto precedente al fine di

#### Dato $N$, produrre la lista di tutti i possibili modi di svuotare un flacone di $N$ pillole.
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a num_pills=3 -a=spot_wrong_consec_if_sorted pills check_list
```

```
> rtal connect -a num_pills=3 pills score_list
```

</details>

___
Proposte successive:

#### *Next:* dato un trattamento, sapresti produrre direttamente il prossimo trattamento nella tua lista?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a current_sol=IIHIH -a next_sol=IIHHI pills check_next
```
```
> rtal connect -a sorting_criterion=dislike_integer_pills pills score_next
```
</details>

___
#### *Ranking:* dato un trattamento, sapresti dire in che posizione si colloca entro la tua lista senza percorrerla?
<details>
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a num_pills=3 -a risp=4 pills check_risp
```
</details>

___
<details>
#### *Unranking:* dato $N$ ed un $i$, sapresti produrre direttamente il trattamento $i$-esimo nella tua lista?
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect -a num_pills=3 -a risp=4 pills check_risp
```
</details>

___
<details>
#### *Recognizing:* data una stringa sull'alfabeto $\{H,I\}$, sapresti riconoscere se essa codifica un possibile trattamento (per un qualche $N$)?
<summary><strong>Servizi offerti</strong></summary>
<H4>Servizi offerti</H4>

```
> rtal connect pills recognize
```
</details>
