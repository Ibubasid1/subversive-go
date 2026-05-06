class Board:

    SIZE = 9

    def __init__(self):
        self.board = [[0]*Board.SIZE for _ in range(Board.SIZE)]
        self.moves = 0
        self.last_was_pass = False
        self.current_player = 1
        self.game_over = False
        self.black_score = 0
        self.white_score = 6.5 #starts with komi bonus
        self.result = 0


    #retrieves all adjacent pieces to the provided piece
    def get_adj(self, row, col):
        adjacent = set()
        if row < 8:
            adjacent.add((row + 1, col))
        if row > 0:
            adjacent.add((row - 1, col))
        if col < 8:
            adjacent.add((row, col + 1))
        if col > 0:
            adjacent.add((row, col - 1))
        return adjacent
    
    def skip(self):
        if self.last_was_pass: #checks if opponent has already passed
            self.game_over = True #if opponent has, then the game should end
        else: #if the opponent hasn't, then the game continues 
            self.moves += 1
            self.last_was_pass = True
        self.current_player = 2 if self.current_player == 1 else 1
        if self.game_over:
            self._announce_winner()
    
    
    @property
    def is_terminal(self):
        return self.game_over
    

    def is_legal(self, row, col, color):
        result = True
        if self.board[row][col] != 0:
            return False
        self.board[row][col] = color
        adjacents = self.get_adj(row, col)

        for element in adjacents:
            if self.count_liberties(element[0], element[1]) == 0 and self.board[element[0]][element[1]] != color:
                result = True
        if self.count_liberties(row, col) == 0:
            result = False

        self.board[row][col] = 0
        return result
    

    def legal_moves(self, color) -> set:
        #none represents 'pass' 
        all_legal_moves = set()
        all_legal_moves.add(None)
        for r in range(9):
            for c in range(9):
                if self.is_legal(r, c, color):
                    all_legal_moves.add((r, c))
        return all_legal_moves


    def place(self, row, col): #uses a simply row and column to make the move
        #make a check to see whether the move is available
        if not self.is_legal(row, col, self.current_player):
            # print("Invalid move")
            print(f"Invalid move at ({row}, {col}) for player {self.current_player}")
            return
        else:
            self.board[row][col] = self.current_player

        temp = self.get_adj(row, col)

        for element in temp:
            if self.count_liberties(element[0], element[1]) == 0 and self.board[element[0]][element[1]] != self.current_player:
                removable = self._traversal(element[0], element[1], self.board[element[0]][element[1]])
                for item in removable:
                    self.board[item[0]][item[1]] = 0

        self.last_was_pass = False

        self.moves += 1

        self.current_player = 2 if self.current_player == 1 else 1

        if self.moves >= 400: self.game_over = True

        if self.game_over:
            self._announce_winner()


    def __str__(self):
        rows = []
        for row in self.board:
            rows.append("|".join(str(cell) for cell in row))
        return "\n".join(rows)

    def _traversal_helper(self, row, col, color, visited) -> set:
        visited.add((row, col))
        if (row + 1) < self.SIZE and self.board[row + 1][col] == color and (row + 1, col) not in visited:
            self._traversal_helper(row + 1, col, color, visited)
        if (row - 1) >= 0 and self.board[row - 1][col] == color and (row - 1, col) not in visited:
            self._traversal_helper(row - 1, col, color, visited)
        if (col + 1) < self.SIZE and self.board[row][col + 1] == color and (row, col + 1) not in visited:
            self._traversal_helper(row, col + 1, color, visited)
        if (col - 1) >= 0 and self.board[row][col - 1] == color and (row, col - 1) not in visited:
            self._traversal_helper(row, col - 1, color, visited)
        return visited

    #main traversal function, used so that the 'visited' set is not reset on every instance of recursion
    def _traversal(self, row, col, color) -> set:
        #checks for bounds and ensures color is the same as the piece currently in that position
        if(row >= 0 and row < 9 and col >= 0 and col < 9 and self.board[row][col] == color):
            visited = set()
            return self._traversal_helper(row, col, color, visited)
        return set()
    
    def count_liberties(self, row, col) -> int:
        visited = set()
        connected = self._traversal(row, col, self.board[row][col])
        for element in connected:
            r = element[0]
            c = element[1]
            #no need for a 'not in visited' check since if it was already in visited it would simply not be added again. sets hold unique values
            if r < 8 and self.board[r + 1][c] == 0:
                visited.add((r + 1, c))
            if r > 0 and self.board[r - 1][c] == 0:
                visited.add((r - 1, c))
            if c < 8 and self.board[r][c + 1] == 0:
                visited.add((r, c + 1))
            if c > 0 and self.board[r][c - 1] == 0:
                visited.add((r, c - 1))   
        return len(visited)
    
    def scoring(self):
        self.black_score = 0
        self.white_score = 6.5
        total_visited = set()
        all_positions = {(r, c) for r in range(9) for c in range(9)}
        black_list = set()
        white_list = set()

        for element in all_positions:
            if self.board[element[0]][element[1]] == 1:
                black_list.add(element)
                self.black_score += 1
            elif self.board[element[0]][element[1]] == 2:
                white_list.add(element)
                self.white_score += 1
        
        all_positions -= black_list
        all_positions -= white_list
        total_visited.update(black_list)
        total_visited.update(white_list)

        for element in all_positions:
            if element not in total_visited:
                adjacents = set()
                open_space = self._traversal(element[0], element[1], self.board[element[0]][element[1]])
                total_visited.update(open_space)
                for item in open_space:
                    temp = self.get_adj(item[0], item[1])
                    for thing in temp:
                        if self.board[thing[0]][thing[1]] != 0:
                            adjacents.add(thing)
                if not adjacents:
                    continue
                chosen = next(iter(adjacents))
                piece_type = self.board[chosen[0]][chosen[1]]
                all_same = True
                for item in adjacents:
                    if self.board[item[0]][item[1]] != piece_type:
                        all_same = False
                if all_same:
                    if piece_type == 1:
                        self.black_score += len(open_space)
                    else:
                        self.white_score += len(open_space)

    def _announce_winner(self):
        self.scoring()
        # print("Player 1 has " + str(self.black_score) + "!")
        # print("Player 2 has " + str(self.white_score) + "!")
        if(self.white_score > self.black_score):
            # print("Player 2 wins!")
            self.result = 2
        else:
            # print("Player 1 wins!")
            self.result = 1
            
            
    def get_value(self, piece):
        if self.is_terminal:
            if piece == 1:
                return self.black_score
            return self.white_score;  



def main():
    b = Board()
    b.place(1, 1) #1
    b.place(1, 2) #2
    b.place(2, 1) #1
    b.place(0, 1) #2
    b.place(0, 2) #1
    b.place(0, 0) #2
    b.place(3, 5) #1 
    b.place(1, 0) #2
    print(b)
    print()
    b.place(2, 0) #1
    b.place(7, 7) #2
    b.place(0, 0) #1
    print(b.is_legal(0, 1, 2))
    print(b.is_legal(1, 0, 2))
    print(b.is_legal(0, 1, 1))
    print(b.is_legal(1, 0, 1))
    print(b)





    #if even number of moves, then black turn
    #if odd number of moves, then white turn
    #two possible moves, place or pass (maybe resign later)
    #let's call move 1 place and move 2 pass. If there are two consecutive move 2s, the game ends. 
    #however, the ai will likely not willingly pass. The random move will definitely not since that won't even be an option.
    #so, it's more likely that the game will end by the move limit we set, which will be 400

    #have created a new branch for this code, which will specifically be restricted to this file

if __name__ == "__main__":
    main()