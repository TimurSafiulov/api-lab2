from locust import HttpUser, task, between

class FootballAPIUser(HttpUser):
    
    wait_time = between(1, 3) 

    def on_start(self):
        """
        Ця функція виконується ОДИН РАЗ, коли віртуальний юзер "заходить на сайт".
        Тут ми виконуємо першу частину складного сценарію: отримуємо токен.
        """
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin"
        })
        
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            self.token = None

    @task(2) 
    def get_all_teams(self):
        """
        Простий тест: отримуємо список команд. 
        Демонструємо, що використовуємо токен, отриманий в on_start.
        """
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.client.get("/teams/", headers=headers)

    @task(1)
    def create_and_get_team(self):
        """
        СКЛАДНИЙ СЦЕНАРІЙ: Створюємо команду, витягуємо її ID, 
        і одразу робимо запит GET для цієї конкретної команди.
        """
        new_team = {
            "league_id": 1,
            "name": "Locust FC",
            "power_rating": 88.5
        }
       
        create_res = self.client.post("/teams/", json=new_team)
        
        if create_res.status_code == 201:
            
            team_id = create_res.json().get("id")
            
            
            self.client.get(f"/teams/{team_id}")