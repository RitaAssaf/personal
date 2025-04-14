from pycsp3 import *
houses = range (5)
 # each house has a number from 0 ( left ) to 4 ( right )
# colors [ i ] is the house of the ith color
yellow , green , red , white , blue = colors = VarArray ( size =5 , dom = houses )
# nations [ i ] is the house of the inhabitant with the ith nationality
italy , spain , japan , england , norway = nations = VarArray ( size =5 , dom = houses )
# jobs [ i ] is the house of the inhabitant with the ith job
painter , sculptor , diplomat , pianist , doctor = jobs = VarArray ( size =5 , dom = houses )
# pets [ i ] is the house of the inhabitant with the ith pet
cat , zebra , bear , snails , horse = pets = VarArray ( size =5 , dom = houses )
# drinks [ i ] is the house of the inhabitant with the ith preferred drink
milk , water , tea , coffee , juice = drinks = VarArray ( size =5 , dom = houses )
satisfy (
AllDifferent ( colors ) ,
AllDifferent ( nations ) ,
AllDifferent ( jobs ) ,
AllDifferent ( pets ) ,
AllDifferent ( drinks ) ,
painter == horse ,
diplomat == coffee ,
61
white == milk ,
spain == painter ,
england == red ,
snails == sculptor ,
green + 1 == red ,
blue + 1 == norway ,
doctor == milk ,
japan == diplomat ,
norway == zebra ,
abs ( green - white ) == 1 ,
horse in { diplomat - 1 , diplomat + 1} ,
italy in { red , white , green }
)