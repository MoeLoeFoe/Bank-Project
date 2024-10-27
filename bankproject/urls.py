from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include(('user.urls', 'user'), namespace='user')),
    path('api/account/', include(('account.urls', 'account'), namespace='account')),
    path('api/loan/', include(('loan.urls', 'loan'), namespace='loan')),
    path('api/transaction/', include(('transaction.urls', 'transaction'), namespace='transaction')),
]

