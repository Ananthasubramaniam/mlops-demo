import pickle
from rl.agent import Q, PRIOR, won, empty, agent_move

from agent import won, empty, agent_move, Q
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "q_table.pkl"

with open(MODEL_PATH, "rb") as f:
    loaded_q = pickle.load(f)

Q.update(loaded_q)


def print_board(board):

    symbols = [
        v if v else str(i + 1)
        for i, v in enumerate(board)
    ]

    print(f"\n {symbols[0]} | {symbols[1]} | {symbols[2]}")
    print("-----------")
    print(f" {symbols[3]} | {symbols[4]} | {symbols[5]}")
    print("-----------")
    print(f" {symbols[6]} | {symbols[7]} | {symbols[8]}\n")


def play():

    board = [''] * 9

    while True:

        print_board(board)

        move = int(input("Your move (1-9): ")) - 1

        if board[move] != '':
            print("Invalid move")
            continue

        board[move] = 'X'

        if won(board, 'X'):
            print_board(board)
            print("You win")
            break

        if not empty(board):
            print("Draw")
            break

        ai_move = agent_move(board, epsilon=0)

        board[ai_move] = 'O'

        print(f"Agent played {ai_move + 1}")

        if won(board, 'O'):
            print_board(board)
            print("Agent wins")
            break

        if not empty(board):
            print("Draw")
            break


if __name__ == "__main__":
    play()