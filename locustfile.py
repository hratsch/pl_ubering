from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post("/api/auth/login", json={"password": "test"})
        try:
            self.token = response.json()["access_token"]
        except Exception as e:
            print(f"Login failed: {e}")
            self.environment.runner.quit()

    @task
    def get_summary(self):
        self.client.get("/api/reports/summary", headers={"Authorization": f"Bearer {self.token}"})

    @task
    def get_chart_data(self):
        self.client.get("/api/reports/chart-data", headers={"Authorization": f"Bearer {self.token}"})