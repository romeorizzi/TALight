% Graph K-colorability
% MathDecisions 2020
% Department of Computer Science, University of Verona, Italy
% Matteo Zavatteri, March 2020

% PROBLEM DEFINITION: 
% INPUT: An (undirected) graph G=(V,E) and a positive integer K
% OUTPUT: yes iff there exists f:V->{1,..,K} such that f(u) != f(v) whenever (u,v) is in E
%

% Graph G
int: N;
set of int: V = 1..N;
array[V] of set of int: E;
int: K;

array[V] of var 1..K: f;

% Condition
constraint(
   forall(u in V, v in E[u])(f[u] != f[v]) 
);


% Debug:
%output["V=", show(V), "\n"];
%output["E=", show(E), "\n"];

solve satisfy;

output["f=", show(f)];






  


