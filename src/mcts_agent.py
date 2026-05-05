from board import Board
import math
import random


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
    
    def get_best_child(self):
        max_ucb1_value = -math.inf
        chosen_child = None
        for child in self.children:
            child_ucb1_value = child.calculate_ucb_value()
            if child_ucb1_value > max_ucb1_value:
                max_ucb1_value = child_ucb1_value
                chosen_child = child
        return chosen_child
    
    
    def most_love_child(self):
        most_visited = random.choice(self.children)
        for child in self.children:
            if child.visits > most_visited.visits:
                most_visited = child
        return most_visited
    
    
