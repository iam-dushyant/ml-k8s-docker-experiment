from locust import HttpUser, task, between

PAYLOAD = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

class IrisUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(4)
    def predict(self):
        self.client.post("/predict", json=PAYLOAD)

    @task(1)
    def health(self):
        self.client.get("/health")