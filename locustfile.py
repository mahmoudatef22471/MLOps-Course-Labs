from locust import HttpUser, task, between
# add locust file


class ChurnPredictionUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_home(self):
        self.client.get("/")

    @task(3)
    def test_health(self):
        self.client.get("/health")

    @task
    def test_predict(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": 600,
                "Geography": "France",
                "Gender": "Male",
                "Age": 40,
                "Tenure": 5,
                "Balance": 50000.0,
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 100000.0,
            },
        )
