import pytest
from django.db.models import Sum, Value, FilteredRelation, Q
from django.db.models.functions import Coalesce

from salesman.controllers import CreditController
from salesman.models import Salesman, CreditRequest, CreditRequestStateChoice, CreditTransfer, PhoneNumber


@pytest.mark.django_db
def test_salesman_create():
    s = Salesman.objects.create(name="salesman1")
    assert Salesman.objects.count() == 1
    assert Salesman.objects.all().first().total_credit == 0


@pytest.mark.django_db
def test_credit_request():
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    assert CreditRequest.objects.count() == 1
    assert cr.state == CreditRequestStateChoice.REQUESTED
    assert Salesman.objects.all().first().total_credit == 0


@pytest.mark.django_db
def test_credit_acceptance():
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    assert CreditRequest.objects.count() == 1
    assert cr.state == CreditRequestStateChoice.REQUESTED
    assert Salesman.objects.all().first().total_credit == 0

    CreditController().accept(cr)
    assert CreditRequest.objects.count() == 1
    assert cr.state == CreditRequestStateChoice.ACCEPTED
    assert Salesman.objects.all().first().total_credit == 1000


@pytest.mark.django_db
def test_credit_transfer():
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    CreditController().accept(cr)

    assert Salesman.objects.all().first().total_credit == 1000

    phone_number = PhoneNumber.objects.create(
        number='09120000001',
    )
    CreditController().transfer(
        salesman_id=s.id,
        amount=100,
        phone_number_id=phone_number.id,
    )
    assert Salesman.objects.all().first().total_credit == 900


@pytest.mark.django_db(reset_sequences=True)
def test_total_credit(initial_data):
    salesmen = Salesman.objects.all()
    for s in salesmen:
        cr_list = CreditRequest.objects.filter(salesman=s, state=CreditRequestStateChoice.ACCEPTED)
        ct_list = CreditTransfer.objects.filter(salesman=s)
        total_accepted = sum(map(lambda item: item.amount, cr_list))
        total_transferred = sum(map(lambda item: item.amount, ct_list))
        assert total_accepted - total_transferred == s.total_credit
#
# salesmen = Salesman.objects.all()
# for s in salesmen:
#     cr_list = CreditRequest.objects.filter(salesman=s, state=CreditRequestStateChoice.ACCEPTED)
#     ct_list = CreditTransfer.objects.filter(salesman=s)
#     total_accepted = sum(map(lambda item: item.amount, cr_list))
#     total_transferred = sum(map(lambda item: item.amount, ct_list))
#     print(total_accepted, total_transferred, s.total_credit, total_accepted-total_transferred==s.total_credit)
