"""
Breadth-First Search (BFS) Implementation
Uses queue for level-order exploration, guarantees shortest path
"""

from collections import deque


def bfs_shortest_path(maze, start, goal):
    """
    Find shortest path from start to goal using BFS
    Returns path and distance
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path, len(path) - 1
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0 and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    
    return None, float('inf')


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
    
    print("=== BFS Shortest Path ===")
    print(f"Start: {start}, Goal: {goal}\n")
    print("Maze (### = wall, . = path):")
    print_maze(maze)
    
    path, distance = bfs_shortest_path(maze, start, goal)
    
    if path:
        print("Shortest path found:")
        print_maze(maze, path)
        print(f"Path: {path}")
        print(f"Shortest distance: {distance} steps")
    else:
        print("No path found")
