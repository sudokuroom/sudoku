from grille import *
from visualiser import *


test = "030001005600000090090620000061090003000070000500030470000015080050000002900300040"
couverture = "7.3000005680702000000000800900800000007326400000009001004000000000203074100000206"

grille = Grille()

grille.set_grille_chaine(couverture)

grille.visualiser()

print("****************")

#grille.resoudre()





