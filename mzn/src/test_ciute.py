from pycsp3 import *
x = VarArray ( size =4 , dom = range (4))
i = Var ( range ( -1 , 4))
satisfy (
Or ( Sum ( x ) > 10 , AllDifferent ( x )) ,
IfThen ( i != -1 , x [ i ] == 1)
)