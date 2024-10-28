from django.urls import path
from . import views
from .views import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
