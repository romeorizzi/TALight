# Ti convinco che due grafi sono isomorfi senza nulla svelare

E' possibile convincere qualcuno di qualcosa senza in alcun modo svelare nemmeno parzialmente perchè quella cosa è vera?
Con le zero-knowledge proofs abbiamo scoperto che questo è vero nel senso più estremo (non sveleremo nemmeno un bit di informazione al proposito!) e questo ci offre la possibilità di dimostrare la nostra identità senza che chi, anche ci ascoltasse nella nostra interazione, non acquisirebbe nulla della capacità da noi esibita nel far aprire il sesamo. Nemmeno Ali Babà.

Ecco un giochetto simpatico che mostra come ciò possa essere fatto. Utilizzeremo il problema del graph isomorphism, per il quale a tutt'oggi non è noto alcun algoritmo polinomiale.

INPUT: due grafi $G_1$ e $G_2$.
TASK: stabilire che $G_1$ e $G_2$ non sono isomorfi oppure produrre un certificato del loro isomorfismo nella forma di una biezione $f: V(G_1) \mapsto V(G_2)$ tale che $uv$ è un arco di $G_1$ se e solo se $f(u)f(v)$ è un arco di $G_2$.

Ovviamente una condizion necessaria affinchè $G_1$ e $G_2$ siano isomorfi è che $|V(G_1)|=|V(G_2)|$. Essendo solo una questione di rinominare etichette, assumeremo poi che $V(G_1)={1,2,\ldots , n}=V(G_2) =: V$.

Supponiamo di sapere bene che due grafi $G_1$ e $G_2$ sono isomorfi, nel senso di essere a conoscnza di una biezione $f: V \mapsto V$ certificante il loro isomorfismo. Una biezione $f: V \mapsto V$ è anche detta una permutazione su $V$.

Possiamo convincere lo scettico Re Artù del fatto che $G_1$ e $G_2$ sono isomorfi, oppure il sesamo del fatto che noi siamo a conoscenza del segreto dell'isomorfismo tra $G_1$ e $G_2$, confrontandoci con tale intrlocutore lungo un dialogo sequenziato in round di verifica.
I round di verifica sono indipendenti ed a ciascuno di essi l'interlocutore ha probabilità almeno 1/2 di sgamare il mio imboroglio se sono un millantatore (se invece sono davvero in possesso di una tale $f$ tale probabilità sarà invece nulla, ovviamente). Dopo $k$ fasi, la probabilità che un millantatore non venga sgamato è al più $1/2^k$, ossia praticamente nulla già per $k$ molto piccolo (più probabile essere colpiti da un astroide in pieno giorno o che l'interferenza quantistica della mia presenza di fronte al PC gli faccia commettere un errore di valutazione).

Ecco il protocollo di un singolo round:

L> sceglie un permutazione casuale $\pi$ di $V$ e invia al server S il grafo $G_3 = (V,E)$ con $E=\{\pi(u)\pi(u) : uv\in E(G_1)\}$ (è importante che $\pi$ venga scelta secondo distribuzione uniforme ed indipendentemente che in altri round per non cedere info sul segreto di L all'interlocutore S o a colui che stesse origliando sul canale)
S> sceglie a caso un numero in $\{1,2\}$, secondo distribuzione uniforme ed indipendente da altri round. Comunica tale numero $p$ ad L con la richiesta di offrirgli certificato che $G_3$ è isomorfo a $G_p$. 
L> se $p=1$ allora L invia a S la permutazione $\pi$, altrimenti invia ad $S$ la permutazione composta $f(\pi^{-1})$.
S> sia $\sigma$ la permutazione ricvuta da L. Allora S verifica che $E(G_3)=\{\sigma(u)\sigma(u) : uv\in E(G_p)\}$. Se ogni singolo arco passa il check il round di verifica è intso come superato da L, altrimenti S ha sgamato un millantatore.

##Servizi offerti:

```t
> TALight verify_a_G1_G2_f_triple my_private_secret.txt
```

Verifica che $f$ è un isomorfismo tra $G_1$ e $G_2$.
Fornisce inoltre una valutazione su quanto possa essere difficile ricostruire $f$ dalla sola conoscenza di $G_1$ e $G_2$.

```t
> TALight claim_G1_G2_are_iso G1_G2.txt my_Ali --k=10
```

Per verificare che il proprio eseguibile my_Ali correttamente implementa il protocollo visto sopra per convincere il server S di essere a conoscenza dell'isomorfismo dei due grafi $G_1$ e $G_2$ contenuti nel file G1_G2.txt. Per $k$ piccolo puoi sperare di convincere il server anche con una coppia di grafi $G_1$ e $G_2$ che in realtà isomorfi non sono.

## Per sapere di più
[Interactive proof system](https://en.wikipedia.org/wiki/Interactive_proof_system)

Per tutti i problmi in NP (anche quelli NP completi) è possibile, partendo dall'ipotesi di esistenza di one-way functions su cui poggia la crittografia, fornire un protocollo di zero-knowledge proof.


## Possibili progetti

Realizzazione di problemi simpatici su questo versante.

