def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

def is_safe(grid, row, col, num):
    # Vérifier la ligne
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # Vérifier la colonne
    for y in range(9):
        if grid[y][col] == num:
            return False
    
    # Vérifier le carré 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for x in range(3):
        for y in range(3):
            if grid[start_row + x][start_col + y] == num:
                return False
    
    return True

def solve_sudoku(grid):
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True  # La grille est remplie
    
    row, col = empty_cell

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku(grid):
                return True

            grid[row][col] = 0  # Annuler l'attribution si le chiffre ne convient pas
    
    return False  # Aucune solution trouvée

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

# Exemple de grille Sudoku partiellement remplie (0 pour les cases vides)
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if solve_sudoku(grid):
    print("Grille de Sudoku résolue :")
    print_grid(grid)
else:
    print("Aucune solution trouvée pour cette grille.")
