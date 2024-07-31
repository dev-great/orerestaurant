from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from configuration.settings import base
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Ore Restaurant API Documentation",
        default_version='v1',
        description="...",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="developer@orerestaurant.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authorization/', include('authorization.urls')),
    path('api/v1/menus/', include('menu.urls')),
    path('api/v1/order/', include('order.urls')),
    path('api/v1/', include('user.urls')),
]


urlpatterns += [
    path('api/v1/docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)

admin.site.site_header = 'Ore Restaurant Control Panel'
admin.site.index_title = 'Administrators Dashboard'
admin.site.site_title = 'Control Panel'
