import random

import tkinter as tk 

from collections import deque # Import deque for BFS

CELL_SIZE = 30 # Size of each cell in the maze

def create_maze(rows, cols):
    # Create the maze initialized with walls ('#')
    maze = [['#' for _ in range(cols)] for _ in range(rows)]

    # Define the start and end points
    start_row = 0
    start_col = 0
    end_row = rows - 1
    end_col = cols - 1

    # Set the start and end points in the maze
    maze[start_row][start_col] = 'S'
    maze[end_row][end_col] = 'E'


    # Create a simple random path from 'S' to 'E'
    current = (start_row, start_col)
    path = [current]

    # Create a simple random path from S to E
    while current != (end_row, end_col): 
        directions = []
        if current[0] < end_row:
            directions.append((1, 0))  # Move down
        if current[1] < end_col:
            directions.append((0, 1))  # Move right
        if directions:
            move = random.choice(directions)
            current = (current[0] + move[0], current[1] + move[1]) #the current position is updated to the new position
            path.append(current)
            if current != (end_row, end_col):
                maze[current[0]][current[1]] = ' '


    # Set the end point
    maze[end_row][end_col] = 'E'

# Randomly add walls to the maze
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in path:
                if random.random() > 0.5:  # 50% chance of wall
                    maze[i][j] = ' '

    return maze


def print_maze(maze):
    for row in maze:
        print(' '.join(row)) # Print each row of the maze

def bfs(maze, show_path=True):
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    neighbors_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    parent = {}

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for direction in neighbors_directions:
            new_row = current[0] + direction[0]
            new_col = current[1] + direction[1]
            new_pos = (new_row, new_col)

            if 0 <= new_row < rows and 0 <= new_col < cols:
                if maze[new_row][new_col] != '#' and new_pos not in visited:
                    queue.append(new_pos)
                    visited.add(new_pos)
                    parent[new_pos] = current

    if end in parent:
        if show_path:
            path = []
            current = end
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()

            for pos in path:
                if maze[pos[0]][pos[1]] not in ('S', 'E'):
                    maze[pos[0]][pos[1]] = '.'
            print("Path found!")
        return True
    else:
        if show_path:
            print("No path found.")
        return False

if __name__ == "__main__":
    rows = 26
    cols = 48

    while True:
        maze = create_maze(rows, cols)
        temp_maze = [row[:] for row in maze]
        if bfs(temp_maze, show_path=False):
            break

    print("Original Maze:")
    print_maze(maze)

    bfs(maze)  # Show the path on the real maze

    print("\nMaze with Path (if found):")
    print_maze(maze)

class MazeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Generator and Solver")

        # Welcome Frame
        self.welcome_frame = tk.Frame(self.master, bg="white") 
        self.welcome_frame.grid(row=0, column=0, padx=500, pady=350)

        self.welcome_label = tk.Label(self.welcome_frame, text="Welcome to the Maze Game!", font=("Arial", 30, "bold"), bg="white")
        self.welcome_label.pack(pady=10)

        self.start_button = tk.Button(self.welcome_frame, text="Start Game", font=("Arial", 18, "bold"), bg="burlywood", command=self.show_main_ui)
        self.start_button.pack()

        # another frame for the main UI
        self.main_frame = tk.Frame(self.master)
        
        self.generate_button = tk.Button(self.main_frame, text="Generate Maze", font=("Arial", 12, "bold"), bg="white", command=self.generate_maze)
        self.generate_button.grid(row=0, column=0, padx=5, pady=5)

        self.solve_button = tk.Button(self.main_frame, text="Solve Maze", font=("Arial", 12, "bold"), bg="white", command=self.solve_maze)
        self.solve_button.grid(row=0, column=1, padx=5, pady=5)

        self.canvas = tk.Canvas(self.main_frame, width=1530, height=1500, bg="black")
        self.canvas.grid(row=1, column=0, columnspan=2)

        # Maze setup
        self.rows = 28
        self.cols = 51
        self.maze = []

    def show_main_ui(self):
        self.welcome_frame.grid_forget()  # Hide welcome frame
        self.main_frame.grid(row=0, column=0)  # Show main UI
        self.generate_maze()  # Generate first maze

    def generate_maze(self):
        self.maze = create_maze(self.rows, self.cols)
        self.draw_maze()

    def draw_brick(self, x, y):
        brick_color = "#B22222"
        mortar_color = "black"
        self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=brick_color, outline=mortar_color) 
        brick_height = CELL_SIZE // 3
        brick_width = CELL_SIZE // 2
        for i in range(1, 3):
            self.canvas.create_line(x, y + i * brick_height, x + CELL_SIZE, y + i * brick_height, fill=mortar_color, width=2)
        for i in range(2):
            offset = (i % 2) * (brick_width // 2)
            for j in range(3):
                self.canvas.create_line(x + offset, y + j * brick_height, x + offset, y + (j + 1) * brick_height, fill=mortar_color, width=2)
                offset += brick_width

    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                cell = self.maze[row][col]
                if cell == '#':
                    self.draw_brick(x1, y1)
                elif cell == 'S':
                    self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill='burlywood', outline='burlywood')
                elif cell == 'E':
                    self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill='burlywood', outline='burlywood')
                elif cell == '.':
                    self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill='white', outline='burlywood')
                else:
                    self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill='black', outline='black')

    def solve_maze(self):
        temp_maze = [row[:] for row in self.maze]
        if bfs(temp_maze, show_path=True):
            self.maze = temp_maze
            self.draw_maze()
        else:
            print("No path found")

if __name__ == "__main__":
    root = tk.Tk() # Create the main window
    app = MazeGUI(root) # Create an instance of the MazeGUI class
    root.mainloop() # Start the GUI event loop