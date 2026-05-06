import random

# Precompute neighbors for an 81-square 1D board to avoid boundary math during simulations
NEIGHBORS = [[] for _ in range(81)]
for i in range(81):
    r, c = divmod(i, 9)
    if r > 0: NEIGHBORS[i].append(i - 9)
    if r < 8: NEIGHBORS[i].append(i + 9)
    if c > 0: NEIGHBORS[i].append(i - 1)
    if c < 8: NEIGHBORS[i].append(i + 1)

class Board:
    SIZE = 9
    TOTAL_SQUARES = 81

    def __init__(self):
        self.board = [0] * self.TOTAL_SQUARES
        self.empty_points = set(range(self.TOTAL_SQUARES))
        self.moves = 0
        self.last_was_pass = False
        self.current_player = 1
        self.game_over = False
        self.black_score = 0
        self.white_score = 6.5 # Komi

    def clone(self):
        # Extremely fast cloning bypassing __init__
        new = Board.__new__(Board)          
        new.board = self.board[:] 
        new.empty_points = self.empty_points.copy()
        new.moves = self.moves
        new.last_was_pass = self.last_was_pass
        new.current_player = self.current_player
        new.game_over = self.game_over
        new.black_score = self.black_score
        new.white_score = self.white_score
        return new

    def skip(self):
        if self.last_was_pass: 
            self.game_over = True 
        else: 
            self.moves += 1
            self.last_was_pass = True
        self.current_player = 3 - self.current_player # toggles between 1 and 2

    @property
    def is_terminal(self):
        return self.game_over

    def get_group_and_liberties(self, pos, color):
        """Iterative DFS to find group members and liberty count. Much faster than recursion."""
        stack = [pos]
        group = []
        visited = bytearray(self.TOTAL_SQUARES)
        visited[pos] = 1
        liberties = 0

        while stack:
            curr = stack.pop()
            group.append(curr)
            for n in NEIGHBORS[curr]:
                if not visited[n]:
                    visited[n] = 1
                    if self.board[n] == 0:
                        liberties += 1
                    elif self.board[n] == color:
                        stack.append(n)
        return group, liberties

    def is_legal(self, pos, color):
        if self.board[pos] != 0:
            return False

        # Fast check: if an adjacent spot is empty, it definitely has liberties
        for n in NEIGHBORS[pos]:
            if self.board[n] == 0:
                return True

        # Simulate placement
        self.board[pos] = color
        opp = 3 - color
        captures = False

        for n in NEIGHBORS[pos]:
            if self.board[n] == opp:
                _, libs = self.get_group_and_liberties(n, opp)
                if libs == 0:
                    captures = True
                    break
        
        has_liberties = False
        if not captures:
            _, libs = self.get_group_and_liberties(pos, color)
            has_liberties = libs > 0

        self.board[pos] = 0 # revert
        return has_liberties or captures

    def legal_moves(self, color):
        all_legal_moves = [None] # None represents pass
        for pos in self.empty_points:
            if self.is_legal(pos, color):
                all_legal_moves.append(pos) #type: ignore
        return all_legal_moves

    def place(self, pos):
        if pos is None:
            self.skip()
            return
            
        color = self.current_player
        opp = 3 - color

        if not self.is_legal(pos, color):
            r, c = divmod(pos, 9)
            print(f"Invalid move at ({r}, {c}) for player {color}")
            return

        self.board[pos] = color
        self.empty_points.discard(pos)

        # Handle Captures
        for n in NEIGHBORS[pos]:
            if self.board[n] == opp:
                group, libs = self.get_group_and_liberties(n, opp)
                if libs == 0:
                    for p in group:
                        self.board[p] = 0
                        self.empty_points.add(p)

        self.last_was_pass = False
        self.moves += 1
        self.current_player = opp
        if self.moves >= 400: 
            self.game_over = True

    def random_move(self):
        # Instead of random guessing, shuffle the known empty points and take the first legal one
        empty_list = list(self.empty_points)
        random.shuffle(empty_list)
        for pos in empty_list:
            if self.is_legal(pos, self.current_player):
                return pos
        return None # Pass if no legal moves

    def fast_score(self):
        """Simplified fast scoring for MCTS rollouts to prevent bottlenecks at terminal states."""
        self.black_score = sum(1 for p in self.board if p == 1)
        self.white_score = 6.5 + sum(1 for p in self.board if p == 2)
        
        # Attribute empty spaces
        visited = bytearray(self.TOTAL_SQUARES)
        for i in range(self.TOTAL_SQUARES):
            if self.board[i] == 0 and not visited[i]:
                stack = [i]
                visited[i] = 1
                group = []
                touches_black = False
                touches_white = False
                
                while stack:
                    curr = stack.pop()
                    group.append(curr)
                    for n in NEIGHBORS[curr]:
                        if self.board[n] == 1: touches_black = True
                        elif self.board[n] == 2: touches_white = True
                        elif self.board[n] == 0 and not visited[n]:
                            visited[n] = 1
                            stack.append(n)
                
                if touches_black and not touches_white:
                    self.black_score += len(group)
                elif touches_white and not touches_black:
                    self.white_score += len(group)

    def get_value(self, player_perspective):
        if self.is_terminal:
            self.fast_score()
            if player_perspective == 1:
                return 1 if self.black_score > self.white_score else -1
            else:
                return 1 if self.white_score > self.black_score else -1

    def __str__(self):
        rows = []
        for r in range(self.SIZE):
            row = [str(self.board[r * 9 + c]) for c in range(self.SIZE)]
            rows.append("|".join(row))
        return "\n".join(rows)