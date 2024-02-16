class Grille:
  """      Modèle objet de Grille de Sudoku : Une grille est un tableau de dimension 9x9
  afficher()                      afficher la grille courante
  set_grille(grille)              entrer une grille comme tableau 9x9
  set_grille_chaine(chaine)       entrer une grille comme chaine 81 caractères
  sauver(nom_fichier)             sauvegarder la grille courante comme une chaine de 81 caractères
  lire_chaine(nom_fichier)        lire une grille comme chaine de 81 caractères
  """
  # Constructeur
  def __init__(self):             # grille = [[0 for i in range(9)] for j in range(9)]
    self.grille = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
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



# -----------------------------------------
# Tests module
# -----------------------------------------

grille = Grille()

grille.afficher()
print("***************************")

chaine = "123456789123456789123456789123456789123456789123456789123456789123456789123456789"

grille.set_grille_chaine(chaine)

grille.afficher()
 
grille.sauver("test")


