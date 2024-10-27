from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('loans', views.LoanViewSet, basename='loan')

app_name = 'loan'

urlpatterns = [
    path('', include(router.urls)),
]
