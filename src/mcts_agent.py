from board import Board
import math
import random
import time

class _Node:
    def __init__(self, board_layout: "Board", parent=None, move=None):
        self.current_state = board_layout
        self.visits = 0
        self.value = 0
        self.parent = parent
        self.move = move
        self.children = []
        self.untried_moves = board_layout.legal_moves(board_layout.current_player)
    
    @property
    def is_leaf(self) -> bool:
        return not self.children
        
    @property
    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0
    
    def calculate_ucb1_value(self, constant=2) -> float:
        if self.visits == 0 or not self.parent:
            return math.inf
        average_value = self.value / self.visits
        return average_value + constant * math.sqrt(math.log(self.parent.visits) / self.visits)
    
    def get_best_child(self) -> "_Node":
        return max(self.children, key=lambda c: c.calculate_ucb1_value())
    
    def most_loved_child(self):
        return max(self.children, key=lambda c: c.visits)
    
    def expand_node(self) -> "_Node":
        move = self.untried_moves.pop()
        new_state = self.current_state.clone()
        new_state.place(move)
        new_child = _Node(new_state, self, move)
        self.children.append(new_child)
        return new_child

class MCTS:
    def node_selection(self, node: _Node) -> _Node:
        while not node.current_state.is_terminal:
            if not node.is_fully_expanded:
                return node.expand_node()
            else:
                node = node.get_best_child()
        return node
    
    def simulation(self, node: "_Node"):
        state = node.current_state.clone()
        current_player_at_root = 3 - state.current_player # The player who just moved
        
        while not state.is_terminal:
            move = state.random_move()
            state.place(move)
            
        return state.get_value(current_player_at_root)
    
    def backpropagate(self, node: "_Node", value):
        current_node = node
        while current_node is not None:
            current_node.visits += 1
            current_node.value += value
            value = -value # Negate for the parent's perspective
            current_node = current_node.parent
            
    def get_best_move(self, current_state: "Board", time_limit=1.0): 
        root_node = _Node(current_state)
        end_time = time.time() + time_limit
        
        sims = 0
        while time.time() < end_time:
            leaf = self.node_selection(root_node)
            value = self.simulation(leaf)
            self.backpropagate(leaf, value)
            sims += 1
            
        print(f"Simulations completed: {sims}")
        if not root_node.children:
            return None
            
        return root_node.most_loved_child().move

def main():
    board = Board()
    agent = MCTS()
    agent2 = MCTS()
    
    while not board.game_over:
        print("\nPlayer 1 Thinking...")
        move = agent.get_best_move(board, time_limit=2.0)
        board.place(move)
        print(board)
        if board.game_over: break
        
        print("\nPlayer 2 Thinking...")
        move = agent2.get_best_move(board, time_limit=2.0)
        board.place(move)
        print(board)
        if board.game_over: break
        
    board.fast_score()
    print("\nGame Over!")
    print(f"Black Score: {board.black_score}")
    print(f"White Score: {board.white_score}")

if __name__ == "__main__":
    main()