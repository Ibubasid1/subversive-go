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