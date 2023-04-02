from django.contrib import admin
from .models import Subdomain, SecureSocketsLayersCertificate, urlsUnchecked, urlsChecked

admin.site.register(Subdomain)
admin.site.register(SecureSocketsLayersCertificate)
admin.site.register(urlsUnchecked)
admin.site.register(urlsChecked)