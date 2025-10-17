import tkinter as tk
from tkinter import messagebox
import random
import time

# Global variables to maintain game state
grid = [[0 for _ in range(9)] for _ in range(9)]
solution = [[0 for _ in range(9)] for _ in range(9)]
original_puzzle = [[0 for _ in range(9)] for _ in range(9)]
start_time = None
timer_running = False
timer_id = None

# Global UI elements
cells = []
timer_label = None
status_label = None
root = None

def setup_ui():
    global root, timer_label, status_label
    
    # Title
    title_label = tk.Label(root, text="Sudoku Game", 
                          font=("Arial", 20, "bold"), fg="darkblue")
    title_label.pack(pady=10)
    
    # Timer display
    timer_frame = tk.Frame(root)
    timer_frame.pack(pady=5)
    
    tk.Label(timer_frame, text="Time:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
    timer_label = tk.Label(timer_frame, text="00:00", 
                           font=("Arial", 12, "bold"), fg="red")
    timer_label.pack(side=tk.LEFT, padx=5)
    
    # Status label
    status_label = tk.Label(root, text="Fill in the numbers!", 
                            font=("Arial", 10), fg="green")
    status_label.pack(pady=5)
    
    # Sudoku grid frame
    grid_frame = tk.Frame(root, relief=tk.RAISED, bd=2)
    grid_frame.pack(pady=10)
    
    # Create 9x9 grid of cells
    create_grid(grid_frame)
    
    # Control buttons
    create_control_buttons()

def create_grid(parent):
    global cells
    
    cells = []
    
    for i in range(9):
        row = []
        for j in range(9):
            # Create frame for each cell
            cell_frame = tk.Frame(parent, relief=tk.RAISED, bd=1, 
                                bg="white", width=50, height=50)
            cell_frame.grid(row=i, column=j, padx=1, pady=1)
            cell_frame.pack_propagate(False)
            
            # Create entry widget for each cell
            cell = tk.Entry(cell_frame, font=("Arial", 16, "bold"), 
                          justify="center", width=2, bd=0)
            cell.pack(fill=tk.BOTH, expand=True)
            
            # Bind events
            cell.bind('<KeyPress>', lambda e, r=i, c=j: on_key_press(e, r, c))
            cell.bind('<Button-1>', lambda e, r=i, c=j: on_cell_click(r, c))
            cell.bind('<FocusIn>', lambda e, r=i, c=j: on_cell_focus(r, c))
            
            row.append(cell)
        cells.append(row)
    
    # Add thicker borders for 3x3 boxes
    add_box_borders()

def add_box_borders():
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # Top border
            if i > 0:
                for k in range(3):
                    cells[i][j+k].master.configure(relief=tk.RAISED, bd=2)
            
            # Left border
            if j > 0:
                for k in range(3):
                    cells[i+k][j].master.configure(relief=tk.RAISED, bd=2)
            
            # Bottom border
            if i < 6:
                for k in range(3):
                    cells[i+2][j+k].master.configure(relief=tk.RAISED, bd=2)
            
            # Right border
            if j < 6:
                for k in range(3):
                    cells[i+k][j+2].master.configure(relief=tk.RAISED, bd=2)

def create_control_buttons():
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    # Button styles
    button_style = {"font": ("Arial", 12, "bold"), "width": 10, "height": 2}
    
    # New Game button
    new_btn = tk.Button(button_frame, text="New Game", 
                       command=generate_new_puzzle, bg="lightgreen", **button_style)
    new_btn.pack(side=tk.LEFT, padx=5)
    
    # Check button
    check_btn = tk.Button(button_frame, text="Check", 
                         command=check_solution, bg="lightblue", **button_style)
    check_btn.pack(side=tk.LEFT, padx=5)
    
    # Solve button
    solve_btn = tk.Button(button_frame, text="Solve", 
                         command=solve_puzzle, bg="orange", **button_style)
    solve_btn.pack(side=tk.LEFT, padx=5)
    
    # Clear button
    clear_btn = tk.Button(button_frame, text="Clear", 
                        command=clear_user_input, bg="lightcoral", **button_style)
    clear_btn.pack(side=tk.LEFT, padx=5)

def generate_new_puzzle():
    global grid, solution, original_puzzle
    
    # Stop current timer
    stop_timer()
    
    # Clear all grids completely
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[0 for _ in range(9)] for _ in range(9)]
    original_puzzle = [[0 for _ in range(9)] for _ in range(9)]
    
    # Clear the UI display first
    clear_ui_display()
    
    # Generate complete solution
    generate_complete_solution()
    
    # Create puzzle by removing some numbers
    create_puzzle()
    
    # Update UI
    update_grid_display()
    
    # Start timer
    start_timer()
    
    # Update status
    status_label.config(text="New puzzle generated! Good luck!", fg="green")

