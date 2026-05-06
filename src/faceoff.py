from optimized_board import Board
from random_agent import RandomAgent
from alphabeta import AlphaBetaAgent
from mcts_agent import MCTS
import multiprocessing as mp
import time
import os
import random


def winner(board):
    board.fast_score()
    return 2 if board.white_score > board.black_score else 1


def _seed_worker():
    random.seed(os.getpid() ^ time.time_ns())


# ---------------------------------------------------------------
# Workers — each plays one game and returns 1 if `target` won.
# ---------------------------------------------------------------

def play_random_vs_random(target_color):
    _seed_worker()
    board = Board()
    a_black = RandomAgent(1)
    a_white = RandomAgent(2)
    while not board.game_over:
        if board.current_player == 1:
            a_black.make_move(board)
        else:
            a_white.make_move(board)
    return 1 if winner(board) == target_color else 0


def play_ab_vs_random(ab_color):
    _seed_worker()
    board = Board()
    ab = AlphaBetaAgent()
    rand = RandomAgent(3 - ab_color)
    maximizing = (ab_color == 1)
    while not board.game_over:
        if board.current_player == ab_color:
            _, move = ab.search(board, ab.depth, float('-inf'), float('inf'), maximizing)
            board.place(move)
        else:
            rand.make_move(board)
    return 1 if winner(board) == ab_color else 0


def play_mcts_vs_random(args):
    mcts_color, time_limit = args
    _seed_worker()
    board = Board()
    mcts = MCTS()
    rand = RandomAgent(3 - mcts_color)
    while not board.game_over:
        if board.current_player == mcts_color:
            move = mcts.get_best_move(board, time_limit=time_limit)
            board.place(move)
        else:
            rand.make_move(board)
    return 1 if winner(board) == mcts_color else 0


def play_mcts_vs_ab(args):
    mcts_color, time_limit = args
    _seed_worker()
    board = Board()
    mcts = MCTS()
    ab = AlphaBetaAgent()
    ab_color = 3 - mcts_color
    maximizing = (ab_color == 1)
    while not board.game_over:
        if board.current_player == mcts_color:
            move = mcts.get_best_move(board, time_limit=time_limit)
            board.place(move)
        else:
            _, move = ab.search(board, ab.depth, float('-inf'), float('inf'), maximizing)
            board.place(move)
    return 1 if winner(board) == mcts_color else 0


def main():
    GAMES_PER_SIDE = 25
    MCTS_TIME_LIMIT = 2.0
    num_workers = max(1, mp.cpu_count() - 1)
    print(f"Using {num_workers} worker processes\n")

    # Random vs Random
    print(f"=== Random vs Random ({2 * GAMES_PER_SIDE} games) ===")
    start = time.time()
    jobs = [1] * GAMES_PER_SIDE + [2] * GAMES_PER_SIDE
    with mp.Pool(num_workers) as pool:
        results = pool.map(play_random_vs_random, jobs)
    agent1win = sum(results)
    agent2win = len(results) - agent1win
    print(f"Time: {time.time() - start:.1f}s")
    print(f"One wins: {agent1win}")
    print(f"Two wins: {agent2win}\n")

    # AlphaBeta vs Random
    print(f"=== AlphaBeta vs Random ({2 * GAMES_PER_SIDE} games) ===")
    start = time.time()
    jobs = [1] * GAMES_PER_SIDE + [2] * GAMES_PER_SIDE
    with mp.Pool(num_workers) as pool:
        results = pool.map(play_ab_vs_random, jobs)
    abWins = sum(results)
    randWins = len(results) - abWins
    print(f"Time: {time.time() - start:.2f} sec")
    print(f"Random wins: {randWins}")
    print(f"Alpha Beta wins: {abWins}\n")

    # MCTS vs Random
    print(f"=== MCTS vs Random ({2 * GAMES_PER_SIDE} games) ===")
    start = time.time()
    jobs = [(1, MCTS_TIME_LIMIT)] * GAMES_PER_SIDE + [(2, MCTS_TIME_LIMIT)] * GAMES_PER_SIDE
    with mp.Pool(num_workers) as pool:
        results = []
        for i, r in enumerate(pool.imap_unordered(play_mcts_vs_random, jobs), 1):
            results.append(r)
            # print(f"  finished {i}/{len(jobs)}", flush=True)
    mctsWins = sum(results)
    randWinsM = len(results) - mctsWins
    print(f"Time: {(time.time() - start) / 60:.2f} min")
    print(f"Random wins: {randWinsM}")
    print(f"MCTS wins: {mctsWins}\n")

    # MCTS vs AlphaBeta
    print(f"=== MCTS vs AlphaBeta ({2 * GAMES_PER_SIDE} games) ===")
    start = time.time()
    jobs = [(1, MCTS_TIME_LIMIT)] * GAMES_PER_SIDE + [(2, MCTS_TIME_LIMIT)] * GAMES_PER_SIDE
    with mp.Pool(num_workers) as pool:
        results = []
        for i, r in enumerate(pool.imap_unordered(play_mcts_vs_ab, jobs), 1):
            results.append(r)
            # print(f"  finished {i}/{len(jobs)}", flush=True)
    mctsWinsAB = sum(results)
    abWinsM = len(results) - mctsWinsAB
    print(f"Time: {(time.time() - start) / 60:.2f} min")
    print(f"Alpha Beta wins: {abWinsM}")
    print(f"MCTS wins: {mctsWinsAB}")


if __name__ == "__main__":
    main()