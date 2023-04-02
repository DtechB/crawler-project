from django.urls import path
from . import views

urlpatterns = [
    path('subdomains/', views.getSubdomains),
    path('ssls/', views.getSecureSocketsLayersCertificate),
    path('checked/', views.geturlsChecked),
    path('unchecked/', views.urlsUncheckedView)
]