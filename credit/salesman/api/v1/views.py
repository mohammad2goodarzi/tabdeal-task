from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from salesman.api.v1.serializers import CreditRequestSerializer, CreditTransferSerializer
from salesman.controllers import CreditController
from salesman.models import CreditRequest, CreditTransfer


class TempAPIView(APIView):
    def get(self, *args, **kwargs):
        return Response('hello world')


class CreditRequestAPIView(CreateAPIView):
    serializer_class = CreditRequestSerializer


class CreditAcceptAPIView(GenericAPIView):
    queryset = CreditRequest.objects.requested()
    serializer_class = CreditRequestSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        CreditController().accept(instance)
        data = self.get_serializer(instance=instance).data
        return Response(data=data, status=status.HTTP_200_OK)


class CreditTransferAPIView(CreateAPIView):
    serializer_class = CreditTransferSerializer

    def perform_create(self, serializer):
        CreditController().transfer(
            salesman_id=serializer.data['salesman'],
            amount=serializer.data['amount'],
            phone_number_id=serializer.data['phone_number'],
        )
