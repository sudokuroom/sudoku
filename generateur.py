import random

# generateur Gemini

 # Vérifier si n est permis dans la case x y  {assertion: la case x y est vide}
def permis(grille,x,y,n):
      for k in range(9):
          if grille[x][k] == n: return False     # parcours ligne
          if grille[k][y] == n: return False     # parcours colonne
      x0, y0 = (x//3)*3, (y//3)*3                # base du bloc 3x3 de x y
      for i in range(3):
          for j in range(3):
              if grille[x0+i][y0+j] == n: return False
      return True

def est_valide(grille, i, j, valeur):
    """     Vérifie si la valeur est valide dans la case (i, j) de la grille.     """
    for k in range(9):
        if grille[i][k] == valeur or grille[k][j] == valeur:
            return False
    ligne_debut = (i // 3) * 3
    colonne_debut = (j // 3) * 3
    for k in range(3):
        for l in range(3):
            if grille[ligne_debut + k][colonne_debut + l] == valeur:
                return False
    return True

def generer_grille_sudoku(difficulte):
    """
    Génère une grille de Sudoku aléatoire avec un niveau de difficulté donné.
    """
    grille = [[0 for i in range(9)] for j in range(9)]

    random.seed()

    # Remplir aléatoirement des cases
    for _ in range(difficulte):
        random.seed()
        while True:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            valeur = random.randint(1, 9)
            if permis(grille, i, j, valeur):
                grille[i][j] = valeur
                break

    # Utiliser le backtracking pour remplir les cases vides
    def backtrack(i, j):
        if i == 9:
            return True
        if j == 9:
            return backtrack(i + 1, 0)
        if grille[i][j] != 0:
            return backtrack(i, j + 1)
        for valeur in range(1, 10):
            if permis(grille, i, j, valeur):
                grille[i][j] = valeur
                if backtrack(i, j + 1):
                    return True
                grille[i][j] = 0
        return False

    backtrack(0, 0)

    return grille

def afficher_grille(grille):
    """
    Affiche la grille de Sudoku sur la console.
    """
    c = ""
    for i in range(9):
        for j in range(9):
            print(grille[i][j], end=" ")
            c = c + chr(48+grille[i][j])
        print()
    print(c)

# Génération et affichage d'une grille de Sudoku
grille = generer_grille_sudoku(25)
afficher_grille(grille)