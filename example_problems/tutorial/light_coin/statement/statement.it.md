# Individuare la Moneta Leggera (light_coin)

## Descrizione del problema

Vuoi individuare l'unica moneta falsa in un set di $7$ monete numerate da $1$ ad $7$. Puoi avvalerti in questo di una bilancia a braccia uguali.
Questo puzzle classico assume che la moneta falsa abbia un peso diverso delle altre. (Ci sono 2 varianti: sappiamo anche se la moneta è più leggera o pesante, oppure, nella variante più interessante, si sà solo che ha peso diverso.)
Organizzare una pesata significa specificare i due sottoinsiemi disgiunti di monete da collocare sui due piatti della bilancia. Ad esempio, immettendo:

[1, 5, 6], [2, 4]

richiedi una pesata con le monete $1$, $5$, e $6$ sul piatto sinistro e $2, 4$ su quello destro. 

La misura potrà avere uno dei seguenti 3 esiti:

- **NONE:** se i due piatti della bilancia sono in perfetto equilibrio (nessuno dei due scende in basso);

- **LEFT:** se il carico è maggiore sul piatto sinistro;

- **RIGHT:** se il carico è maggiore sul piatto destro.

## Estensibilità ever green del problema

Attorno a questo puzzle potrai condurre delle tue esplorazioni, al momento possiamo proporre i seguenti percorsi:

1. distinzione tra strategie _statiche_ (dove l'insieme delle misure da compiere viene fissato a priori) e _dinamiche_ (dove ogni atto di misura viene stabilito prendendo in considerazione gli esiti delle pesate già fatte);

2. ricerca della natura ricorsiva del problema chiedendosi come possa essere stabilita una buna strategia di gioco per un numero di monete $n$ generico.

Se il problema ti incuriosisce anche in altri modi e ti poni altre questioni intriganti, puoi porti la sfida di realizzare tu stesso dei servizi che stimolino e supportino il problem solver guidandolo sui terreni da tè esplorati. Sarà molto stimolante e formativo, nonché divertente, riscoprirti nel ruolo di problem maker ([brake on through to the other side](https://www.youtube.com/watch?v=-r679Hhs9Zs)).



## Supporti alla programmazione, interfacce grafiche, o avanguardia

Oltre che giocare tu stesso prescrivendo le tue pesate da riga di comando con:

```bash
rtal connect light_coin check_dynamic_strategy
```

puoi divertirti ad istruire un bot affinché giochi in tua vece con:

```bash
rtal connect light_coin check_dynamic_strategy -- python mybot.py
```

Il bot può essere scritto in un qualsiasi altro linguaggio, e, se è un compilato, non ti sarà necessario richiamare l'interprete:

```bash
rtal connect light_coin check_dynamic_strategy -- mybot
```

Ovviamente il file `mybot` sarà il file col codice binario prodotto con la compilazione, coi necessari diritti di esecuzione settati.  

Se vuoi concentrarti sugli aspetti alti del problema e trascurare i dettagli della programmazione, puoi prendere il bot contenitore già predisposto da noi per il tuo linguaggio. Esso prenderà cura della gestione dell'input e output secondo il protocollo di gioco e potrai così limitarti a specificare l'implementazione delle funzioni che esprimono al nocciolo la logica del gioco. Ad esempio in python potrai limitarti ad implementare la funzione `individua()` nel modulo `logic.py` e da `individua()` potrai chiamare il comando/funzione: 

```
risp = piatto_con_peso_maggiore(left=[1, 5, 6], right=[2, 4])
```

Quando poi sei sicuro su quale sia la moneta falsa dovrai consegnarla alla zecca invocando:
```
denuncia(monetaFalsa)
```
per concludere con successo la partita.

E'inoltre possibile giocare entro un applet grafico (adatto per le medie) oppure in un ambiente ibrido dove ti sono consentiti varie possibilità per collocare ogni tua interazione e, ad esempio, se compi una tua mossa col mouse puoi ottenerne visualizzazione/traduzione a vari livelli diversi del protocollo di gioco.

## Servizi di tipo eval (per ottenere un feedback anche sul piano dei metodi e delle tecniche di problem solving)


### Possibili goals per la strategia dinamica

- Il programma termina dopo la prima chiamata alla funzione denuncia oppure allo scadere del tempo limite.

- $1 <= n <= 1,000,000$

## Obbiettivi

1. Trovare la moneta falsa (correttezza).

2. Trovare la moneta falsa tra $7$ monete ($n = 7$) con al massimo $6$ pesate.

3. Trovare la moneta falsa tra $7$ monete ($n = 7$) con al massimo $4$ pesate.

4. Trovare la moneta falsa tra $7$ monete ($n = 7$) con al massimo $3$ pesate.

5. Trovare la moneta falsa tra $8$ monete ($n = 8$) con al massimo $3$ pesate.

6. Trovare la moneta falsa con al più $n - 1$ pesate.

7. Trovare la moneta falsa con al più $\lfloor n/2 \rfloor$ pesate.

8. Trovare la moneta falsa con al più $\lfloor log_2 n \rfloor$ pesate. Ti è possibile migliorare su questo in termini di costante moltiplicativa? 

9. Viene permesso solo quel minimo numero di pesate che, se impiegato, sapientemente, consenta sempre di individuare la moneta falsa.

10. Esibire con un cambio di ruolo (tu ora giochi nel ruolo della bilancia) che non è possibile ridurre ulteriormente tale numero.

## Esempio di investigazioni ever green: di quante pesate hai bisogno se vuoi solo stabilire se la moneta falsa sia più leggera oppure più pesante?

Osservazione 1: $n \geq 3$, altrimenti non è possibile stabilire quale sia quella falsa.

Osservazione 2: non sarà mai possibile concludere nulla da una sola pesata.

Quale è il minimo numero di pesate per una strategia dinamica? Sai giocarla? (Prova il servizio ...). 

Quale è il minimo numero di pesate per una strategia statica? Sai giocarla? (Prova il servizio ...).

Per quei valori di $n$ dove la tua strategia statica richieda più di $2$ pesate, cerca di dimostrare che non esiste una strategia con meno pesate della tua:
    prova costruendo un algoritmo che, dato un qualunque set con meno pesate, offra due risposte e due verità compatibili con esse (una verità con moneta falsa leggere e l'altra verità con moneta falsa pesante). Questo potrebbe aiutarti a contestualizzare il problema. Ed è supportato dal nostro servizio

```bash
rtal connect light_coin empass_static_strategy_lighter_or_heavier -- mybot
```


<!---
    strategia dinamica in 2 pesate:
        n=3k+r con r=1,2.
        1. confronta A contro B con |A|=|B|=k
        2. se A = B la falsa è tra le k+r rimanenti:
            le confronti contro k+r monete prese da A \cup B
           altrimenti:
               per stabilire se la falsa è in A o in B confronti A contro k delle rimanenti.
    strategia statica di 2 pesate quando r=0:
      si partizioni in A,B,C con |A|=|B|=|C|=k.
      1. A versus B
      2. A versus C
    strategia dinamica di 3 pesate quando r=1,2:
      applico la strategia statica di 2 pesate alle prime 3k monete
      se almeno una pesata sbilancia, allora la falsa è tra queste prime 3k monete e quindi l 2 psate bastano a determinare la verità.
      Altrimenti la falsa è tra le r monete rimanenti, che confronto (staticamente) con le prime r monete.  
-->

