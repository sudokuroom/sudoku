import random
from grille import *

# Genération d'une grille de Sudoku complète (avec 81 chiffres)

class Generateur():
    def __init__(self) -> None:
        self.grille = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku()

    def permis(self,x,y,n):
      for k in range(9):
          if self.grille[x][k] == n: return False     # parcours ligne
          if self.grille[k][y] == n: return False     # parcours colonne
      x0, y0 = (x//3)*3, (y//3)*3                     # base du bloc 3x3 de x y
      for i in range(3):
          for j in range(3):
              if self.grille[x0+i][y0+j] == n: return False
      return True

    def is_safe(self, grid, row, col, num):
        # Vérifier la ligne
        if num in grid[row]:
            return False     
        # Vérifier la colonne
        if num in [grid[i][col] for i in range(9)]:
            return False       
        # Vérifier le carré 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False        
        return True

    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True  # La grille est remplie
        
        row, col = empty_cell

        for num in random.sample(range(1, 10), 9):
            if self.is_safe(self.grille, row, col, num):
                self.grille[row][col] = num

                if self.solve_sudoku():
                    return True

                self.grille[row][col] = 0  # Annuler l'attribution si le chiffre ne convient pas
        
        return False  # Aucune solution trouvée

    def find_empty_cell(self):
            for i in range(9):
                for j in range(9):
                    if self.grille[i][j] == 0:
                        return i, j
            return None


# Tests
if __name__ == "__main__":
    g = Generateur()
    print(g.grille)

    gg = Grille()
    gg.grille = g.grille
    gg.visualiser()

 