import streamlit as st
import pickle
from pathlib import Path

st.set_page_config(page_title="RL Tic Tac Toe")

st.title("RL Tic Tac Toe AI")


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "q_table.pkl"

with open(MODEL_PATH, "rb") as f:
    Q = pickle.load(f)


WIN_LINES = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]


if "board" not in st.session_state:
    st.session_state.board = [''] * 9

if "game_over" not in st.session_state:
    st.session_state.game_over = False


board = st.session_state.board


def check_win(player):

    return any(
        all(board[i] == player for i in line)
        for line in WIN_LINES
    )


def ai_move():

    moves = [
        i for i, v in enumerate(board)
        if v == ''
    ]

    if not moves:
        return -1

    best_move = max(
        moves,
        key=lambda m: Q.get((tuple(board), m), 0)
    )

    return best_move


def reset_game():

    st.session_state.board = [''] * 9
    st.session_state.game_over = False


def make_move(i):

    if st.session_state.game_over:
        return

    if board[i] != '':
        return

    board[i] = 'X'

    if check_win('X'):
        st.success("You Win!")
        st.session_state.game_over = True
        return

    if '' not in board:
        st.warning("Draw!")
        st.session_state.game_over = True
        return

    move = ai_move()

    if move != -1:
        board[move] = 'O'

    if check_win('O'):
        st.error("Agent Wins!")
        st.session_state.game_over = True
        return

    if '' not in board:
        st.warning("Draw!")
        st.session_state.game_over = True


for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        idx = row * 3 + col

        with cols[col]:

            st.button(
                board[idx] if board[idx] != '' else " ",
                key=f"cell_{idx}",
                on_click=make_move,
                args=(idx,),
                use_container_width=True
            )

st.button("Reset Game", on_click=reset_game)