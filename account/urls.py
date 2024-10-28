from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('accounts', views.AccountViewSet, basename='account')

app_name = 'account'

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/<int:pk>/close/', views.AccountViewSet.as_view({'post': 'close_account'}), name='account-close'),
    path('accounts/<int:pk>/balance/', views.AccountViewSet.as_view({'get': 'get_balance'}), name='account-balance'),

]
