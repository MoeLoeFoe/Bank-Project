from django.contrib import admin
from .models import Account, Transaction, Loan, User



admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)
admin.site.register(User)