
			cnt = 0
			while solve () is SAT :
				cnt += 1
				print (f" Solution { cnt }:{ values ( I )} " )
				satisfy ( I != values ( I ))

[
			((I[u], I[v]) in E2) for (u, v) in E1
		]

[
			Exist(
					(I[E1[e1][0]] == E2[e2][p]) & (I[E1[e1][1]] == E2[e2][(p+ 1) % 2]) #p=1 ou 0
				for e2 in range(NE_2) for p in range(2) if A1[e1]==A2[e2]
			) for e1 in range(NE_1)
		]

[
			Exist(
					(I[E1[e1][0]] == E2[e2][p]) & (I[E1[e1][1]] == E2[e2][(p+ 1) % 2]) #p=1 ou 0
				for e2 in range(NE_2) for p in range(2) if A1[e1]!=A2[e2]
			) for e1 in range(NE_1)
		]