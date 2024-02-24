class Grille:
  """   Modèle objet de Grille de Sudoku : Une grille est un tableau de dimension 9x9
  afficher()                      afficher la grille courante
  set_grille(grille)              entrer une grille comme tableau 9x9
  set_grille_chaine(chaine)       entrer une grille comme chaine 81 caractères
  valide()                        retourne True si la grille courante (complète) est valide
  permis(x,y,n)                   vérifie que le chiffre n est permis en x y retourne True False
  resoudre()                      résolution de la grille de sudoku (récursif)
  sauver(nom_fichier)             sauvegarder la grille courante comme une chaine de 81 caractères
  lire_chaine(nom_fichier)        lire une grille comme chaine de 81 caractères
  permuter(permutation)           remplacer chaque chiffre de la grille par un autre chiffre
  echanger(ligne_colonne, i, j)   echanger des lignes ou des colonnes dans une même bande
  deplacer(sens, indice)          echanger des bandes de blocs
  rotation()                      tourner la grille de 90 degrés - sens des aiguilles d'une montre

  """
  # Constructeur
  def __init__(self):                   # grille = [[0 for i in range(9)] for j in range(9)]
    self.grille = [                     # grille = [[0]*9 for i in range(9)]
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    self.nb = 0                                                 # nombre de solutions trouvées par resoudre()
    self.solution = [[0 for i in range(9)] for j in range(9)]   # utilisation: print(grille.solution)
  
  # Afficher la grille courante 9x9
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
  
  # Entrer une grille sous forme de chaine  len(chaine) = 81  (soit k position de 0 à 80 alors i = k//9 j = k%9)
  def set_grille_chaine(self, chaine):
    vecteur = list(map(lambda x: ord(x)-48, chaine))            # convertir alpha en chiffres 0 à 9
    for i in vecteur: 
       if vecteur[i] < 0 or vecteur[i] > 9: vecteur[i] = 0      # remplace par 0 les caractères non chiffres 0 à 9
    if len(vecteur) == 81:                                      # contrôle la longueur du vecteur
      for k in range(81):
        i = k//9      # floor(k/9)
        j = k - 9*i   # k%9
        self.grille[i][j] = vecteur[k]
    else:
       print("La chaine de caractères doit être composée de 81 caractère")
    
  # Entrer une grille sous forme de matrice 9x9 (a revoir l'adresse passée en paramètre)
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
  
  # résoudre la grille de sudoku
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
            print(self.grille[i][j], end="")
            self.solution[i][j] = self.grille[i][j]
        print()
      print("-------------------------", self.nb)


  # sauvegarde de la grille sous forme de chaine len = 81, case vide = 0
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

  # lire une grille sous forme de chaine
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

  # Permutation des chiffres de la grille  permutation = [0,8,7,1,2,3,6,9,4,5] (avec 0 initial)
  def permuter(self, permutation):
    tempo = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
       for j in range(9):
          tempo[i][j] = permutation[self.grille[i][j]]
    self.grille = tempo
    
  # Transposition
  def echanger(self):
     pass
  
  # Rotation de 90 degrés à droite, position de la cellule après rotation: i -> j et j -> 9 - i -1
  def rotation(self):
    tempo = [[0]*9 for i in range(9)]
    for i in range(9):
        for j in range(9):
      # Accéder à la cellule courante
          tempo[j][8-i] = self.grille[i][j]
    self.grille = tempo

# -----------------------------------------
# Tests module
# -----------------------------------------

probleme = "560002030009007000030050000100000300650348092003000008000090050000700400040500079"
solution = "564982731819437625732651984198265347657348192423179568371894256985726413246513879"

test       = "030001005600000090090620000061090003000070000500030470000015080050000002900300040"

couverture = "703000005680702000000000800900800000007326400000009001004000000000203074100000206"

