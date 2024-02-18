from grille import *

test = "030001005600000090090620000061090003000070000500030470000015080050000002900300040"

grille = Grille()

grille.set_grille_chaine(test)

grille.afficher()

print("****************")

grille.rotation()

grille.afficher()

grille.resoudre()


