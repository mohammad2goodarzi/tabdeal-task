from rest_framework import serializers

from salesman.models import CreditRequest, CreditTransfer, Salesman


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CreditRequest


class CreditTransferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CreditTransfer

    def is_valid(self, *, raise_exception=False):
        result = super(CreditTransferSerializer, self).is_valid(raise_exception=raise_exception)
        salesman = Salesman.objects.get(id=self.initial_data['salesman'])
        if salesman.total_credit < self.validated_data['amount']:
            raise serializers.ValidationError({'amount': 'amount is greater than your credit'})
        return result
