import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse_lazy
from rest_framework import status

from salesman.models import Salesman, CreditRequest, CreditRequestStateChoice, PhoneNumber, CreditTransfer


@pytest.mark.django_db
def test_credit_request(api_client):
    s = Salesman.objects.create(name="salesman1")

    url = reverse_lazy('v1:credit-request')
    payload = {
        "salesman": s.pk,
        "amount": 1000
    }

    with CaptureQueriesContext(connection) as context:
        response = api_client.post(path=url, data=payload)
        assert len(context.captured_queries) == 2

    assert response.status_code == status.HTTP_201_CREATED
    assert CreditRequest.objects.count() == 1
    cr = CreditRequest.objects.first()
    assert cr.amount == 1000
    assert cr.state == CreditRequestStateChoice.REQUESTED


credit_request_test_cases = [
    (2, 1000),
    (1, -1000),
    (1, 0),
]


@pytest.mark.parametrize("salesman,amount",
                         credit_request_test_cases)
@pytest.mark.django_db
def test_credit_request_invalid_data(api_client, salesman, amount):
    s = Salesman.objects.create(name="salesman1")

    url = reverse_lazy('v1:credit-request')
    payload = {
        "salesman": salesman,
        "amount": amount
    }
    with CaptureQueriesContext(connection) as context:
        response = api_client.post(path=url, data=payload)
        assert len(context.captured_queries) == 1

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert CreditRequest.objects.count() == 0


@pytest.mark.django_db
def test_credit_accept(api_client):
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )

    url = reverse_lazy('v1:credit-accept', kwargs={'pk': cr.pk})
    payload = {}

    with CaptureQueriesContext(connection) as context:
        response = api_client.post(path=url, data=payload)
        assert len(context.captured_queries) == 2

    assert response.status_code == status.HTTP_200_OK
    assert CreditRequest.objects.count() == 1
    cr = CreditRequest.objects.first()
    assert cr.amount == 1000
    assert cr.state == CreditRequestStateChoice.ACCEPTED


@pytest.mark.django_db
def test_invalid_credit_accept(api_client):
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    cr.set_as_accepted()

    url = reverse_lazy('v1:credit-accept', kwargs={'pk': cr.pk})
    payload = {}

    with CaptureQueriesContext(connection) as context:
        response = api_client.post(path=url, data=payload)
        assert len(context.captured_queries) == 1

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_credit_transfer(api_client):
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    cr.set_as_accepted()
    phone_number = PhoneNumber.objects.create(
        number='09120000001',
    )

    url = reverse_lazy('v1:credit-transfer')
    payload = {
        "amount": 100,
        "salesman": s.pk,
        "phone_number": phone_number.pk
    }

    with CaptureQueriesContext(connection) as context:
        response = api_client.post(path=url, data=payload)
        assert len(context.captured_queries) == 4

    assert response.status_code == status.HTTP_201_CREATED
    assert CreditTransfer.objects.count() == 1
    ct = CreditTransfer.objects.first()
    assert ct.amount == 100
    assert Salesman.objects.annotate_total_credit().first().total_credit == 900


invalid_credit_transfer = [
    (1, 1, 10000, 3),
    (1, 2, 100, 2),
    (2, 1, 100, 2),
]


@pytest.mark.parametrize("salesman_id,phone_number_id,amount,number_of_queries",
                         invalid_credit_transfer)
@pytest.mark.django_db
def test_invalid_credit_transfer(api_client, salesman_id, phone_number_id, amount, number_of_queries):
    s = Salesman.objects.create(name="salesman1")
    cr = CreditRequest.objects.create(
        salesman=s,
        amount=1000,
    )
    cr.set_as_accepted()
    phone_number = PhoneNumber.objects.create(
        number='09120000001',
    )

    url = reverse_lazy('v1:credit-transfer')
    payload = {
        "amount": amount,
        "salesman": salesman_id,
        "phone_number": phone_number_id,
    }

    with CaptureQueriesContext(connection) as context:
        response = api_client.post(path=url, data=payload)
        assert len(context.captured_queries) == number_of_queries

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert CreditTransfer.objects.count() == 0
    assert Salesman.objects.annotate_total_credit().first().total_credit == 1000
