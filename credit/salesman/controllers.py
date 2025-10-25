from django.db import transaction

from salesman.models import CreditTransfer, Salesman


class CreditController:
    def accept(self, db_obj):
        # What if I use a post save signal? or override save method? or any other options?
        with transaction.atomic():
            db_obj.set_as_accepted()
            salesman = Salesman.objects.select_for_update().get(pk=db_obj.salesman.pk)
            salesman.total_credit += db_obj.amount
            salesman.save()

    def transfer(self, salesman_id, amount, phone_number_id):
        with transaction.atomic():
            ct = CreditTransfer.objects.create(
                salesman_id=salesman_id,
                amount=amount,
                phone_number_id=phone_number_id,
            )
            salesman = Salesman.objects.select_for_update().get(pk=ct.salesman.pk)
            salesman.total_credit -= ct.amount
            salesman.save()
