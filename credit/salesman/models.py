from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Value, Sum, F, FilteredRelation, Q
from django.db.models.functions import Coalesce
from django_fsm import FSMField, transition


class CreditRequestStateChoice(models.TextChoices):
    REQUESTED = 'requested'
    ACCEPTED = 'accepted'


class CreditRequestQuerySet(models.QuerySet):
    def requested(self, *args, **kwargs):
        return super(CreditRequestQuerySet, self).filter(*args, **kwargs).filter(
            state=CreditRequestStateChoice.REQUESTED,
        )

    def accepted(self, *args, **kwargs):
        return super(CreditRequestQuerySet, self).filter(*args, **kwargs).filter(
            state=CreditRequestStateChoice.ACCEPTED,
        )


class Salesman(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    total_credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class CreditRequest(models.Model):
    objects = CreditRequestQuerySet.as_manager()
    created_at = models.DateTimeField(auto_now_add=True)
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
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
    created_at = models.DateTimeField(auto_now_add=True)
    salesman = models.ForeignKey(to=Salesman, on_delete=models.CASCADE)
    amount = models.IntegerField()
    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)  # CASCADE?? what if I use SET_NULL??

    def __str__(self):
        return f'{self.amount} - {self.salesman} ({self.phone_number})'
