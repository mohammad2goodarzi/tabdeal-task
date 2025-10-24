from django.contrib import admin

from .models import Salesman, CreditRequest, PhoneNumber, CreditTransfer


class CreditRequestInline(admin.TabularInline):
    model = CreditRequest


class CreditTransferInline(admin.TabularInline):
    model = CreditTransfer


class SalesmanAdmin(admin.ModelAdmin):
    inlines = [CreditRequestInline, CreditTransferInline]


class CreditRequestAdmin(admin.ModelAdmin):
    list_filter = ['salesman', 'state']
    search_fields = ['salesman__name', 'amount']


class CreditTransferAdmin(admin.ModelAdmin):
    list_filter = ['salesman']
    search_fields = ['salesman__name', 'amount', 'phone_number__number']


admin.site.register(Salesman, SalesmanAdmin)
admin.site.register(CreditRequest, CreditRequestAdmin)
admin.site.register(PhoneNumber)
admin.site.register(CreditTransfer, CreditTransferAdmin)
