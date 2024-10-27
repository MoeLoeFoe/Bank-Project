from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('accounts', views.AccountViewSet, basename='account')

app_name = 'account'

urlpatterns = [
    path('', include(router.urls)),
]
