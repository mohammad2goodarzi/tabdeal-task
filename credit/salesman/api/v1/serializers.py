from rest_framework import serializers

from salesman.models import CreditRequest, CreditTransfer


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CreditRequest


class CreditTransferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CreditTransfer
