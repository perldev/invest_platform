from django.contrib import admin

from .models import Currency, Bank, BankTransfers, InvestLot, InvestDeals, Trans, \
    TransAdmin, ClientProfile, Accounts, BankTransfersAdmin
# Register your models here.


admin.site.register(Currency)
admin.site.register(Bank)
admin.site.register(BankTransfers, BankTransfersAdmin)
admin.site.register(InvestLot)
admin.site.register(InvestDeals)
admin.site.register(Trans, TransAdmin)
admin.site.register(ClientProfile)
admin.site.register(Accounts)
