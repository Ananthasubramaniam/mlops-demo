import random

# The agent's memory — maps (board_state, cell) -> learned value
Q = {}

WINS = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

# Strategic starting values — center > corners > edges
PRIOR = [0.10, 0.06, 0.10,
         0.06, 0.20, 0.06,
         0.10, 0.06, 0.10]


def get_q(board, cell):
    key = (tuple(board), cell)
    print(key)
    return Q.get(key, PRIOR[cell])


def empty(board):
    return [i for i, v in enumerate(board) if v == '']


def won(board, player):
    return any(all(board[i] == player for i in line) for line in WINS)


def agent_move(board, epsilon):
    moves = empty(board)
    if random.random() < epsilon:
        return random.choice(moves)                         # explore
    return max(moves, key=lambda m: get_q(board, m))       # exploit


def print_board(board):
    symbols = [v if v else str(i+1) for i, v in enumerate(board)]
    print(f"\n {symbols[0]} | {symbols[1]} | {symbols[2]}")
    print(f" --|---|--")
    print(f" {symbols[3]} | {symbols[4]} | {symbols[5]}")
    print(f" --|---|--")
    print(f" {symbols[6]} | {symbols[7]} | {symbols[8]}\n")


# ── Training ────────────────────────────────────────────────

def train(episodes):
    epsilon = 1.0

    for ep in range(episodes):
        board = [''] * 9
        player = 'X'
        history = []

        # play one full game
        while True:
            move = agent_move(board, epsilon)
            history.append((tuple(board), move, player))
            board[move] = player

            if won(board, player) or not empty(board):
                break
            player = 'O' if player == 'X' else 'X'

        # assign reward
        if won(board, 'X'):   reward =  1
        elif won(board, 'O'): reward = -1
        else:                 reward =  0

        # update Q backwards through the game
        for (state, move, who) in reversed(history):
            r = reward if who == 'X' else -reward
            old = Q.get((state, move), PRIOR[move])
            Q[(state, move)] = old + 0.4 * (r - old)

        epsilon = max(0.05, epsilon * 0.995)

    print(f"Training done — {len(Q)} state-action pairs learned.")


# ── Play against the agent ───────────────────────────────────

def play():
    board = [''] * 9
    print_board(board)

    while True:
        # human turn
        move = int(input("Your move (1-9): ")) - 1
        board[move] = 'X'
        print_board(board)
        if won(board, 'X'): print("You win!"); return
        if not empty(board): print("Draw!"); return

        # show what the agent is thinking
        print("Agent Q-values:", {i+1: round(get_q(board, i), 3) for i in empty(board)})

        # agent turn
        move = agent_move(board, epsilon=0)
        board[move] = 'O'
        print(f"Agent plays {move+1}")
        print_board(board)
        if won(board, 'O'): print("Agent wins!"); return
        if not empty(board): print("Draw!"); return


# ── Main ─────────────────────────────────────────────────────

print("=== RL Tic-Tac-Toe ===\n")
print("1) Play BEFORE training  — agent uses only the prior")
print("2) Train the agent")
print("3) Play AFTER training   — agent uses learned Q-values")
print()

while True:
    choice = input("Choice (1/2/3): ")
    if choice == '1': play()
    elif choice == '2':
        n = int(input("Episodes: "))
        train(n)
    elif choice == '3': play()
