import pickle
import mlflow
import matplotlib.pyplot as plt
from pathlib import Path
from agent import Q, PRIOR, won, empty, agent_move

from agent import Q, PRIOR, won, empty, agent_move

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("TicTacToe-RL")


def train(episodes=10000):

    epsilon = 1.0

    x_wins = 0
    o_wins = 0
    draws = 0

    rewards = []

    mlflow.start_run()

    mlflow.log_param("episodes", episodes)

    for ep in range(episodes):

        board = [''] * 9
        player = 'X'

        history = []

        while True:

            move = agent_move(board, epsilon)

            history.append((tuple(board), move, player))

            board[move] = player

            if won(board, player) or not empty(board):
                break

            player = 'O' if player == 'X' else 'X'

        if won(board, 'X'):
            reward = 1
            x_wins += 1

        elif won(board, 'O'):
            reward = -1
            o_wins += 1

        else:
            reward = 0
            draws += 1

        rewards.append(reward)

        for (state, move, who) in reversed(history):

            r = reward if who == 'X' else -reward

            old = Q.get((state, move), PRIOR[move])

            Q[(state, move)] = old + 0.4 * (r - old)

        epsilon = max(0.05, epsilon * 0.995)

    mlflow.log_metric("x_win_rate", x_wins / episodes)
    mlflow.log_metric("o_win_rate", o_wins / episodes)
    mlflow.log_metric("draw_rate", draws / episodes)

    BASE_DIR = Path(__file__).resolve().parent.parent

    MODELS_DIR = BASE_DIR / "models"
    METRICS_DIR = BASE_DIR / "metrics"

    MODELS_DIR.mkdir(exist_ok=True)
    METRICS_DIR.mkdir(exist_ok=True)

    MODEL_PATH = MODELS_DIR / "q_table.pkl"
    REWARD_PLOT_PATH = METRICS_DIR / "rewards.png"

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(Q, f)

    plt.plot(rewards)
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.title("Training Rewards")

    plt.savefig(REWARD_PLOT_PATH)

    mlflow.log_artifact(str(REWARD_PLOT_PATH))

    mlflow.end_run()

    print("Training Complete")


if __name__ == "__main__":
    train()