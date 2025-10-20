from django.db import models


class Salesman(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CreditRequest(models.Model):
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    amount = models.IntegerField()
    state = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.amount} - {self.salesman} ({self.state})'


class PhoneNumber(models.Model):
    number = models.CharField(max_length=11)

    def __str__(self):
        return self.number


class CreditTransfer(models.Model):
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    amount = models.IntegerField()
    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)  # CASCADE?? what if I use SET_NULL??

    def __str__(self):
        return f'{self.amount} - {self.salesman} ({self.phone_number})'
