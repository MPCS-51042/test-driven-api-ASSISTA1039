from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Database
# from typing import Dict

app = FastAPI()
# injected database instance
app.db = Database()

# games: Dict[str, Dict] = {"name": "NIER", "genre": {"ACT"}}

class Game(BaseModel):
    name: str
    genre: str

@app.get("/")
def hello():
    return {"hello": "world!"}

@app.get('/games')
def get_games():
    return app.db.all()

@app.get("/games/{game_name}")
def get_game(game_name: str):
    game = app.db.get(game_name)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.post("/games")
def create_game(game: Game):
    if app.db.get(game.name.lower()):
        raise HTTPException(status_code=400, detail="Game already exists")
    app.db.put(game.name.lower(), game.dict())
    return app.db.get(game.name.lower())

@app.delete("/games/{game_name}")
def delete_game(game_name: str):
    if not app.db.delete(game_name):
        raise HTTPException(status_code=404, detail="Game not found")
    return game_name