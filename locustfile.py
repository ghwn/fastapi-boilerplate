from uuid import uuid4

from locust import HttpUser, task


class LocustHttpUser(HttpUser):
    @task
    def signup_and_login(self):
        username = f"user{uuid4().hex[:8]}"
        password = "password"
        self.client.post(
            url="/api/v1/users",
            json={
                "username": username,
                "password": password,
            },
        )
        self.client.post(
            url="/auth/token",
            json={
                "username": username,
                "password": password,
            },
        )
