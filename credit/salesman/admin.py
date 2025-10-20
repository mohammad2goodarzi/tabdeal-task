from django.contrib import admin

from .models import Salesman, CreditRequest, PhoneNumber, CreditTransfer


admin.site.register(Salesman)
admin.site.register(CreditRequest)
admin.site.register(PhoneNumber)
admin.site.register(CreditTransfer)
