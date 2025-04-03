from locust import HttpUser, task, between

class NginxUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def hit_delay_endpoint(self):
        self.client.get("/")
