from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from dj_rest_auth.registration.views import ConfirmEmailView

schema_view = get_schema_view(
    openapi.Info(
        title="Website Monitoring API",
        default_version='v1',
        description="monitor internal and external websites",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="techino2022@gmail.com"),
        license=openapi.License(name="GPLv3 License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dj_rest_auth.urls')),
    path('', include('api.urls')),
    path('api/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r"^api/registration/confirm-email/(?P<key>[-:\w]+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
