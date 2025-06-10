
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from accounts.api.router import router_user

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from appAdmin.api.router import router as crm_router


from webhook.api.views import whatsapp_webhook




schema_view = get_schema_view(
    openapi.Info(
        title="Documentation supra_enterprise_back",
        default_version='v 1.0.1',
        description="API supra_enterprise_back",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jeffer443@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin-dashboard/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


    path('api/', include('accounts.api.router')),
    path('api/', include(router_user.urls)),
    path('api/', include(crm_router.urls)),
     path('webhooks/', whatsapp_webhook, name='whatsapp-webhook'),


    # ---------------------------------------------------------------------

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
