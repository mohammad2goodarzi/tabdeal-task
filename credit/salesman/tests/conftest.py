from random import choice, randint

import pytest

from salesman.controllers import CreditController
from salesman.models import Salesman, CreditRequest, PhoneNumber, CreditTransfer


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def initial_data():
    s1 = Salesman.objects.create(name="test_salesman1")
    s2 = Salesman.objects.create(name="test_salesman2")
    cr0 = CreditRequest.objects.create(salesman=s1, amount=10000)
    cr1 = CreditRequest.objects.create(salesman=s1, amount=20000)
    cr2 = CreditRequest.objects.create(salesman=s1, amount=30000)
    cr3 = CreditRequest.objects.create(salesman=s1, amount=40000)
    cr4 = CreditRequest.objects.create(salesman=s1, amount=50000)
    cr5 = CreditRequest.objects.create(salesman=s1, amount=10000)
    cr6 = CreditRequest.objects.create(salesman=s1, amount=20000)
    cr7 = CreditRequest.objects.create(salesman=s1, amount=30000)
    cr8 = CreditRequest.objects.create(salesman=s1, amount=40000)
    cr9 = CreditRequest.objects.create(salesman=s1, amount=50000)
    CreditController().accept(cr0)
    CreditController().accept(cr1)
    CreditController().accept(cr2)
    CreditController().accept(cr3)
    CreditController().accept(cr4)
    CreditController().accept(cr5)
    CreditController().accept(cr6)
    CreditController().accept(cr7)
    CreditController().accept(cr8)
    CreditController().accept(cr9)

    p1 = PhoneNumber.objects.create(number='09120000001')
    p2 = PhoneNumber.objects.create(number='09120000002')
    p3 = PhoneNumber.objects.create(number='09120000003')
    p4 = PhoneNumber.objects.create(number='09120000004')
    for i in range(1000):
        salesman = choice([s1, s1])
        amount = randint(1, 100)
        phone_number = choice([p1, p2, p3, p4])
        CreditController().transfer(
            salesman_id=salesman.id,
            amount=amount,
            phone_number_id=phone_number.id,
        )
