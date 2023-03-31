from django.contrib import admin
from .models import Subdomain, SecureSocketsLayersCertificate

admin.site.register(Subdomain)
admin.site.register(SecureSocketsLayersCertificate)