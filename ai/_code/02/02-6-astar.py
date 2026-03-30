"""
A* Search Algorithm Implementation
Uses heuristic to guide search toward goal efficiently
"""

import heapq


def heuristic(a, b):
    """Manhattan distance heuristic for grid"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_search(maze, start, goal):
    """
    Find shortest path using A* algorithm
    f(n) = g(n) + h(n) where g=cost from start, h=heuristic to goal
    """
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1], g_score[goal]
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            neighbor = (nr, nc)
            
            if (0 <= nr < rows and 0 <= nc < cols and 
                maze[nr][nc] == 0):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
    
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
    
    print("=== A* Search Algorithm ===")
    print(f"Start: {start}, Goal: {goal}")
    print("Using Manhattan distance heuristic\n")
    print("Maze (### = wall, . = path):")
    print_maze(maze)
    
    path, cost = astar_search(maze, start, goal)
    
    if path:
        print("Optimal path found:")
        print_maze(maze, path)
        print(f"Path: {path}")
        print(f"Total cost: {cost}")
    else:
        print("No path found")
