from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
