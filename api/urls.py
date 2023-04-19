from django.urls import path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'sites', views.SiteViewSet)

urlpatterns = [
    path('subdomains/', views.getSubdomains),
    path('ssls/', views.getSecureSocketsLayersCertificate),
    path('analyze/', views.runAnalyzer),
]

urlpatterns += router.urls
