import pytest
from salesman.models import Salesman, CreditRequest, CreditRequestStateChoice, CreditTransfer, PhoneNumber


@pytest.mark.django_db
def test_salesman_create():
    s = Salesman.objects.create(name="salesman1")
    assert Salesman.objects.count() == 1
    assert Salesman.objects.annotate_total_credit().first().total_credit == 0


@pytest.mark.django_db
def test_credit_request():
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    assert CreditRequest.objects.count() == 1
    assert cr.state == CreditRequestStateChoice.REQUESTED
    assert Salesman.objects.annotate_total_credit().first().total_credit == 0


@pytest.mark.django_db
def test_credit_acceptance():
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    assert CreditRequest.objects.count() == 1
    assert cr.state == CreditRequestStateChoice.REQUESTED
    assert Salesman.objects.annotate_total_credit().first().total_credit == 0

    cr.set_as_accepted()
    assert CreditRequest.objects.count() == 1
    assert cr.state == CreditRequestStateChoice.ACCEPTED
    assert Salesman.objects.annotate_total_credit().first().total_credit == 1000


@pytest.mark.django_db
def test_credit_transfer():
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    cr.set_as_accepted()

    assert Salesman.objects.annotate_total_credit().first().total_credit == 1000

    phone_number = PhoneNumber.objects.create(
        number='09120000001',
    )
    ct = CreditTransfer.objects.create(
        salesman=s,
        amount=100,
        phone_number=phone_number,
    )
    assert Salesman.objects.annotate_total_credit().first().total_credit == 900
