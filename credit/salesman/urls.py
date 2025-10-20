from django.urls import path, include

urlpatterns = [
    # Version 1
    path("salesman/api/v1/", include('salesman.api.v1.urls', namespace='v1')),
]
