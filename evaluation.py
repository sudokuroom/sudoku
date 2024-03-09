
class Evaluation:
    def __init__(self, grille) -> None:
        self.grille = grille
        self.tableau = [[0]*9 for i in range(9)]   

    def candidats(self):
        for i in range(9):
            for j in range(9):
                if self.grille[i][j] != 0:
                    compteur = 0
                    for k in range(1,10):
    #                    if permis(k):
                            compteur = compteur + 1
                    self.tableau[i][j] = compteur
        