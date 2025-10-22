from django.urls import path

from . import views

app_name = 'salesman'

urlpatterns = [
    path('credit', views.CreditRequestAPIView.as_view(), name="credit-request"),
    path('admin/credit/<int:pk>/accept', views.CreditAcceptAPIView.as_view(), name="credit-accept"),
    path('credit/transfer', views.CreditTransferAPIView.as_view(), name="credit-transfer"),
]
