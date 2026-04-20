from fastapi.testclient import TestClient
from main import app 


client = TestClient(app)



def test_get_teams():
    response = client.get("/teams/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  

def test_create_team():
    new_team = {
        "league_id": 1,
        "name": "Шахтар",
        "power_rating": 84.5
    }
    response = client.post("/teams/", json=new_team)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Шахтар"
    assert "id" in data

def test_get_team_success():
    response = client.get("/teams/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Динамо"

def test_get_team_not_found():
    response = client.get("/teams/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Команду не знайдено"

def test_delete_team():

    new_team = {"league_id": 1, "name": "Карпати", "power_rating": 75.0}
    create_resp = client.post("/teams/", json=new_team)
    team_id = create_resp.json()["id"]

   
    delete_resp = client.delete(f"/teams/{team_id}")
    assert delete_resp.status_code == 204


    get_resp = client.get(f"/teams/{team_id}")
    assert get_resp.status_code == 404



def test_register_user_success():
    new_user = {"username": "testuser", "password": "securepassword"}
    response = client.post("/register", json=new_user)
    assert response.status_code == 201
    assert response.json()["message"] == "Користувача успішно створено"

def test_register_existing_user():
    existing_user = {"username": "admin", "password": "admin"}
    response = client.post("/register", json=existing_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Користувач з таким логіном вже існує"

def test_login_success():
    user = {"username": "admin", "password": "admin"}
    response = client.post("/login", json=user)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    wrong_user = {"username": "admin", "password": "wrongpassword"}
    response = client.post("/login", json=wrong_user)
    assert response.status_code == 401
    assert response.json()["detail"] == "Невірний логін або пароль"