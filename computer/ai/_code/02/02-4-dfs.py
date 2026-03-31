"""
Depth-First Search (DFS) Implementation
Uses a stack-based approach to explore the maze
"""

class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def is_empty(self):
        return len(self.items) == 0


def dfs_maze(maze, start, goal):
    """
    Find path from start to goal using DFS
    Returns path as list of coordinates
    """
    rows, cols = len(maze), len(maze[0])
    stack = Stack()
    stack.push([start])
    visited = set()
    visited.add(start)
    
    while not stack.is_empty():
        path = stack.pop()
        current = path[-1]
        
        if current == goal:
            return path
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and (nr, nc) not in visited):
                visited.add((nr, nc))
                new_path = path + [(nr, nc)]
                stack.push(new_path)
    
    return None


def print_maze(maze, path=None):
    """Display maze with path marked"""
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if path and (r, c) in path:
                line += " * "
            elif cell == 1:
                line += " ###"
            else:
                line += " . "
        print(line)
    print()


if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    goal = (4, 4)
    
    print("=== DFS Maze Solver ===")
    print(f"Start: {start}, Goal: {goal}\n")
    print("Maze (### = wall, . = path):")
    print_maze(maze)
    
    path = dfs_maze(maze, start, goal)
    
    if path:
        print("Solution path found:")
        print_maze(maze, path)
        print(f"Path: {path}")
        print(f"Steps: {len(path)}")
    else:
        print("No path found")
