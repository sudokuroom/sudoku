from grille import *

#  grid = [[0 for i in range(9)] for j in range(9)]

grid = [
    [4,0,0,0,0,2,0,0,6],
    [0,0,0,0,0,0,0,9,0],
    [8,0,3,0,7,0,0,0,0],
    [0,0,0,0,0,6,0,0,0],
    [6,0,2,0,0,0,0,0,0],
    [0,0,0,8,0,9,0,0,1],
    [0,7,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,4,0],
    [0,0,1,2,0,0,8,0,0]
    ]

nb = 0

class Solution:
    def __init__(self):
      self.grid = [[0 for i in range(9)] for j in range(9)]
      self.nb = 0


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
    exit(0)



pb = Grille()
pb.set_grille(grid)
pb.afficher()

solve()