import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1
        
    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1
        return self.board.flatten()
    
    def get_empty_cells(self):
        return list(zip(*np.where(self.board == 0)))
    
    def check_winner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.player):
                return True
            if np.all(self.board[:, i] == self.player):
                return True
        if np.all(np.diag(self.board) == self.player):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == self.player):
            return True
        return False
    
    def step(self, action):
        row, col = action // 3, action % 3
        
        if self.board[row, col] != 0:
            return self.board.flatten(), -1.0, True
            
        self.board[row, col] = self.player
        
        if self.check_winner():
            return self.board.flatten(), 1.0, True
            
        if len(self.get_empty_cells()) == 0:
            return self.board.flatten(), 0.0, True
            
        self.player = -self.player
        return self.board.flatten(), 0.0, False

class TictactoeRL:
    def __init__(self):
        self.q_table = {}
        
    def get_state_key(self, board):
        return tuple(board)
    
    def get_q(self, state, action):
        key = (self.get_state_key(state), action)
        return self.q_table.get(key, 0.0)
    
    def update(self, state, action, reward):
        key = (self.get_state_key(state), action)
        self.q_table[key] = reward

game = TicTacToe()
agent = TictactoeRL()

print("=" * 60)
print("Tic-Tac-Toe RL Demo")
print("=" * 60)

state = game.reset()
print("Initial board:")
print(np.array([' ' if x == 0 else ('X' if x == 1 else 'O') for x in state]).reshape(3,3))

actions = [4, 0, 1, 2]
for a in actions:
    state, reward, done = game.step(a)
    agent.update(state, a, reward)
    board_display = np.array([' ' if x == 0 else ('X' if x == 1 else 'O') for x in state]).reshape(3,3)
    print(f"\nAfter move {a}:")
    print(board_display)
    if done:
        print(f"Game over! Reward: {reward}")
        break

print("\n✓ Tic-Tac-Toe RL demonstrates:")
print("  - Discrete action space (9 positions)")
print("  - Perfect information game")
print("  - Can be solved with Q-learning / search")
print("  - Good baseline for game-playing RL")
