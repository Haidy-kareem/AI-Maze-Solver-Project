## MazeSolver — AI Maze Generator & Pathfinding Visualizer

A Python application that generates random mazes and solves them using 
Breadth-First Search (BFS), with an interactive visual interface built in Tkinter.

### Features
- Random maze generation with a guaranteed path between start (S) and end (E)
- BFS algorithm to find the shortest path between start and end points
- Interactive GUI: generate a new maze or solve the current one with a click
- Visual rendering of walls, path, start, and end points on a canvas

### How it works
1. A maze is generated as a grid, with a random walk carving a guaranteed 
   path from start to end, then walls are added randomly around it.
2. BFS explores the maze level by level from the start point until it 
   reaches the end, tracking the shortest path found.
3. The GUI displays the maze and highlights the solved path.

### Tech stack
Python, Tkinter, collections.deque (BFS implementation)
