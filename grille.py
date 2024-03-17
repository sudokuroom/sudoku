from visualiser import *
from math import *
import random
from statistics import *


# ---------------------------------------------------------------------------------------------------------------
class Grille:
  """   Modèle objet de Grille de Sudoku : Une grille est un tableau de dimension 9x9
  afficher()                      afficher la grille courante
  afficher_solution()             afficher la solution
  visualiser()                    afficher la grille courante dans une fenêtre tkinter
  verification()                  retourne True si la grille courante (partielle) est valide (pas de doublons)
  valide()                        retourne True si la grille courante (complète) est valide 
  permis(x,y,n)                   vérifie que le chiffre n est permis en x y retourne True False
  possibles()                     calcul des candidats dans chaque case vide -> candidats[][]
  resoudre()                      résolution de la grille de sudoku (récursif) -> nb, solution
  sauver(nom_fichier)             sauvegarder la grille courante comme une chaine de 81 caractères
  lire_chaine(nom_fichier)        lire une grille comme chaine de 81 caractères
  permuter(permutation)           remplacer chaque chiffre de la grille par un autre chiffre
  rotation()                      tourner la grille de 90 degrés - sens des aiguilles d'une montre
  generer()                       générer aléatoirement une grille complète
  evaluer()                       calculer les principaux paramètres d'une grille
  compléter()                     remplir la grille selon cases et secteurs à candidat unique
  """
  # ---------------------------------------------------------------------------------------------------------------
  # Constructeur
  # ---------------------------------------------------------------------------------------------------------------
  def __init__(self):                                                                
    self.grille = [[0]*9 for i in range(9)]                      # grille de Sudoku, présumée incomplète
    self.solution = [[0 for i in range(9)] for j in range(9)]    # grille solution, grille complète
    self.nb = 0                                                  # nombre de solutions trouvées par resoudre()
    self.candidats = [[[] for i in range(9)] for j in range(9)]  # candidats dans les cases vides (type = list)
    self.tempo = [] # grille de travail

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
  
  # ---------------------------------------------------------------------------------------------------------------
  # Visualiser la grille courante dans une fenetre tkinter
 # ---------------------------------------------------------------------------------------------------------------
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

  # ---------------------------------------------------------------------------------------------------------------     
  # Entrer une grille sous forme de chaine  len(chaine) = 81  (soit k position de 0 à 80 alors i = k//9 j = k%9)
  # ---------------------------------------------------------------------------------------------------------------
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

  # ---------------------------------------------------------------------------------------------------------------
  # Vérifier si la grille complète est valide (ne traite pas les grilles partielles)
  # ---------------------------------------------------------------------------------------------------------------
  def valide(self)-> bool:
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

  # ---------------------------------------------------------------------------------------------------------------  
  # Verifier si une grille partielle est valide (aucun doublon dans aucun secteur)
  # ---------------------------------------------------------------------------------------------------------------
  def verification(self)-> bool:
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

  # ---------------------------------------------------------------------------------------------------------------
  # Vérifier si n est permis dans la case x y  {assertion: la case x y est vide}
  # ---------------------------------------------------------------------------------------------------------------
  def permis(self,x,y,n)-> bool:
      #assert self.grille[x][y] == 0, "appel de permis() avec une case non vide"
      for k in range(9):
          if self.grille[x][k] == n: return False     # parcours ligne
          if self.grille[k][y] == n: return False     # parcours colonne
      x0, y0 = (x//3)*3, (y//3)*3                     # base du bloc 3x3 de x y
      for i in range(3):
          for j in range(3):
              if self.grille[x0+i][y0+j] == n: return False
      return True

  # ---------------------------------------------------------------------------------------------------------------  
  # Calcule les candidats possibles dans chaque case et remplit candidats[][]
  # ---------------------------------------------------------------------------------------------------------------
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
  # résoudre la grille de sudoku: grille -> nb, solution  (recursif)
  # ---------------------------------------------------------------------------------------------------------------
  def resoudre(self):
      if self.nb > 1: return      
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
            self.solution[i][j] = self.grille[i][j]           # à la fin self.grille n'est pas modifiée
      
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
  # Generation d'une grille aléatoire partielle indices = nombre des dévoilés
  # ---------------------------------------------------------------------------------------------------------------
  def generer(self):
    indices = 20
    random.seed()
    while True:
        self.grille = [[0 for i in range(9)] for j in range(9)]
        self.nb = 0
        for n in range(indices):
            i, j = random.randint(0, 8), random.randint(0, 8)
            while self.grille[i][j] != 0:
               i, j = random.randint(0, 8), random.randint(0, 8)
            for k in random.sample(range(1,10),9):
               if self.permis(i,j,k):
                  break
            self.grille[i][j] = k
        print(self.grille)
        print("on a trouve une grille")
        chiffres = set([self.grille[i][j] for i in range(9) for j in range(9)])
        if len(chiffres) > 8:
            self.completer()
            self.optimiser()
            # self.resoudre()
            if self.nb == 1: 
               break
            else: print("essai infructueux")
        else:
           print("moins de 8 chiffres")
      
  # ---------------------------------------------------------------------------------------------------------------     
  # Evaluation de la grille courante, calcul des paramètres courants
  # ---------------------------------------------------------------------------------------------------------------
  def evaluer(self) -> tuple:
    # calculer les candidats
    self.possibles()
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
    return nombre, presences, frequences, pstdev(frequences[1:]), uniques, binaires, liens, total, pstdev(liens[1:])
  
  # ---------------------------------------------------------------------------------------------------------------
  # Compléter la grille en placant les cases et les secteurs à candidat unique
  # ---------------------------------------------------------------------------------------------------------------
  def completer(self):   
     # recherche des cases et secteurs à candidat unique
     while True:
        self.possibles()
        modifie = False
        # recherche des cases à candidat unique
        for i in range(9):
          for j in range(9):
            liste = self.candidats[i][j]
            if len(liste) == 1:
              self.grille[i][j] = liste[0] 
              modifie = True           
        # recherche des lignes à candidat unique
        for i in range(9):                          # parcours des lignes et colonnes
           ligne = [[] for i in range(10)]          
           for j in range(9):                       # explorer la ligne par case
              for k in range(1,10):                 # parcourir les candidats
                 if k in self.candidats[i][j]:
                    ligne[k].append((i,j))          # on recence toutes les cases qui contiennent k                
           for k in range(1,10):
              if len(ligne[k]) == 1:                # le chiffre k est présent dans une seule case
                 x,y = ligne[k][0]
                 self.grille[x][y] = k              # placer le chiffre k
                 modifie = True    
        # recherche des colonnes à candidat unique
        for i in range(9):                          # parcours des colonnes           
           colonne = [[] for i in range(10)]
           for j in range(9):                       # explorer la ligne par case
              for k in range(1,10):                 # parcourir les candidats
                 if k in self.candidats[j][i]:
                    colonne[k].append((j,i))
           for k in range(1,10):                    # si on fusionne li/col le résultat sera différent
              if len(colonne[k]) == 1:              # parce que l'ordre des opérations est différent !
                 x,y = colonne[k][0]
                 self.grille[x][y] = k
                 modifie = True   
       # recherche des blocs à candidat unique    
        for b in range(9):
          x,y = (b//3)*3, (b%3)*3                     # base du bloc b ->  3*(b//3), 3*(b%3)
          bloc = [[] for i in range(10)]              # génère [ [], [] ... ,[] ]
          for i in range(3):
            for j in range(3):
              for k in range(1,10):
                if k in self.candidats[x+1][y+j]:
                   bloc[k].append((x+i,y+j))
          for k in range(1,10):
             if len(bloc[k]) == 1:
                i,j = bloc[k][0]
                self.grille[i][j] = k
                modifie = True

        if modifie == False:
           break
          
     
  # ---------------------------------------------------------------------------------------------------------------
  # QuickSolve backtracking itératif opère sur une liste de cases vides triées par nbre candidats
  # ---------------------------------------------------------------------------------------------------------------
  def quicksolve(self):
      # remplir la pile avec les cases vides en allant de (0,0) à (8,8)
      self.travail = self.grille.copy()
      cases = [(-1,-1)]                                   # cases contient les cases vides
      chiffre = [-1]                                      # chiffre contiendra le chiffre essayé dans la case
      self.possibles()                                    # calcul tous les candidats pour ordonner les tables
      ptr = 1                                             # ptr est le pointeur de pile
      for i in range(9):
        for j in range(9):
            if self.grille[i][j] == 0:                      # case vide 
              cases.append((i,j))                           # ajouter la case vide dans cases comme tuple
              chiffre.append(len(self.candidats[i][j]))     # chiffre contient le nombre des candidats de (i,j)
              ptr += 1
      N = len(cases)-1                                      # N sera la hauteur de la pile de 1 à N      
      # trier la pile par ordre de valeur croissante
      for i in range(2,N+1):                                # tri par insertion (maximum 80 cases)
        tempo = chiffre[i]
        cell = cases[i]
        j = i -1
        while j >= 1 and chiffre[j] > tempo:                # decalage vers le haut
            chiffre[j+1] = chiffre[j]
            cases[j+1] = cases[j]
            j = j -1
        chiffre[j+1] = tempo                                # mettre la valeur dans sa place
        cases[j+1] = cell
      chiffre = [0 for i in range(N+1)]                     # quand la pile est triée remettre à zéro chiffre[]      
      # backtracking itératif     
      ptr = 1                                             # Pointeur de pile initialisé à 1
      compteur = 0                                        # compteur de solutions trouvées
      while ptr > 0:                                      # assert chiffre[ptr] == 0
          if ptr > N:                        
                 compteur += 1                            # assert ptr == N  on a trouvé une solution                
                 ptr -= 1                                 #  on remonte d'un cran pas de maj a ce niveau N+1          
                 if compteur > 1:                         # tout arrêter si on a trouvé plus d'une solution
                    break
          else:                                           # assert chiffre[ptr] == 0 il faut trouver un chiffre possible
              valeur = chiffre[ptr]+1
              trouve = False                              #  trouve = on a trouve un chiffre valide
              i, j = cases[ptr]                           #  case que l'on teste
              while valeur < 10:               
                 if self.permis(i,j, valeur):             # boucle pour essayer tous les chiffres
                    trouve = True
                    break
                 else:
                    valeur += 1                 
              if trouve:
                  chiffre[ptr] = valeur                    # Mettre à jour la valeur du nœud dans la pile
                  i, j = cases[ptr]
                  self.grille[i][j] = valeur
                  ptr += 1                                 # Descendre d'un niveau dans la pile                
              else:
                  chiffre[ptr] = 0                         # Remettre la cellule à zéro
                  i, j = cases[ptr]
                  self.grille[i][j] = 0
                  ptr -= 1        
      return compteur 

  # place en première ligne la colonne la plus peuplée (aussi en échangeant les 3 premières lignes)
  def optimiser(self):
     a = 0
     b = 0
     for i in range(3):
        for j in range(9):
           if self.grille[0][j] != 0: a += 1
           if self.grille[j][0] != 0: b += 1
        if b >= a:
           self.rotation()

# ---------------------------------------------------------------------------------------------------------------
# Tests module
# ---------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
  g = Grille()
  # mutiples solutions
  g.grille = [[0, 0, 8, 0, 0, 0, 0, 0, 0], 
[0, 0, 2, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 3, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 2, 0, 0], 
[2, 0, 0, 6, 0, 1, 0, 0, 4], 
[0, 0, 7, 0, 0, 0, 8, 1, 0], 
[0, 1, 0, 3, 8, 0, 0, 7, 0], 
[4, 0, 6, 9, 2, 0, 5, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0]]
  #g.completer()
  #g.optimiser()
  g.grille = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 1, 0, 0, 0, 0], [0, 0, 0, 9, 7, 0, 0, 3, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [9, 0, 5, 0, 0, 0, 0, 0, 2], [0, 0, 1, 0, 3, 0, 4, 0, 0], [0, 4, 0, 0, 0, 0, 2, 0, 7], [0, 9, 0, 0, 0, 0, 0, 0, 8]]
  #g.set_grille_chaine("560002030009007000030050000100000300650348092003000008000090050000700400040500079")
  g.afficher()
  print("***")
  g.completer()

  print(g.quicksolve())
  
  g.afficher()
  print(g.solution)
  

  """g.grille = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 1, 0, 0, 0, 0], 
            [0, 0, 0, 9, 7, 0, 0, 3, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [9, 0, 5, 0, 0, 0, 0, 0, 2], [0, 0, 1, 0, 3, 0, 4, 0, 0], [0, 4, 0, 0, 0, 0, 2, 0, 7], 
            [0, 9, 0, 0, 0, 0, 0, 0, 8]]
"""

 

  """g.set_grille_chaine(imposs)
  g.grille = [[2, 0, 0, 0, 0, 1, 7, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 3, 6, 0, 0], [0, 0, 0, 0, 1, 0, 8, 0, 0], [0, 0, 2, 0, 3, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], 
           [0, 1, 0, 0, 0, 0, 4, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 3, 0, 0]]
  g.grille = [
    [0, 0, 0, 0, 0, 0, 4, 0, 3],
    [0, 0, 0, 0, 0, 4, 0, 9, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 2, 9, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 5, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 2, 7, 0, 0, 0, 0, 1],
    [4, 0, 3, 0, 0, 6, 0, 0, 0]
]"""
  

