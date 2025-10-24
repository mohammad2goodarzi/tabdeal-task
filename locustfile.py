from random import randint, choice

from locust import HttpUser, task, between


class SalesmanUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user think time
    choices = list(range(1000, 18192))

    @task
    def request_credit(self):
        salesman = randint(1, 9)
        amount = randint(1, 10) * 1000

        self.client.post("/salesman/api/v1/credit", name='request credit', json={
            "salesman": salesman,
            "amount": amount
        })

    @task
    def request_temp(self):
        self.client.get("/salesman/api/v1/temp", name='temp')

    @task
    def accept_credit(self):
        pk = choice(self.choices)
        self.choices.remove(pk)
        self.client.post(f"/salesman/api/v1/admin/credit/{pk}/accept", name='accept credit')

    @task
    def transfer_credit(self):
        amount = randint(1, 10) * 10
        salesman = randint(1, 9)
        phone_number = randint(1, 100)
        self.client.post("/salesman/api/v1/credit/transfer", name='transfer credit', json={
            "salesman": salesman,
            "amount": amount,
            "phone_number": phone_number,
        })