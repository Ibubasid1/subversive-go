from board import Board
import math


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
    
    
