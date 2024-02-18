from grille import *

# module de mise au point la classe Solution ne sera pas developée finalement

#  grid = [[0 for i in range(9)] for j in range(9)]

grid = [
    [4,0,0,0,0,2,0,7,6],
    [0,0,5,0,0,8,0,9,0],
    [8,0,3,0,7,0,0,0,0],
    [1,0,0,0,0,6,0,0,0],
    [6,0,2,5,0,0,4,0,0],
    [0,0,0,8,0,9,0,0,1],
    [0,7,0,4,0,0,0,2,0],
    [0,0,0,0,3,0,0,0,0],
    [3,0,1,2,0,0,0,5,0]
    ]

nb = 0

""" Solution calcule les solutions d'une grille
resoudre()  imprimer les solutions
solutions() fournit le nombre des solutions
"""
class Solution:
    def __init__(self):
      self.grille = [[0 for i in range(9)] for j in range(9)]    
      self.nb = 0
      self.resultat = self.grille

    # vérifier si n est permis dans la case x y
    def permis(self,x,y,n):
        for k in range(9):
            if self.grille[x][k] == n: return False     # parcours ligne
            if self.grille[k][y] == n: return False     # parcours colonne
        x0 = (x//3)*3                                   # base du bloc 3x3 de x y
        y0 = (y//3)*3
        for i in range(3):
            for j in range(3):
                if self.grille[x0+i][y0+j] == n: return False
        return True

    # résoudre le sudoku
    def resoudre(self):
        self.nb = 0
        for x in range(9):
            for y in range(9):
                if self.grille[x][y] == 0:
                    for n in range(1,10):
                        if self.permis(x,y,n):
                            self.grille[x][y] = n
                            self.resoudre()
                            self.grille[x][y] = 0
                    return
        self.nb = self.nb + 1
        




def n_valide(y, x, n):
    """Détermine si un nombre n peut être mis sur une case à la colonne x et à la ligne y"""
    global grid
    #On détermine si le nombre est valide sur sa ligne
    for x0 in range(len(grid)):
        if grid[y][x0] == n:
            return False

    #On détermine si le nombre est valide sur sa colonne
    for y0 in range(len(grid)):
        if grid[y0][x] == n:
            return False
    
    x0 = (x//3) * 3
    y0= (y//3) * 3
    #On détermine si le nombre est valide dans sa sous-grille 3x3
    for i in range(3):
        for j in range(3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

def solve():
    global grid, nb
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if n_valide(y, x, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    nb = nb + 1
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end="")
        print()
    print("-------------------------", nb)
    # exit(0)



pb = Grille()
pb.set_grille(grid)
pb.afficher()

solve()


