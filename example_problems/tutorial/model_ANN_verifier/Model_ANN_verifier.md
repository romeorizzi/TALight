# Model_ANN_verifier
The purpose of this problem is to provide a first approach to the task of neural network verification using linear programming. We will start with the basics, introducing what a neural network is, how it is possible to learn a task using this approach, and how it is possible to verify that the network actually learned what was required.

You will soon understand that this task is an NP-hard problem, so your task will be to model this problem, i.e., to try to relate this problem to a class of problems for which a solution strategy is known.

The verification of neural networks (optimization) using linear programming algorithms (Simplex) is known in the literature due to this contribution:

- Katz, G., C. Barrett, D. L. Dill, K. Julian, and M. J. Kochenderfer. 2017. “Reluplex: An efficient SMT solver for verifying deep neural networks”. In: International Conference on Computer Aided Verification.

## What is an Artificial Neural Network(ANN)?
Artificial neural networks (ANNs), usually simply called neural networks (NNs), are computing systems inspired by the biological neural networks that constitute animal brains. Any complex system can be abstracted in a simple way, or at least dissected to its basic abstract components.
In particular, neural networks are approximation functions (linear or not) that are mainly used in the field of Deep Learning (DL) for classification tasks, for example, or in the field of learning, particularly in Reinforcement Learning (RL).

An ANN is a processing system that includes a collection of connected units called *neurons*, which are organized into one or more layers. Each connection between neurons transmits a signal that goes from the neurons to the input nodes, to one or more layers up to the output/s node/s. Generally it is represent as:

![](https://i.imgur.com/ELBOcWp.png)
A node combines input from the data with a set of coefficients, or *weights*, that either amplify or dampen that input, thereby assigning significance to inputs with regard to the task the algorithm is trying to learn.
These input-weight products are summed and then the sum is passed through a node’s so-called ***activation function***, to determine whether and to what extent that signal should progress further through the network to affect the outcome. If we want to make a parallel with the functioning of the human brain, these connections represent the synapses.

## How is it possible to learn a task using ANN?
The input layer is nothing more than a set of values representing a particular initial state/feature. Each arc connecting one node to the next has a label representing the weight <img src="https://latex.codecogs.com/gif.latex?w_i"/>. So each node <img src="https://latex.codecogs.com/gif.latex?h_i"/> of the hidden layers will be: <img src="https://latex.codecogs.com/gif.latex?h_i = \sum_{i = 0}^m x_i \; w_i" /> 

![](https://i.imgur.com/uAyuxZX.png)

Activation functions are mathematical equations that determine the output of a neural network. The function is attached to each neuron (generally in the hidden layers) in the network and determines whether it should be activated “fired” or not, based on whether each neuron’s input is relevant for the model’s prediction. Activation functions also help normalize the output of each neuron to a range between 1 and 0 or between -1 and 1.
For the purpose of this problem we will not use activation functions and will only work with linear approximation functions.

### Learning process
We have said that neural networks are nothing more than functions of approximations that, given a particular input, return a particular output. For example, in the field of reinforcement learning, given a particular state in which the robotic agent is, and that is passed as input, the network returns a particular value that encodes a particular action.

But how does the learning process take place? It's all about correctly finding/adjusting the weights of the neural network through various steps of forward propagation and back propagation. These issues are not explored here as they are not of interest to the proposed problem. We only see an example of forward propagation and what we mean by verification of the neural network.

## Neural Network verification
The verification of neural networks proves that a given input corresponds to a given output or that the output is in a given range.

<img src="https://latex.codecogs.com/gif.latex?\mathcal{X}_0 \in [\underline{x_0} \;\; \Bar{x_0}] \land ... \land \mathcal{X}_n \in [\underline{x_n}\;\; \Bar{x_n}]  \implies \mathcal{Y} \in [\underline{y_n}\;\; \Bar{y_n}]"/>

Since a network can have many input nodes that describe a particular initial configuration, and each has its own domain, to verify that the network respects certain constraints, we should test all possible combinations that obviously could be infinite, which makes the problem NP-hard. However, it is possible to use modeling and Linear Programming (LP) methods to be able to determine whether particular properties are satisfied or not given a given neural network (already trained) and constraints for the output. Let's see an example:
![](https://i.imgur.com/UUYV6Pv.png)
This is a very simple example, we have this NN already trained, where there is a single input node <img src="https://latex.codecogs.com/gif.latex?x_1"/> and a single hidden layer composed by two nodes <img src="https://latex.codecogs.com/gif.latex?x_2,x_3"/> and a single output node <img src="https://latex.codecogs.com/gif.latex?x_4"/>.
We want to check if this property could be satisfied: <img src="https://latex.codecogs.com/gif.latex?for\; x_1 \in [0\;\;1], \;\; always\; x_4 \notin [0.5\;\;1]"/>.

In other words if we can find an assignment for the variables <img src="https://latex.codecogs.com/gif.latex?x_1,x_2,x_3"/> that make <img src="https://latex.codecogs.com/gif.latex?x_4"/> be in that range, then the property is not satisfied, i.e. it violates that particular constraint.
To do this (find a counterexample) it is better to overturn the property, that is just to find an assignment for <img src="https://latex.codecogs.com/gif.latex?x_1,x_2,x_3"/> that allows <img src="https://latex.codecogs.com/gif.latex?x_4 \in [0.5\;\;1]"/>.

Intuitively if we look the network is simple to see that the property (not the negated one) always holds, can you say why? **Can you figure out how to model this problem? One suggestion might be to start by rewriting each node with the above formula....**

## Prerequisites
- Python3.7+
- GMPL

## Services for this problem
Lo scopo dell'utente è riuscire a scrivere il modello (.mod) per questo problema, che data una rappresentazione (equazioni, matrici, grafi,....) trovi una risposta che sia sempre corretta. Quindi l'utente tramite il servizio try_gmpl testa il suo modello su una istanza fornita e il servizio internamente chiama gmpl sol sulla coppia di argomenti e stampa il risultato.
Se l'utente chiede al servizio try_gmpl di valutare la soluzione ottenuta dal modello sull'istanza c'è la necessità da parte dell'utente di passare come input una rappresentazione dell'istanzache può essere grafo, matrice, ecc in formato .dat o .txt che però deve essere coerente con il sistema di verifica (deve essere accettato dal modello scritto dal problem maker o dalla sua lib)

eval_gmpl --> prende il modello dell'utente e lo testa su un insieme di istanze generate in formato .dat (che possono essere però matrici, grafi, equazioni, ecc...) e lo confronta con il modello del problem maker.

Step da fare:
1) creo un mio modello di rete che passerò a GMPL sol 
2) metedo per genere le istanze --> basta modificare il file instance_generator.py e il GEN dove all'inizio si specificano tutti i vari formati, e poi su suite si creano le varie cartelle da mettere in instances (è obbligatorio per ogni goal dell'eval avere una cartella specifica con lo stesso nome, basta copiare il template dell'eval)
3) fare try ed eval


- [x] Service 
- [x] Service 2
- [x] Service 3





## Author
* **Luca Marzari** - [LM095](https://github.com/LM095)

