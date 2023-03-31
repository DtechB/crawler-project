from django.urls import path
from . import views

urlpatterns = [
    path('subdomains/', views.getSubdomains),
    path('ssls/', views.getSecureSocketsLayersCertificate)
]