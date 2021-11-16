# Model_ANN_verifier

The purpose of this TALight problem is to offer a playground where to experiment a linear programming based approach to the task of neural network verification.

## Artificial Neural Networks (ANNs)

Artificial Neural Networks (ANNs), usually simply called Neural Networks (NNs), are computing systems inspired by the biological neural networks that constitute animal brains. They are mainly used in the field of Deep Learning (DL) for classification tasks, or in the general field of learning, particularly in Reinforcement Learning (RL).
Any complex system can be abstracted in a simple way, or at least dissected to its basic abstract components. The basic units of an ANN are its *neurons*, which are organized into one or more layers.
The first and the last layers contain no neuron. These are called the input layer and the output layer, and their nodes represent the input and the output lines of the ANN. Every node carries a real number expressing its output value. 
The neurons of each layer, also represented by nodes, are fed with the output values of nodes in the previous layer and compute their own output values in deteterministic dependence from these.

The general topology of the network is illustrated in figure.
![](https://i.imgur.com/ELBOcWp.png)

A fundamental property is that the input/output function of an ANN is fully determined by the input/output function for each one of its neurons. The behaviour of each single neuron is described by its activation function and by a set of real parameters also called weights. A neuron has one weight for every node of the previous layer to which the neuron is connected.
The input/output function of a neuron is computed as follows:

   let wv be the weighted sum of its input values.
   Set the output value to f(wv), where f() is the activation function of the neuron.

Training a network amounts to choosing a complete set of weights for each one of ist neurons.

If we want to make a parallel with the functioning of the human brain, the weights represent the intensity of a possible synapses. Each neuron combines its input value through its weights and activation function, thus either amplifing or dampeing the original stimulus coming from the data offered by the input layer, thereby assigning significance to these data with regard to the task that the network training algorithm is trying to learn.

A neuron is called linear when f is the identity function, activated otherwise.
A special kind of activated neurons are the Rectified Linear Unit (ReLU), which are those neurons for which f(x) = \max{0,x}.

In general, once trained, the neural network offers (and computes) a function approximating the desired input/output behaviour for a certain device (the value of a position in chess, or the probability of cancer for a certain biopsi, the action a robot should make in a certain state, ...). When all neurons are linear then all the representable approximation functions are also linear.


## How is it possible to learn a task using ANN?
The input layer is nothing more than a set of values representing a particular initial state/feature. Each arc connecting one node to the next has a label representing the weight <img src="https://latex.codecogs.com/gif.latex?w_i"/>. So each node <img src="https://latex.codecogs.com/gif.latex?h_i"/> of the hidden layers will be: <img src="https://render.githubusercontent.com/render/math?math=h_i = \sum_{i = 0}^m x_i w_i">

![](https://i.imgur.com/uAyuxZX.png)

Activation functions are mathematical equations that determine the output of a neural network. The function is attached to each neuron (generally in the hidden layers) in the network and determines whether it should be activated “fired” or not, based on whether each neuron’s input is relevant for the model’s prediction. Activation functions also help normalize the output of each neuron to a range between 1 and 0 or between -1 and 1.
For the purpose of this problem we will not use activation functions and will only work with linear approximation functions.

### Learning process

The learning process is where one computes a set of weights so that the actual behaviour function of the network best approximates its intended behaviour. There are several classical network training algorithms through which this process is generally managed using them as black-box, mainly finding/adjusting the weights of the neural network through various steps of forward propagation and back propagation. These issues are not explored here as they are not of interest to the proposed problem.

minimizzare lo scarto massimo (si modella come programmazione lineare)

Learning lineare.
https://open.bu.edu/handle/2144/35386
https://watermark.silverchair.com/10-2-172.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAAsswggLHBgkqhkiG9w0BBwagggK4MIICtAIBADCCAq0GCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMWSHgwCGExc3qdkffAgEQgIICfhzBgzkX_6uB_7PlXDH47djTOk52LbVvxXppJDK1KBShD41dDUL6w7NT9DzgUiJK_h7DxBUjX6tI-1jOTwTypLhCMiDk5_yMljnWX0gqSUaVNxrmoOO0-qjvEhLECTW_z6mFCUeh9nkqi9DzOGF64f4MOEC6oBJ4joc2kqj1_VjBAvE27bNYRAB-cGDJ1pmKC0LyW1JoBt5HvdluE4tSYdz16hWjtJsLXB5Iqj1b445sav-N8Jx4cPcaOA-iedlgSo47f6qso3g4cN8FrqF_e29YYKJR58v2CGEReVfsf8Wy9cyGGFI6yOXNROvIeNGoCS7ufjea8AmNw9c_Hlck2q9hyEIgISOfOQhNCVRW-uvxN65PSEVD9SyNbv63hLbKSTrGZ-2_ZvoV-luVEieNV1GcqDI8FV3DKxqAGCi3Ep37muHC4QkuFSPcA5jOum7br1MWR-K-K1dYsCcOLD7qwqw4RDKokcL_a5CFB2dSJkY0b_uhDYCRxqyehlSVTmsDuuBmpNM0fC8e-k8IMW7pkyfwW0iWsKEHBKz6wLVAwONF8v3cAf6rS7NBmnq5b7mLlkDQl-7Nqcz4dfa32k888MuzOJr5OlFVM7jwmbbPKIQawGHJ2p8s1luAsptsgIk0FAhReb1XUL937LJ_PUQiOSrwOojn5tYri1WjEIbdXEmmKAAdtjWZUvSleCaSgEQ4axv6Eoux2ep3HJsa9UAQEXjScRJ0uYsntbwEg7xMIgrtGP9Zdn1V4LOfxwB8jrb-avAtHMXw9OEd6rTVISI6DecDj4HgZVTY6-XvI2PmprTTuk6Gk94hzahiAQ1G2lwjMb24pzkFTgQIz8T9oYdC


DATA:
f(x_j) = y_j per j = 1,...,m. dove x_j = (x_j[1], ... , x_j[n])

TASK:
trovare c_i, i = 1, ..., n

tali che:

\max_{j=1}^m  |c x_j - y_j| sia il più piccola possibile.

Chiamato s il valore del massimo scostamento, può essere formulato come:

\min s
   s >= c x_j - y_j, per j=1,...,m
   s >= y_j - c x_j, per j=1,...,m
c_i in R per i=1,...,n
s >= 0

se invece TASK:
trovare c_i, i = 1, ..., n

tali che:

\sum_{j=1}^m  |c x_j - y_j| sia la più piccola possibile.

può essere formulato come:

\min \sum_{j=1}^m  s_j
   s_j >= c x_j - y_j, per j=1,...,m
   s_j >= y_j - c x_j, per j=1,...,m
c_i in R per i=1,...,n
s_j >= 0 per j=1,...,m




minimizzare lo scarto quadratico medio (si modella come metodo dei minimi quadrati)
https://www.actuaries.digital/2021/03/31/gauss-least-squares-and-the-missing-planet/
https://blog.bookstellyouwhy.com/carl-friedrich-gauss-and-the-method-of-least-squares
https://thatsmaths.com/2021/06/24/gauss-predicts-the-orbit-of-ceres/


Learning non-lineare.

We limit ourself to proposing a most classical algorithm (nome, referenza, nome dei servizi che lo implementano o che verificano la nostra implementazione).


## Neural Network verification
The verification of neural networks proves that a given input corresponds to a given output or that the output is in a given range.

<img src="https://latex.codecogs.com/gif.latex?\mathcal{X}_0&space;\in&space;[\underline{x_0}&space;\;\;&space;\Bar{x_0}]&space;\land&space;...&space;\land&space;\mathcal{X}_n&space;\in&space;[\underline{x_n}\;\;&space;\Bar{x_n}]&space;\implies&space;\mathcal{Y}&space;\in&space;[\underline{y_n}\;\;&space;\Bar{y_n}]" title="\mathcal{X}_0 \in [\underline{x_0} \;\; \Bar{x_0}] \land ... \land \mathcal{X}_n \in [\underline{x_n}\;\; \Bar{x_n}] \implies \mathcal{Y} \in [\underline{y_n}\;\; \Bar{y_n}]" />

Since a network can have many input nodes that describe a particular initial configuration, and each has its own domain, to verify that the network respects certain constraints, we should test all possible combinations that obviously could be infinite, which makes the problem NP-hard. However, it is possible to use modeling and Linear Programming (LP) methods to be able to determine whether particular properties are satisfied or not given a given neural network (already trained) and constraints for the output. Let's see an example:
![](https://i.imgur.com/UUYV6Pv.png)

This is a very simple example, we have this NN already trained, where there is a single input node <img src="https://latex.codecogs.com/gif.latex?x_1"/> and a single hidden layer composed by two nodes <img src="https://latex.codecogs.com/gif.latex?x_2,x_3"/> and a single output node <img src="https://latex.codecogs.com/gif.latex?x_4"/>.
We want to check if this property could be satisfied: <img src="https://latex.codecogs.com/gif.latex?for\;&space;x_1&space;\in&space;[0\;\;1],&space;\;\;&space;always\;&space;x_4&space;\notin&space;[0.5\;\;1]" title="for\; x_1 \in [0\;\;1], \;\; always\; x_4 \notin [0.5\;\;1]" />

In other words if we can find an assignment for the variables <img src="https://latex.codecogs.com/gif.latex?x_1,x_2,x_3"/> that make <img src="https://latex.codecogs.com/gif.latex?x_4"/> be in that range, then the property is not satisfied, i.e. it violates that particular constraint.
To do this (find a counterexample) it is better to overturn the property, that is just to find an assignment for <img src="https://latex.codecogs.com/gif.latex?x_1,x_2,x_3"/> that allows <img src="https://latex.codecogs.com/gif.latex?x_4&space;\in&space;[0.5\;\;1]" title="x_4 \in [0.5\;\;1]" /> .

Intuitively if we look the network is simple to see that the property (not the negated one) always holds, can you say why? **Can you figure out how to model this problem? One suggestion might be to start by rewriting each node with the above formula....**




Given that this task is an NP-hard problem, your task will be to model this problem, i.e., to try to relate this problem to a class of problems for which a solution strategy is known.

The verification of neural networks (optimization) using linear programming algorithms (Simplex) is known in the literature due to this contribution:

- Katz, G., C. Barrett, D. L. Dill, K. Julian, and M. J. Kochenderfer. 2017. “Reluplex: An efficient SMT solver for verifying deep neural networks”. In: International Conference on Computer Aided Verification.


## Prerequisites
- Python3.7+
- GMPL

## Services for this problem
Lo scopo dell'utente è riuscire a scrivere il modello (.mod) per questo problema, che data una rappresentazione (equazioni, matrici, grafi,....) trovi una risposta che sia sempre corretta. Quindi l'utente tramite il servizio try_gmpl testa il suo modello su una istanza fornita e il servizio internamente chiama gmpl sol sulla coppia di argomenti e stampa il risultato.
Se l'utente chiede al servizio try_gmpl di valutare la soluzione ottenuta dal modello sull'istanza c'è la necessità da parte dell'utente di passare come input una rappresentazione dell'istanza che può essere grafo, matrice, ecc, in formato .dat o .txt che però deve essere coerente con il sistema di verifica (deve essere accettato dal modello scritto dal problem maker o dalla sua lib)

eval_gmpl --> prende il modello dell'utente e lo testa su un insieme di istanze generate in formato .dat (che possono essere però matrici, grafi, equazioni, ecc...) e lo confronta con il modello del problem maker.

Step da fare:
1) creo un mio modello di rete che passerò a GMPL sol 
2) metodo per genere le istanze --> basta modificare il file instance_generator.py e il GEN dove all'inizio si specificano tutti i vari formati, e poi su suite si creano le varie cartelle da mettere in instances (è obbligatorio per ogni goal dell'eval avere una cartella specifica con lo stesso nome, basta copiare il template dell'eval)
3) fare try ed eval


- [x] Service 
- [x] Service 2
- [x] Service 3



