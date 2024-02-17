class Grille:
  """   Modèle objet de Grille de Sudoku : Une grille est un tableau de dimension 9x9
  afficher()                      afficher la grille courante
  set_grille(grille)              entrer une grille comme tableau 9x9
  set_grille_chaine(chaine)       entrer une grille comme chaine 81 caractères
  valide()                        retourne True si la grille courante est valide
  sauver(nom_fichier)             sauvegarder la grille courante comme une chaine de 81 caractères
  lire_chaine(nom_fichier)        lire une grille comme chaine de 81 caractères
  permuter(permutation)           remplacer chaque chiffre de la grille par un autre chiffre
  echanger(ligne_colonne, i, j)   echanger des lignes ou des colonnes dans une même bande
  deplacer(sens, indice)          echanger des blocs
 
   """
  # Constructeur
  def __init__(self):             # grille = [[0 for i in range(9)] for j in range(9)]
    self.grille = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
  
  # Afficher la grille
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
  
  # Entrer une grille sous forme de chaine  len(chaine) = 81
  def set_grille_chaine(self, chaine):
    vecteur = list(map(lambda x: ord(x)-48, chaine))
    for k in range(81):
      i = k//9    # floor(k/9)  # k//9 idem
      j = k - 9*i
      self.grille[i][j] = vecteur[k]
    
  # Entrer une grille sous forme de matrice 9x9
  def set_grille(self, tableau):
    self.grille = tableau
  
  # Valider la grille courante, renvoit True ou False
  def valide(self):
    # Vérifier les lignes et colonnes
    for i in range(9):
      ligne = set(self.grille[i])
      colonne = set(self.grille[j][i] for j in range(9))
      if ligne != set(range(1, 10)) or colonne != set(range(1, 10)):    # plus vite ? suite = {1,2,3,4,5,6,7,8,9}
          return False
    # Vérifier les blocs 3x3
    for i in range(0, 9, 3):
      for j in range(0, 9, 3):
          bloc = []
          for k in range(3):
              for l in range(3):
                  bloc.append(self.grille[i+k][j+l])
          if set(bloc) != set(range(1, 10)):
              return False
    return True
  
  # sauvegarde de la grille
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

  # Permutation des chiffres de la grille  permutation = [0,8,7,1,2,3,6,9,4,5]
  def permuter(self, permutation):
    tempo = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
       for j in range(9):
          tempo[i][j] = permutation[self.grille[i][j]]
    self.grille = tempo
    
  # Transposition
  def echanger(self):
     pass
# -----------------------------------------
# Tests module
# -----------------------------------------

grille = Grille()
r = grille.valide()
if r: 
   print("vrai")
else:
   print("faux")