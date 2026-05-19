from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import pickle

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "q_table.pkl"

with open(MODEL_PATH, "rb") as f:
    Q = pickle.load(f)


class BoardInput(BaseModel):
    board: list


@app.get("/")
def home():
    return {
        "message": "RL Tic Tac Toe API Running"
    }


@app.post("/move")
async def move(data: BoardInput):

    board = data.board

    moves = [
        i for i, v in enumerate(board)
        if v == ''
    ]

    if not moves:
        return {"move": -1}

    best_move = max(
        moves,
        key=lambda m: Q.get((tuple(board), m), 0)
    )

    return {"move": best_move}