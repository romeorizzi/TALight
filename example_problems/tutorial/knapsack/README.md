  dec2opt:
    explains: "this service poses you an instance of the Knapsack problem in its decision form and remains available as an oracle for the Knapsack problem in its optimization form. You can call the oracle as many times as you want but are asked to ultimately answer yes or no for the single decision question posed by the server at the very start of the exchange."

> rtal connect knapsack -an=5 -a goal=at_most_one_call dec2opt -- mybot
# sono il servizio dec2opt del problma knapsack
# sono stato chiamato coi parametri ... seed=random_seed ...
# ho generato un certo seed, esso è 34532643.
5 100 752
# n=5  cap_zaino = 100  target=752
22 171
# peso valore 
12 112
20 71
42 371
51 271
# il server ha fornito l'istanza
> 5 100
> 22 171
> 12 112
> 20 71
> 42 371
> 51 271
642
> n

==========================================

  opt2con:
    explains: "this service poses you an instance of the Knapsack problem in its optimization form and remains available as an oracle for the Knapsack problem in its construction form. You can call the oracle as many times as you want but are asked to ultimately answer with the optimum value for the single optimization question posed by the server at the very start of the exchange."

> rtal connect knapsack -an=5 -a goal=at_most_one_call opt2con -- mybot
# sono il servizio opt2con del problma knapsack
# sono stato chiamato coi parametri ... seed=random_seed ...
# ho generato un certo seed, esso è 34532643.
5 100
# n=5  cap_zaino = 100
22 171
# peso valore 
12 112
20 71
42 371
51 271
# il server ha fornito l'istanza
> 5 100
> 22 171
> 12 112
> 20 71
> 42 371
> 51 271
0 0 0 1 1
> 642

==========================================

  con2dec:
    explains: "this service poses you an instance of the Knapsack problem in its construction form and remains available as an oracle for the Knapsack problem in its decision form. You can call the oracle for the decision form as many times as you want but are asked to ultimately yield an optimal solution for the single construction question posed by the server at the very start of the exchange. Posing yourself a different set of goals, you might also ask for one single call to an oracle for the Knapsack problem in its optimization form (see the arguments of the service to know more)."
      goal:
        regex: ^(correct|polynomial_dec_calls|at_most_n_dec_calls)$
        default: correct
      ask_for_one_opt_oracle_call:
        explain: "setting this flag to 1, your very first call to an oracle is interpreted as a call to an oracle for the Knapsack problem in its optimization form. By resorting on a suitable such call, you can reduce to at most n the calls to the decision oracle."
        regex: ^(0|1)$
        default: 0


> rtal connect knapsack -aask_for_one_opt_oracle_call -an=5 -a goal=at_most_one_call con2dec -- mybot
# sono il servizio dec2opt del problma knapsack
# sono stato chiamato coi parametri ... seed=random_seed ...
# ho generato un certo seed, esso è 34532643.
5 100
# n=5  cap_zaino = 100
22 171
# peso valore 
12 112
20 71
42 371
51 271
# il server ha fornito l'istanza
> 5 100
> 22 171
> 12 112
> 20 71
> 42 371
> 51 271
642
> 4 100 642
> 12 112
> 20 71
> 42 371
> 51 271
y
> 3 100 642
> 20 71
> 42 371
> 51 271
y
> 2 100 642 
> 42 371
> 51 271
y
> 1 100 642 
> 51 271
n
> 0 0 0 1 1

==========================================




  trilly:
    explains: "this service poses you an n elements instance of the Knapsack problem in its optimization form and remains available as an oracle for the Knapsack problem, again in its optimization form, but considering only instances on at most n-1 elements. You can call this oracle as many times as you want but are asked to ultimately yield an optimal solution for the single optimization question posed by the server at the very start of the exchange."

> rtal connect knapsack -an=5 -a goal=at_most_two_calls trilly -- mybot
# sono il servizio opt2con del problma knapsack
# sono stato chiamato coi parametri ... seed=random_seed ...
# ho generato un certo seed, esso è 34532643.
5 100
# n=5  cap_zaino = 100
22 60
12 112
20 71
42 371
51 271
# il server ha fornito l'istanza
> 4 100
> 22 60
> 12 112
> 20 71
> 42 371
614
> 4 49
> 22 60
> 12 112
> 20 71
> 42 371
371
> # 371 + 271 = 642 > 614
> 642


==========================================
