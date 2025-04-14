% Subgraph isomorphism problem with constrained angles
% https://en.wikipedia.org/wiki/Subgraph_isomorphism_problem
% Run with: minizinc --globals-dir std

% Global constraints defined in /usr/share/minizinc/std
include "alldifferent.mzn";

% Angle of the edge of a graph
enum ORDER_RELATIONS = { l, c };

% =============== DATA

% Pattern graph G1 = (V1, E1), with |V1| = NV_1, |E1| = NV_1, and A1 the angle of each edges in E1
int: NV_1;
int: NE_1;
array[1..NV_1] of string: V1;
array[1..NE_1, 1..2] of 1..NV_1: E1;
array[1..NE_1] of ORDER_RELATIONS: A1;

% Target graph G2 = (V2, E2), with |V2| = NV_2, |E2| = NV_2, and A2 the angle of each edges in E2
int: NV_2;
int: NE_2;
array[1..NV_2] of string: V2;
array[1..NE_2, 1..2] of 1..NV_2: E2;
array[1..NE_2] of ORDER_RELATIONS: A2;

% =============== VARIABLE

% Mapping nodes from graph 1 to graph 2
array[1..NV_1] of var 1..NV_2: I;

% =============== CONSTRAINT

constraint

	% Map all nodes from graph 1
	alldifferent(I)

	% Each edges of graph 1 has a mapping in graph 2 (I*(E1) subset E2), with angle(e1) = angle(e2)
	/\ forall(e1 in 1..NE_1)
	(
		% Found a mapping from the edge in graph 1 to an edge in graph 2, with angle(e1) = angle(e2)
		exists(e2 in 1..NE_2, p in 1..2)
		(
			A1[e1] == A2[e2]
			%/\ I[E1[e1, 1]] == E2[e2, p] /\ I[E1[e1, 2]] == E2[e2, p mod 2 + 1] % allows both orientation (a,b,c) mapped to (1,2,3) & (3,2,1)  
			/\ I[E1[e1, 1]] == E2[e2, 1] /\ I[E1[e1, 2]] == E2[e2, 2]
			%ajouter la contrainte de ILF
		)
	)
;

% =============== SOLVE

solve satisfy;