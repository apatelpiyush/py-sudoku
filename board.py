import random
from tabulate import tabulate 

# === Sudoku Constraint Checks: The Three Pillars ===

def Row(x, row, grid):
    # It verifies if  x is already vertically present 
    # The value to accept from 1 to 9
    # The row index is from 0 to 8
    # If the number is not safe then True, otherwise False

    if x in grid[row]:
        return True
    else:
        return False

def Col(x, col, grid):    
    # It verifies if x is already vertically present 
    # The value to accept from 1 to 9
    # The row index is from 0 to 8
    # The 9x9 Sudoku matrix.
    # If the number is not safe then True, otherwise False
    colList = []
    for i in range(9):
        colList.append(grid[i][col])
    if x in colList:
        return True
    else:
        return False

def Square(x, row, col, grid):
    # Verifies if x is present within its local part.
    # The value to validate from 1 to 9.
    # If the number is not safe then True, otherwise False
    square = []

    if row < 3:
        if col < 3:
            square = [grid[i][0:3] for i in range(0, 3)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(0, 3)]
        else:
            square = [grid[i][6:9] for i in range(0, 3)]
    elif row < 6:
        if col < 3:
            square = [grid[i][0:3] for i in range(3, 6)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(3, 6)]
        else:
            square = [grid[i][6:9] for i in range(3, 6)]
    else:
        if col < 3:
            square = [grid[i][0:3] for i in range(6, 9)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(6, 9)]
        else:
            square = [grid[i][6:9] for i in range(6, 9)]

    return bool(x in square[0]+square[1]+square[2])


def isGridFilled(grid):

    # Checks if the entire 9x9 grid has been successfully populated, 
    # If complete True otherwise False 

    # Quick and clean check: return True if every row has no '0'.
    for r in range(9):
        for c in range(9):
            if grid[r][c]==0:
                return False
    else:
        return True


def fillGrid(grid):
    # Recursively attempts to find a valid solution by iterating through empty cells
    # and testing all numbers from 1 to 9 . If a path fails, it triggers the crucial
    # backtracking step.
    # If a solution is found then True otherwise False

    values= [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Find the next empty cell (value == 0) to fill.
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0:
                
                # Shuffling ensures a new, unique puzzle is generated each time.
                random.shuffle(values)
                
                for testVal in values:
                    a=Row(testVal, row, grid)
                    b=Col(testVal, col, grid)
                    c=Square(testVal, row, col, grid)

                    # debug 1 Corrected the logical typo (b == False -> c == False)
                    # HereiIf all three constraints are satisfied that is all are not True, the function get executed
                    if not a and not b and not c:
                        
                        # Tentative placement: Commit the valid number to the grid.
                        grid[row][col] = testVal

                        # Recurse: Try to fill the NEXT empty cell.
                        if fillGrid(grid):
                            # Success! The sub-problem worked out. Propagate success.
                            return True
                        
                # If the inner loop finishes, it means all 9 numbers failed for this cell.
                # Here the 'break' statement has been REMOVED here.
                # Here the indentation to execute this step immediately after the inner loop fails so we change.

                grid[row][col]=0
                return False

    return True 


grid = []
for i in range(9):
    # Initialize the 9x9 grid with zeros so that it actually initialises.
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

# Call the function to run the final code and fill in the grid with numbers and after getting output check if everything is correct.
fillGrid(grid)

def Printgrid(Grid):
    # Presents the finalized Sudoku solution in a clean, professional grid format.
    # It finally forms a 9x9 solved grid.

    print(" Sudoku Grid")
    print(tabulate(grid,tablefmt="fancy_grid"))

Printgrid(grid)