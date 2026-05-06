from board import Board
import math
import random
import time
import copy


class _Node:
    def __init__(self, board_layout: "Board", parent=None, move=None):
        self.current_state = board_layout
        self.visits = 0
        self.value = 0
        self.parent = parent
        self.move = move
        self.children = []
        
    
    def add_child(self, child: "_Node") -> None:
        self.children.append(child)
    
    
    @property
    def is_leaf(self) -> bool:
        return not self.children
    
    
    def calculate_ucb1_value(self, constant = 2) -> float:
        if self.visits == 0 or not self.parent:
            return math.inf
        average_value = self.value/self.visits
        return average_value + constant * math.sqrt(math.log(self.parent.visits)/self.visits)
    
    
    def get_best_child(self) -> "_Node":
        max_ucb1_value = -math.inf
        for child in self.children:
            child_ucb1_value = child.calculate_ucb1_value()
            if child_ucb1_value > max_ucb1_value:
                max_ucb1_value = child_ucb1_value
                best_child = child
        return best_child
    
    
    def most_loved_child(self):
        most_visited = random.choice(self.children)
        for child in self.children:
            if child.visits > most_visited.visits:
                most_visited = child
        return most_visited
    
    
    def expand_node(self) -> bool:
        available_legal_moves = self.current_state.legal_moves(self.current_state.current_player);
        if not available_legal_moves:
            return False
        for move in available_legal_moves:
            new_state = self.current_state.simulate_move(move)
            new_child = _Node(new_state, self, move)
            self.children.append(new_child)
        return True



class MCTS:
    def node_selection(self, node) -> _Node:
        while not node.is_leaf:
            node = node.get_best_child()
        return node
    
    
    def simulation(self, node: "_Node"):
        state = node.current_state
        current_player = 2 if state.current_player == 1 else 1
        while True:
            if state.is_terminal:
                return state.get_value(current_player)
            state = state.simulate_move(state.random_move())
    
        
    def backpropagate(self, node: "_Node", value):
        current_node = node
        while True:
            current_node.visits += 1
            current_node.value += value
            if not current_node.parent:
                break
            value = -value
            current_node = current_node.parent
            
    def get_best_move(self, current_state: "Board") -> tuple: #type: ignore
        root_node = _Node(current_state)
        current_time = time.time()
        while time.time() - current_time < 1:
            node = self.node_selection(root_node)
            if not node.current_state.is_terminal:
                if node.visits:
                    node.expand_node()
                    node = random.choice(node.children)
            value = self.simulation(node)
            self.backpropagate(node, value)
        most_visited_child = root_node.most_loved_child()
        print(root_node.visits)
        return most_visited_child.move
        
def main():
    board = Board()
    agent = MCTS()
    agent2 = MCTS()
    # print(len(board.legal_moves(board.current_player)))
    while not board.game_over:
        move = agent.get_best_move(board)
        if move == None:
            board.skip()
        else:
            board.place(move[0], move[1])
        print(board)
        if board.game_over: break
        move = agent2.get_best_move(board)
        if move == None:
            board.skip()
        else:
            board.place(move[0], move[1])
        print(board)
        if board.game_over: break
    board._announce_winner()
        
        
if __name__ == "__main__":
    main()
    
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
#filler
