import uuid

from locust import HttpUser, task
import random


class WebsiteUser(HttpUser):
    def on_start(self):
        self.id = uuid.uuid4()

    @task
    def index(self):
        self.client.get("/api/dudos", headers={'User-ID': str(self.id)})
