from fastapi.testclient import TestClient
from main import app
from database import Database

client = TestClient(app)

db = Database()
db.put("elden_ring", {"name": "Elden Ring", "genre": "RPG"})
app.db = db 

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world!"}

def test_get_games():
    response = client.get("/games")
    assert response.status_code == 200
    assert response.json() == {"elden_ring" : {"name": "Elden Ring", "genre": "RPG"}}

def test_get_games():
    response = client.get("/games/elden_ring")
    assert response.status_code == 200
    assert response.json() == {"name": "Elden Ring", "genre": "RPG"}

def test_create_game():
    game_info = {"name": "NIER", "genre": "ACT"}
    response = client.post("/games?game_name=nier", json=game_info)
    assert response.status_code == 200
    assert response.json() == {"name": "NIER", "genre": "ACT"}

def test_delete_game():
    response = client.delete("/games/elden_ring")
    assert response.status_code == 200
    assert response.json() == "elden_ring"

    response = client.get("/games/elden_ring")
    assert response.status_code == 404
    