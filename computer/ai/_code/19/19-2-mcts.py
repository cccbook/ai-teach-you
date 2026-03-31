import numpy as np

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = {}
        self.visits = 0
        self.value = 0.0
        
    def is_expanded(self):
        return len(self.children) > 0
    
    def best_child(self, c_param=1.4):
        best_score = float('-inf')
        best_child = None
        for action, child in self.children.items():
            exploitation = child.value / (child.visits + 1)
            exploration = c_param * np.sqrt(np.log(self.visits + 1) / (child.visits + 1))
            score = exploitation + exploration
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

class MCTS:
    def __init__(self, num_actions):
        self.num_actions = num_actions
        self.root = None
        
    def select(self, node):
        while node.is_expanded():
            node = node.best_child()
        return node
    
    def expand(self, node, action, next_state):
        child = MCTSNode(next_state, node, action)
        node.children[action] = child
        return child
    
    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

def simulate(env_state):
    return np.random.randn()

mcts = MCTS(num_actions=4)
mcts.root = MCTSNode(state=np.array([0, 0]))

for i in range(3):
    node = mcts.select(mcts.root)
    action = i
    next_state = np.array([i+1, i+1])
    child = mcts.expand(node, action, next_state)
    reward = simulate(next_state)
    mcts.backpropagate(child, reward)

best = mcts.root.best_child()

print("=" * 60)
print("MCTS (Monte Carlo Tree Search) Demo")
print("=" * 60)
print(f"Number of actions: 4")
print(f"Root visits: {mcts.root.visits}")
print(f"Root value: {mcts.root.value:.4f}")

print("\nChildren:")
for action, child in mcts.root.children.items():
    print(f"  Action {action}: visits={child.visits}, value={child.value:.4f}")

print("\n✓ MCTS combines tree search with Monte Carlo simulation:")
print("  - Selection: traverse tree using UCB")
print("  - Expansion: add new child node")
print("  - Simulation: rollout random policy")
print("  - Backpropagation: update statistics")
