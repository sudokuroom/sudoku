import tkinter as tk
from visualiser import *
import random

class Grille:
  """   Modèle objet de Grille de Sudoku : Une grille est un tableau de dimension 9x9
  afficher()                      afficher la grille courante
  afficher_solution()             afficher la solution
  visualiser()                    afficher la grille courante dans une fenêtre tkinter
  set_grille_chaine(chaine)       entrer une grille comme chaine 81 caractères
  set_grille(grille)              entrer une grille comme tableau 9x9
  verification()                  retourne True si la grille courante (partielle) est valide 
  valide()                        retourne True si la grille courante (complète) est valide 
  permis(x,y,n)                   vérifie que le chiffre n est permis en x y retourne True False
  possibles()                     calcul des candidats dans chaque case vide -> candidats[][]
  resoudre()                      résolution de la grille de sudoku (récursif) -> nb, solution
  sauver(nom_fichier)             sauvegarder la grille courante comme une chaine de 81 caractères
  lire_chaine(nom_fichier)        lire une grille comme chaine de 81 caractères
  permuter(permutation)           remplacer chaque chiffre de la grille par un autre chiffre
  rotation()                      tourner la grille de 90 degrés - sens des aiguilles d'une montre
  generer()                       générer aléatoirement une grille complète
  """
  # ---------------------------------------------------------------------------------------------------------------
  # Constructeur
  # ---------------------------------------------------------------------------------------------------------------
  def __init__(self):                                                                
    self.grille = [[0]*9 for i in range(9)]                      # grille de Sudoku, présumée incomplète
    self.solution = [[0 for i in range(9)] for j in range(9)]    # grille solution, grille complète
    self.nb = 0                                                  # nombre de solutions trouvées par resoudre()
    self.candidats = [[[] for i in range(9)] for j in range(9)]  # candidats dans les cases vides (type = list)

  # ---------------------------------------------------------------------------------------------------------------    
  # Afficher la grille courante 9x9 sur la console
  # ---------------------------------------------------------------------------------------------------------------
  def afficher(self):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")       
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(self.grille[i][j])
            else:
                print(str(self.grille[i][j]) + " ", end="")
  
  # ---------------------------------------------------------------------------------------------------------------
  # Afficher la grille solution
  # ---------------------------------------------------------------------------------------------------------------
  def afficher_solution(self):
     for i in range(9):
        for j in range(9):
           print(self.solution[i][j], end="")
        print()
  
  # Visualiser la grille courante dans une fenetre tkinter
  def visualiser(self):
    root = tk.Tk()
    root.title("Grille de Sudoku")
    root.geometry("400x400")
    # Encadrement du conteneur principal avec une bordure noire
    frame = tk.Frame(root, borderwidth=2, relief='solid')
    frame.pack(expand=True, fill='both')
    # Grille de Sudoku
    sudoku_grid = SudokuGrid(frame, self.grille)
    sudoku_grid.pack(expand=True, fill='both')
    root.mainloop()
     
  # Entrer une grille sous forme de chaine  len(chaine) = 81  (soit k position de 0 à 80 alors i = k//9 j = k%9)
  def set_grille_chaine(self, chaine):
    if len(chaine) == 81:                                         # contrôle la longueur du vecteur
      vecteur = list(map(lambda x: ord(x)-48, chaine))            # convertir alpha en chiffres 0 à 9
      for i in range(81):      
       if vecteur[i] < 0 or vecteur[i] > 9: vecteur[i] = 0        # remplace par 0 les caractères non chiffres 0 à 9      
      for k in range(81):
        i = k//9      # floor(k/9)
        j = k - 9*i   # k%9
        self.grille[i][j] = vecteur[k]
    else:
       print("La chaine doit être composée de 81 caractères")
    
  # Entrer une grille sous forme de matrice 9x9 (a revoir l'adresse passée en paramètre) ** à tester **
  def set_grille(self, tableau):
    self.grille = tableau
  # Fournir une grille sous forme de matrice 9x9
  def get_grille(self):
     return self.grille

  # Vérifier si la grille complète est valide (ne traite pas les grilles partielles)
  def valide(self):
     chiffres = {1,2,3,4,5,6,7,8,9}
     for i in range(9):
        if set(self.grille[i]) != chiffres: return False
        if set(self.grille[j][i] for j in range(9)) != chiffres: return False     
     for i in range(0, 9, 3):
        for j in range(0, 9, 3):
          bloc = []                # autre solution bloc = set() et bloc.add(self.grille[i+k][j+l])
          for k in range(3):
              for l in range(3):
                  bloc.append(self.grille[i+k][j+l])
          if set(bloc) != chiffres:
              return False
     return True
  
  # Verifier si une grille partielle est valide (aucun doublon dans aucun secteur)
  def verification(self):
    def zero(s):                                              # enleve les zeros dans le secteur qui est analysé
       while 0 in s: s.remove(0)
       return list(s)
    for i in range(9):                                        # parcours des lignes et des colonnes
        ligne = zero(self.grille[i].copy())                   # en l'absence .copy() la grille est modifiée !
        if len(ligne) != len(set(ligne)): return False
        colonne = zero([self.grille[j][i] for j in range(9)].copy())
        if len(colonne) != len(set(colonne)): return False
    for b in range(9):                                         # parcours de tous les blocs
        liste = []
        for i in range(3*(b//3), 3*(b//3)+3):
           for j in range(3*(b%3), 3*(b%3)+3):
              liste.append(self.grille[i][j])
        liste = zero(liste)
        if len(liste) != len(set(liste)): return False
    return True

  # Vérifier si n est permis dans la case x y  {assertion: la case x y est vide}
  def permis(self,x,y,n):
      for k in range(9):
          if self.grille[x][k] == n: return False     # parcours ligne
          if self.grille[k][y] == n: return False     # parcours colonne
      x0, y0 = (x//3)*3, (y//3)*3                     # base du bloc 3x3 de x y
      for i in range(3):
          for j in range(3):
              if self.grille[x0+i][y0+j] == n: return False
      return True
  
  # Calcule les candidats possibles dans chaque case et remplit candidats[][]
  def possibles(self):     
     for i in range(9):
        for j in range(9):
          if self.grille[i][j] == 0:
            chiffres = []
            for k in range(1,10):
              if self.permis(i, j, k):
                chiffres.append(k)
            self.candidats[i][j] = chiffres
          else:
             self.candidats[i][j] = []
       
  # ---------------------------------------------------------------------------------------------------------------          
  # résoudre la grille de sudoku: grille -> solution
  # ---------------------------------------------------------------------------------------------------------------
  def resoudre(self):      
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
      for i in range(9):
        for j in range(9):
            self.solution[i][j] = self.grille[i][j]
      #self.afficher_solution()
      #print("-------------------------", self.nb)

  # ---------------------------------------------------------------------------------------------------------------
  # sauvegarde de la grille sous forme de chaine dans un fichier len = 81, case vide = 0
  # ---------------------------------------------------------------------------------------------------------------
  def sauver(self, nom):
    chaine = ""
    for i in range(9):
       for j in range(9):
          chaine = chaine + chr(48+self.grille[i][j])
    try:
      with open(nom, "w") as fichier:
        fichier.write(chaine)
    except Exception as e:
      print(f"Une erreur est survenue lors de la sauvegarde du fichier : {e}")
    finally:
      fichier.close()
      print(f"Sauvegarde effectuée, fichier : {nom}")

  # ---------------------------------------------------------------------------------------------------------------
  # lire une grille sous forme de chaine dans un fichier
  def lire_chaine(self, nom):
    try:
      with open(nom, "r") as fichier:
        chaine = fichier.read()
    except Exception as e:
      print(f"Une erreur est survenue lors de la lecture du fichier : {e}")
      return None
    finally:
      fichier.close()
      self.set_grille_chaine(chaine)
      print(f"Lecture effectuée, fichier : {nom}")
      return chaine

  # ---------------------------------------------------------------------------------------------------------------
  # Permutation des chiffres de la grille  permutation = [0,8,7,1,2,3,6,9,4,5] (avec 0 initial)
  def permuter(self, permutation):
    tempo = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
       for j in range(9):
          tempo[i][j] = permutation[self.grille[i][j]]
    self.grille = tempo

  # ---------------------------------------------------------------------------------------------------------------   
  # Rotation de 90 degrés à droite, position de la cellule après rotation: i -> j et j -> 9 - i -1
  def rotation(self):
    tempo = [[0]*9 for i in range(9)]
    for i in range(9):
        for j in range(9):
      # Accéder à la cellule courante
          tempo[j][8-i] = self.grille[i][j]
    self.grille = tempo

  # ---------------------------------------------------------------------------------------------------------------  
  # Generation d'une grille aléatoire
  def generer(self):
     while True:
      for _ in range(25):
        random.seed()
        while True:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.grille[i][j] == 0:
               valeur = random.randint(1, 9)
               if self.permis(i, j, valeur):
                  self.grille[i][j] = valeur
                  break
      self.resoudre()
      print("Grille générée:", self.nb)
      if self.nb == 1: break
      #self.afficher()

  # ---------------------------------------------------------------------------------------------------------------     
  # Evaluation de la grille courante, calcul des paramètres courants
  # ---------------------------------------------------------------------------------------------------------------
  def evaluer(self) -> tuple:
    # Calcul des fréquences des chiffres
    frequences = [0 for i in range(10)]
    for i in range(9):
       for j in range(9):
          frequences[self.grille[i][j]] += 1
    # Calcul des présences
    presences = 9
    for i in range(1,10):
       if frequences[i] == 0: presences -= 1
    # Calcul du nombre des chiffres dans la grille
    nombre = 0
    for i in range(9):
       for j in range(9):
          if self.grille[i][j] != 0: nombre += 1
    # Calcul des cases binaires ou a candidats uniques
    uniques = 0
    binaires = 0
    for i in range(9):
       for j in range(9):
          if len(self.candidats[i][j]) == 1: uniques += 1
          if len(self.candidats[i][j]) == 2: binaires += 1
    # Calcul du nombre de liens forts
    liens = [0 for i in range(10)]
    for i in range(9):
       ligne = [0 for i in range(10)]
       colonne = [0 for i in range(10)]
       for j in range(9):
          ligne.extend(self.candidats[i][j])
          colonne.extend(self.candidats[j][i])
       for k in range(1,10):
          if ligne.count(k) == 2: liens[k] +=1
          if colonne.count(k) == 2: liens[k] +=1
    for b in range(9):
      x,y = (b//3)*3, (b%3)*3                     # base du bloc b ->  3*(b//3), 3*(b%3)
      bloc = []
      for i in range(3):
          for j in range(3):
              bloc.extend(self.candidats[x+i][y+j])
      for k in range(1,10):
          if bloc.count(k) == 2: liens[k] +=1
    # Calcul du total des liens forts
    total = 0
    for i in range(1,10):
       total = total + liens[i]
    # Renvoit un tuple avec les valeurs calculées
    return nombre, presences, frequences, uniques, binaires, liens, total
 

# ---------------------------------------------------------------------------------------------------------------
# Tests module
# ---------------------------------------------------------------------------------------------------------------

probleme = "560002030009007000030050000100000300650348092003000008000090050000700400040500079"
solution = "564982731819437625732651984198265347657348192423179568371894256985726413246513879"

test       = "030001005600000090090620000061090003000070000500030470000015080050000002900300040"
test2       = "400000090000250030200409806005100000000020500040000023000007960010000000026093004"
couverture = "703000005680702000000000800900800000007326400000009001004000000000203074100000206"
tt   = "003000400200000009000079000620000004010000050905040000100000285004000600057000900"
hard2 = "1...567.9...1.926.6..27..51...91...5.1.5.792.....62.17.34............5...6.7....."
hard = "100056709000109260600270051000910005010507920000062017034000000000000500060700000"

m118 = "9876.....6...54......8..6..8.9.3.76.3..........2...3.87..2..9.3.369..27........8."
n118 = "9876.....6...54......8..6..8.9.3.76.3..........2...3.87..9..2.3.362..97........8."

if __name__ == '__main__':
  g = Grille()
  g.set_grille_chaine(hard2)
  print(g.possibles())
  print(g.candidats)

  print(g.evaluer())