def generate_complete_solution():
    global solution
    
    # Clear the grid
    solution = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the grid using backtracking
    success = fill_grid(solution)
    
    # Verify the solution is valid
    if not success or not is_valid_solution(solution):
        # If generation failed, try again
        generate_complete_solution()

def fill_grid(grid_to_fill):
    # Find the next empty cell
    for row in range(9):
        for col in range(9):
            if grid_to_fill[row][col] == 0:
                # Try each number from 1 to 9
                values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                random.shuffle(values)  # Randomize for variety
                
                for test_val in values:
                    if is_valid_placement(test_val, row, col, grid_to_fill):
                        grid_to_fill[row][col] = test_val
                        
                        # Recursively try to fill the rest
                        if fill_grid(grid_to_fill):
                            return True
                        
                        # If this path didn't work, backtrack
                        grid_to_fill[row][col] = 0
                
                # If no number worked for this cell, backtrack
                return False
    
    # If we get here, the grid is filled
    return True

def is_valid_placement(num, row, col, grid_to_check):
    # Check row
    if num in grid_to_check[row]:
        return False
    
    # Check column
    for i in range(9):
        if grid_to_check[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    
    for i in range(3):
        for j in range(3):
            if grid_to_check[box_row + i][box_col + j] == num:
                return False
    
    return True

def create_puzzle():
    global grid, original_puzzle
    
    # Copy solution to puzzle
    grid = [row[:] for row in solution]
    original_puzzle = [row[:] for row in solution]
    
    # Remove numbers to create puzzle (adjust difficulty by changing number of removals)
    cells_to_remove = random.randint(40, 50)  # Remove 40-50 numbers
    removed_positions = set()
    
    while len(removed_positions) < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if (row, col) not in removed_positions:
            grid[row][col] = 0
            original_puzzle[row][col] = 0
            removed_positions.add((row, col))

def clear_ui_display():
    for i in range(9):
        for j in range(9):
            cell = cells[i][j]
            cell.delete(0, tk.END)
            cell.config(state="normal", bg="white", fg="black")

def update_grid_display():
    for i in range(9):
        for j in range(9):
            cell = cells[i][j]
            value = grid[i][j]
            
            if value == 0:
                # Empty cell - should be editable
                cell.delete(0, tk.END)
                cell.config(state="normal", bg="white", fg="black")
            else:
                # Non-empty cell - check if it's from original puzzle or user input
                cell.delete(0, tk.END)
                cell.insert(0, str(value))
                
                # If this cell was in the original puzzle, make it readonly
                if original_puzzle[i][j] != 0:
                    cell.config(state="readonly", bg="lightgray", fg="black")
                else:
                    # This is user input - make it editable
                    cell.config(state="normal", bg="lightyellow", fg="black")

def update_solution_display():
    for i in range(9):
        for j in range(9):
            cell = cells[i][j]
            value = grid[i][j]
            
            if value == 0:
                # Empty cell
                cell.delete(0, tk.END)
                cell.config(state="normal", bg="white", fg="black")
            else:
                # Non-empty cell - make all readonly when showing solution
                cell.delete(0, tk.END)
                cell.insert(0, str(value))
                cell.config(state="readonly", bg="lightblue", fg="black")

def on_key_press(event, row, col):
    # Only allow numbers 1-9
    if event.char.isdigit() and event.char in "123456789":
        # Prevent the default behavior to avoid double input
        event.widget.delete(0, tk.END)
        event.widget.insert(0, event.char)
        # Update the grid
        grid[row][col] = int(event.char)
        # Move to next cell
        move_to_next_cell(row, col)
        # Check if puzzle is complete
        check_completion()
        return "break"  # Prevent further processing
    elif event.keysym == "BackSpace":
        # Handle backspace
        event.widget.delete(0, tk.END)
        grid[row][col] = 0
        return "break"  # Prevent further processing
    elif event.keysym in ["Up", "Down", "Left", "Right"]:
        # Handle arrow keys
        handle_arrow_keys(event.keysym, row, col)
        return "break"  # Prevent further processing
    else:
        # Block all other characters
        return "break"

def on_cell_click(row, col):
    # Only allow editing if it's not a pre-filled cell
    if original_puzzle[row][col] == 0:
        cells[row][col].config(state="normal", bg="lightyellow")
        cells[row][col].focus_set()

def on_cell_focus(row, col):
    if original_puzzle[row][col] == 0:
        cells[row][col].config(bg="lightyellow")

def move_to_next_cell(row, col):
    # Try to find next empty cell
    for i in range(row, 9):
        start_col = col + 1 if i == row else 0
        for j in range(start_col, 9):
            if original_puzzle[i][j] == 0:
                cells[i][j].focus_set()
                return
    
    # If no empty cell found, focus on current cell
    cells[row][col].focus_set()

def handle_arrow_keys(direction, row, col):
    """Handle arrow key navigation"""
    if direction == "Up" and row > 0:
        cells[row-1][col].focus_set()
    elif direction == "Down" and row < 8:
        cells[row+1][col].focus_set()
    elif direction == "Left" and col > 0:
        cells[row][col-1].focus_set()
    elif direction == "Right" and col < 8:
        cells[row][col+1].focus_set()

def check_solution():
    """Check if the current solution is valid"""
    # Check if all cells are filled
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                messagebox.showwarning("Incomplete", "Please fill in all cells first!")
                return
    
    # Check validity
    if is_valid_solution():
        messagebox.showinfo("Valid!", "Congratulations! Your solution is correct!")
        stop_timer()
        status_label.config(text="Puzzle solved correctly!", fg="green")
    else:
        messagebox.showerror("Invalid", "Your solution has errors. Please check again.")
        status_label.config(text="Solution has errors. Keep trying!", fg="red")

def is_valid_solution(grid_to_check=None):
    if grid_to_check is None:
        grid_to_check = grid
        
    # Check rows
    for row in grid_to_check:
        if len(set(row)) != 9 or 0 in row:
            return False
    
    # Check columns
    for col in range(9):
        column = [grid_to_check[row][col] for row in range(9)]
        if len(set(column)) != 9 or 0 in column:
            return False
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(grid_to_check[box_row + i][box_col + j])
            if len(set(box)) != 9 or 0 in box:
                return False
    
    return True

def solve_puzzle():
    """Show the complete solution"""
    global grid
    
    if messagebox.askyesno("Solve Puzzle", "Are you sure you want to see the solution?"):
        # Copy solution to grid
        grid = [row[:] for row in solution]
        
        # Update display with all cells readonly (since we're showing solution)
        update_solution_display()
        
        # Stop timer
        stop_timer()
        
        # Update status
        status_label.config(text="Solution revealed!", fg="blue")

def clear_user_input():
    """Clear all user input while keeping the original puzzle"""
    global grid
    
    if messagebox.askyesno("Clear Input", "Are you sure you want to clear all your input?"):
        # Reset grid to original puzzle
        grid = [row[:] for row in original_puzzle]
        
        # Update display
        update_grid_display()
        
        # Reset timer
        start_timer()
        
        # Update status
        status_label.config(text="Input cleared. Try again!", fg="orange")

def start_timer():
    global start_time, timer_running
    start_time = time.time()
    timer_running = True
    update_timer()

def stop_timer():
    global timer_running, timer_id
    timer_running = False
    if timer_id:
        root.after_cancel(timer_id)

def update_timer():
    global timer_id
    if timer_running:
        elapsed = int(time.time() - start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        timer_id = root.after(1000, update_timer)

def check_completion():
    # Check if all cells are filled
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return
    
    # Check if solution is valid
    if is_valid_solution():
        stop_timer()
        elapsed = int(time.time() - start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        messagebox.showinfo("Congratulations!", 
                          f"Puzzle solved correctly!\nTime: {minutes:02d}:{seconds:02d}")
        status_label.config(text=f"Solved in {minutes:02d}:{seconds:02d}!", fg="green")

def main():
    global root
    
    root = tk.Tk()
    root.title("Sudoku Game")
    root.geometry("600x700")
    root.resizable(False, False)
    
    setup_ui()
    generate_new_puzzle()
    
    root.mainloop()

if __name__ == "__main__":
    main()