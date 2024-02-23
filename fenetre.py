from tkinter import *
from tkinter.scrolledtext import ScrolledText

class Fenetre(Tk):
    def __init__(self):
        super().__init__()
        self.initialiser()
        self.geometry("400x300")
        self.grid()

    def initialiser(self):
        label = Label(self, text="test")
        #label.grid(row=0, column=1)
        self.title("Grille 9x9")
        txt = 1

    def afficher_grille(self):
        tableau = []
        for i in range(9):
            ligne = []
            for j in range(9):
                # Créer un bouton
                bouton = Button(self, text=f"{i+1},{j+1}")
                # Définir la position du bouton dans la grille
                bouton.grid(row=i, column=j)
                ligne.append(bouton)
                tableau.append(ligne)
        #bouton = Button(self, text="Quitter", command=self.destroy)
        #bouton.grid(row=30, column=0)
        print(tableau)

# Démarrage de l'application
if __name__ == "__main__":
  app = Fenetre()
  app.afficher_grille()

  app.mainloop()
  
