import numpy as np

class GridWorld:
    def __init__(self, width=4, height=4, start=(0, 0), goal=(3, 3)):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.state = start
        
    def reset(self):
        self.state = self.start
        return self.state
    
    def step(self, action):
        x, y = self.state
        if action == 0:
            y = max(0, y - 1)
        elif action == 1:
            y = min(self.height - 1, y + 1)
        elif action == 2:
            x = max(0, x - 1)
        elif action == 3:
            x = min(self.width - 1, x + 1)
            
        self.state = (x, y)
        
        if self.state == self.goal:
            return self.state, 1.0, True
        return self.state, -0.1, False
    
    def render(self):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        gx, gy = self.goal
        grid[gy][gx] = "G"
        sx, sy = self.state
        grid[sy][sx] = "A"
        return "\n".join([" ".join(row) for row in grid])

env = GridWorld()
state = env.reset()

print("=" * 60)
print("Grid World Environment Demo")
print("=" * 60)
print(f"Grid size: {env.width}x{env.height}")
print(f"Start: {env.start}, Goal: {env.goal}")
print("\nInitial state:")
print(env.render())

actions = [1, 1, 3, 3, 1, 1, 3]
for a in actions:
    state, reward, done = env.step(a)
    print(f"\nAction {a}, Reward: {reward:.1f}")
    print(env.render())
    if done:
        print("Goal reached!")
        break
