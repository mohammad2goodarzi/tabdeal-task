from django.db import models
from django_fsm import FSMField, transition


class CreditRequestStateChoice(models.TextChoices):
    REQUESTED = 'requested'
    ACCEPTED = 'accepted'


class Salesman(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CreditRequest(models.Model):
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    amount = models.IntegerField()
    state = FSMField(
        choices=CreditRequestStateChoice.choices,
        default=CreditRequestStateChoice.REQUESTED,
    )

    def __str__(self):
        return f'{self.amount} - {self.salesman} ({self.state})'

    @transition(field='state',
                source=CreditRequestStateChoice.REQUESTED,
                target=CreditRequestStateChoice.ACCEPTED,
                custom={'button_name': 'set as accepted'})
    def set_as_accepted(self):
        pass


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
