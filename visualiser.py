import tkinter as tk
    
# Affichage d'une grille de Sudoku dans une fenetre tkinter

class Case(tk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(font=('Helvetica', 16, "bold"), justify='center')

class SudokuGrid(tk.Frame):
    def __init__(self, master, grille):
        super().__init__(master)
        self.grille = grille
        self.grille = [[0]*9 for i in range(9)]
        self.grille = [
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
        self.grid_propagate(False)
        self.create_grid()
    
    def create_grid(self):
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)  # Poids pour étirer verticalement
            for j in range(3):
                self.grid_columnconfigure(j, weight=1)  # Poids pour étirer horizontalement
                frame = tk.Frame(self, borderwidth=1, relief='solid')
                frame.grid(row=i, column=j, sticky='nsew')
                self.create_subgrid(frame, i, j)

    def create_subgrid(self, master, x, y):
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)           # Poids pour étirer verticalement
            for j in range(3):
                master.grid_columnconfigure(j, weight=1)    # Poids pour étirer horizontalement
                case = Case(master, width = 2)
                case.grid(row=i, column=j, sticky='nsew')
                a = i+3*x
                b = j+3*y
                if self.grille[a][b] != 0:
                    case.insert(tk.END, str(self.grille[a][b]))
                    case.config(state='disabled')

# Utilisation du module:

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
root = tk.Tk()
root.title("Grille de Sudoku")
root.geometry("400x400")

# Encadrement du conteneur principal avec une bordure noire
frame = tk.Frame(root, borderwidth=2, relief='solid')
frame.pack(expand=True, fill='both')

# Grille de Sudoku
sudoku_grid = SudokuGrid(frame, grid)
sudoku_grid.pack(expand=True, fill='both')

root.mainloop()


