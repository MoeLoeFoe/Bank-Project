from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bank Management System API",
        default_version='v1',
        description="API documentation for the Bank Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include(('user.urls', 'user'), namespace='user')),
    path('api/account/', include(('account.urls', 'account'), namespace='account')),
    path('api/loan/', include(('loan.urls', 'loan'), namespace='loan')),
    path('api/transaction/', include(('transaction.urls', 'transaction'), namespace='transaction')),

    # Swagger UI and JSON schema endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
