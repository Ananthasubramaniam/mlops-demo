import random

Q = {}

WINS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

PRIOR = [
    0.10, 0.06, 0.10,
    0.06, 0.20, 0.06,
    0.10, 0.06, 0.10
]


def get_q(board, cell):
    key = (tuple(board), cell)
    return Q.get(key, PRIOR[cell])


def empty(board):
    return [i for i, v in enumerate(board) if v == '']


def won(board, player):
    return any(
        all(board[i] == player for i in line)
        for line in WINS
    )


def agent_move(board, epsilon=0.1):

    moves = empty(board)

    if random.random() < epsilon:
        return random.choice(moves)

    return max(
        moves,
        key=lambda m: get_q(board, m)
    )