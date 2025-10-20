from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from salesman.api.v1.serializers import CreditRequestSerializer
from salesman.models import CreditRequest


class CreditRequestAPIView(CreateAPIView):
    serializer_class = CreditRequestSerializer


class CreditAcceptAPIView(GenericAPIView):
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.set_as_accepted()
        data = self.get_serializer(instance=instance).data
        return Response(data=data, status=status.HTTP_200_OK)
