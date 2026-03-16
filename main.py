from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Football API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeagueCreate(BaseModel):
    name: str

class League(LeagueCreate):
    id: int

class TeamCreate(BaseModel):
    league_id: int
    name: str
    power_rating: float

class Team(TeamCreate):
    id: int

class MatchCreate(BaseModel):
    home_team_id: int
    away_team_id: int
    home_goals: int
    away_goals: int

class Match(MatchCreate):
    id: int


class LoginData(BaseModel):
    username: str
    password: str

leagues_db: List[League] = [League(id=1, name="УПЛ")]
teams_db: List[Team] = [
    Team(id=1, league_id=1, name="Динамо", power_rating=85.5),
    Team(id=2, league_id=1, name="Рух", power_rating=78.2)
]
matches_db: List[Match] = []


@app.post("/login")
def login(data: LoginData):
    if data.username == "admin" and data.password == "admin":
     
        return {"token": "my-super-secret-token"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірний логін або пароль")

@app.post("/teams/", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreate):
    new_id = len(teams_db) + 1
    new_team = Team(id=new_id, **team.model_dump())
    teams_db.append(new_team)
    return new_team

@app.get("/teams/", response_model=List[Team], status_code=status.HTTP_200_OK)
def get_teams(
    skip: int = Query(0, description="Пагінація: пропустити"),
    limit: int = Query(10, description="Пагінація: ліміт"),
    min_rating: Optional[float] = Query(None, description="Фільтр: мінімальний рейтинг"),
    sort_desc: Optional[bool] = Query(False, description="Сортування за рейтингом")
):
    result = teams_db
    if min_rating:
        result = [t for t in result if t.power_rating >= min_rating]
    if sort_desc:
        result = sorted(result, key=lambda x: x.power_rating, reverse=True)
    return result[skip : skip + limit]

@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    for t in teams_db:
        if t.id == team_id:
            return t
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команду не знайдено")

@app.put("/teams/{team_id}", response_model=Team)
def update_team(team_id: int, data: TeamCreate):
    for i, t in enumerate(teams_db):
        if t.id == team_id:
            teams_db[i] = Team(id=team_id, **data.model_dump())
            return teams_db[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команду не знайдено")

@app.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int):
    for i, t in enumerate(teams_db):
        if t.id == team_id:
            del teams_db[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команду не знайдено")

users_db = [{"username": "admin", "password": "admin"}]

class LoginData(BaseModel):
    username: str
    password: str


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: LoginData):
   
    for u in users_db:
        if u["username"] == data.username:
            raise HTTPException(status_code=400, detail="Користувач з таким логіном вже існує")
   
    users_db.append({"username": data.username, "password": data.password})
    return {"message": "Користувача успішно створено"}

@app.get("/users/")
def get_users():
    
    return users_db


@app.post("/login")
def login(data: LoginData):
    for u in users_db:
        if u["username"] == data.username and u["password"] == data.password:
     
            return {"token": f"secret-token-for-{data.username}"}
            
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірний логін або пароль")