import tkinter as tk

SIZE = 9
CELL = 60
MARGIN = CELL


class Board:

    def __init__(self):

        self.board = [[0] * SIZE for _ in range(SIZE)]

        self.moves = 0
        self.last_was_pass = False
        self.current_player = 1
        self.game_over = False

        self.black_score = 0
        self.white_score = 6.5

        self.root = tk.Tk()
        self.root.title("Go Game")

        canvas_size = 2 * MARGIN + (SIZE - 1) * CELL

        self.canvas = tk.Canvas(
            self.root,
            width=canvas_size,
            height=canvas_size,
            bg="beige"
        )

        self.canvas.pack()

        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):

        self.canvas.delete("all")

        for i in range(SIZE):

            x = MARGIN + i * CELL
            y = MARGIN + i * CELL

            self.canvas.create_line(
                MARGIN,
                y,
                MARGIN + (SIZE - 1) * CELL,
                y,
                width=2
            )

            self.canvas.create_line(
                x,
                MARGIN,
                x,
                MARGIN + (SIZE - 1) * CELL,
                width=2
            )

        for row in range(SIZE):
            for col in range(SIZE):

                piece = self.board[row][col]

                if piece == 0:
                    continue

                x = MARGIN + col * CELL
                y = MARGIN + row * CELL

                radius = CELL // 2 - 4

                color = "black" if piece == 1 else "white"

                self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=color
                )

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

        if self.last_was_pass:
            self.game_over = True

        else:
            self.moves += 1
            self.last_was_pass = True

        if self.game_over:
            self._announce_winner()

    def place(self, row, col):
        

        if self.board[row][col] != 0:
            print("Invalid move")
            return

        self.board[row][col] = self.current_player

        temp = self.get_adj(row, col)

        for element in temp:

            r, c = element

            if (
                self.board[r][c] != 0
                and self.board[r][c] != self.current_player
                and self.count_liberties(r, c) == 0
            ):

                removable = self._traversal(
                    r,
                    c,
                    self.board[r][c]
                )

                for item in removable:
                    self.board[item[0]][item[1]] = 0

        if self.count_liberties(row, col) == 0:

            self.board[row][col] = 0
            print("Invalid move")
            return

        self.last_was_pass = False

        self.moves += 1

        self.current_player = 2 if self.current_player == 1 else 1

        if self.moves >= 400:
            self.game_over = True

        if self.game_over:
            self._announce_winner()

    def __str__(self):

        rows = []

        for row in self.board:
            rows.append("|".join(str(cell) for cell in row))

        return "\n".join(rows)

    def _traversal_helper(self, row, col, color, visited):

        visited.add((row, col))

        if (
            row + 1 < SIZE
            and self.board[row + 1][col] == color
            and (row + 1, col) not in visited
        ):
            self._traversal_helper(
                row + 1,
                col,
                color,
                visited
            )

        if (
            row - 1 >= 0
            and self.board[row - 1][col] == color
            and (row - 1, col) not in visited
        ):
            self._traversal_helper(
                row - 1,
                col,
                color,
                visited
            )

        if (
            col + 1 < SIZE
            and self.board[row][col + 1] == color
            and (row, col + 1) not in visited
        ):
            self._traversal_helper(
                row,
                col + 1,
                color,
                visited
            )

        if (
            col - 1 >= 0
            and self.board[row][col - 1] == color
            and (row, col - 1) not in visited
        ):
            self._traversal_helper(
                row,
                col - 1,
                color,
                visited
            )

        return visited

    def _traversal(self, row, col, color):

        if (
            0 <= row < SIZE
            and 0 <= col < SIZE
            and self.board[row][col] == color
        ):

            visited = set()

            return self._traversal_helper(
                row,
                col,
                color,
                visited
            )

        return set()

    def count_liberties(self, row, col):

        visited = set()

        temp = self._traversal(
            row,
            col,
            self.board[row][col]
        )

        for element in temp:

            r, c = element

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

        all_positions = {
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
        }

        black_list = set()
        white_list = set()

        for element in all_positions:

            r, c = element

            if self.board[r][c] == 1:
                black_list.add(element)
                self.black_score += 1

            elif self.board[r][c] == 2:
                white_list.add(element)
                self.white_score += 1

        all_positions -= black_list
        all_positions -= white_list

        total_visited.update(black_list)
        total_visited.update(white_list)

        for element in all_positions:

            if element not in total_visited:

                adjacents = set()

                open_space = self._traversal(
                    element[0],
                    element[1],
                    self.board[element[0]][element[1]]
                )

                total_visited.update(open_space)

                for item in open_space:

                    temp = self.get_adj(
                        item[0],
                        item[1]
                    )

                    for thing in temp:

                        if self.board[thing[0]][thing[1]] != 0:
                            adjacents.add(thing)

                if not adjacents:
                    continue

                chosen = next(iter(adjacents))

                piece_type = self.board[
                    chosen[0]
                ][
                    chosen[1]
                ]

                all_same = True

                for item in adjacents:

                    if (
                        self.board[item[0]][item[1]]
                        != piece_type
                    ):
                        all_same = False

                if all_same:

                    if piece_type == 1:
                        self.black_score += len(open_space)

                    else:
                        self.white_score += len(open_space)

    def _announce_winner(self):

        self.scoring()

        print("Black:", self.black_score)
        print("White:", self.white_score)

        if self.white_score > self.black_score:
            print("White wins!")

        else:
            print("Black wins!")

    def on_click(self, event):

        col = round((event.x - MARGIN) / CELL)
        row = round((event.y - MARGIN) / CELL)

        if not (0 <= row < SIZE and 0 <= col < SIZE):
            return

        old_board = [r[:] for r in self.board]

        self.place(row, col)

        if old_board != self.board:
            self.draw_board()

    def run(self):

        self.root.mainloop()


go_board = Board()
go_board.run()