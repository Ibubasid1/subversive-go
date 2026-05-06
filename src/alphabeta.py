import copy

class AlphaBetaAgent:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, board):
        board.scoring()
        return board.black_score - board.white_score

    def search(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.game_over:
            return self.evaluate(board), None

        if maximizing:
            color = 1
        else:
            color = 2

        moves = board.legal_moves(color)
        if not moves:
            return self.evaluate(board), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                sim = copy.deepcopy(board)
                if move is None:
                    sim.skip()
                else:
                    sim.place(move[0], move[1])
                eval_score, _ = self.search(sim, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha: break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                sim = copy.deepcopy(board)
                if move is None:
                    sim.skip()
                else:
                    sim.place(move[0], move[1])
                eval_score, _ = self.search(sim, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha: break
            return min_eval, best_move